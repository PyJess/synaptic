prompt={"system": """You are an expert clinical trial protocol writer. 
                            You will generate a fully structured section of a clinical trial protocol based on the sponsor-provided input data. 
                            Always follow standard clinical trial protocol conventions, using formal, precise, and professional language.
                            The sponsor provides mandatory inputs including:

                            Sponsor Name 
                            Study Acronym 
                            Investigational Medicinal Product (IMP) 
                            Comparative Drug 
                            Study Type (e.g., Interventional) and Phase 
                            Study Design 
                            Aim of the study
                            Target Disease 
                            Randomization details
                            Drug administration details and dosages
                            Scheduled patient visits
                            Primary and secondary efficacy outcomes
                            Primary and secondary safety outcomes
                            Maximum sample size
                            Recommended inclusion and exclusion criteria.
                            Your task is to write the content for the "{chapter_title}" section of the protocol, ensuring it is comprehensive and adheres to regulatory standards.""",
        "user": "Here you find all the infrormation you need to to write the {chapter_title} section of the protocol: {input_data}",
        "retrieved": ""

}


from Evaluator import Evaluator
from SeleneEvaluator import SeleneEvaluator
from RagasEvaluator import RagasEvaluator
from DeepEvaluator import DeepEval
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolCall 
import asyncio
import aiofiles
import os
import logging
import json
from docx import Document
import re
import sys

logger = logging.getLogger(__name__)

class EvaluatorAgent():
    """
    EvaluatorAgent handles automated evaluation of LLM-generated outputs using multiple metrics.

    Attributes:
        metrics (dict): Dictionary of evaluation metric instances mapped by string identifiers.
        expected_files (list): List of required file names within each evaluation directory.
        choosen_metrics (list): List of metric identifiers to apply for evaluation.
    """
    

    def __init__(self):
        """
        Initializes the EvaluatorAgent with predefined evaluation metrics.
        """

        self.metrics = {
        "faithfulness-ragas":RagasEvaluator('faithfulness'),
        "ans-rel-ragas":RagasEvaluator('ResponseRelevancy'),
        "faithfulness-deepeval":DeepEval("faithfulness"),
        "ans-rel-deepeval":DeepEval("answer_relevancy"),
        "faithfulness-selene":SeleneEvaluator("atla_default_faithfulness"),
        "ans-rel-selene":SeleneEvaluator("atla_default_relevance")

        }
        self.choosen_metrics=["faithfulness-ragas",
                                "faithfulness-deepeval",
                                "faithfulness-selene",
                                "ans-rel-ragas",
                                "ans-rel-deepeval",
                                "ans-rel-selene"
                                ]

    async def evaluate(self, chapter_title:str, prompt:dict, output, input_data):
        final_score={}
        final_warnings={}
        root= os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Outputs"))
        metric_coroutines=[]
        input_prompt=prompt['system']+'\n\n'+prompt['user']
        input_prompt= input_prompt.replace("{chapter_title}", chapter_title)
        input_prompt= input_prompt.replace("{input_data}", input_data)
        logger.debug(f"Input prompt: {input_prompt[:200]}...")
        #Performs evaluation for provided metrics...

        task = [
                self.metrics[metric].evaluate(
                    output,
                    input_prompt,
                    context=prompt.get('retrieved', "")
                )
            for metric in self.choosen_metrics]
            
            
        results=await asyncio.gather(*task)


        for result in results:
            scores, warnings=result
            final_score= final_score | scores
            final_warnings= final_warnings | warnings

        #Saves evaluation results...
        async with aiofiles.open(os.path.join(root,f"eval_{chapter_title}.json"),'w',encoding='utf-8') as f:
            await f.write(json.dumps(final_score, indent=4))
        # async with aiofiles.open(os.path.join(root,"warn.json"),'w',encoding='utf-8') as f:
        #     await f.write(json.dumps(final_warnings, indent=4))

        return final_score, final_warnings 

async def a_invoke_model(gpt, msgs):
        return await gpt.ainvoke(msgs)


async def evaluate_chapter(file_path, chapter_title, cleaned_title, evaluator, prompt, input_data):
    print(f"Evaluating chapter: {chapter_title}")
    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            output = await f.read()

        scores, warnings = await evaluator.evaluate(
            chapter_title=chapter_title,
            prompt=prompt,
            output=output,
            input_data=input_data
        )

        print(f"\n=== SCORES ({chapter_title}) ===")
        print(scores)
        print(f"\n=== WARNINGS ({chapter_title}) ===")
        print(warnings)

        with os.open(os.path.join(os.path.join(os.path.dirname(__file__), '..', "prompts", "system_prompt.txt"))) as f:
                     system_prompt=f.read()
        with os.open(os.path.join(os.path.join(os.path.dirname(__file__), '..', "prompts", "user_prompt.txt"))) as f:
                     user_prompt=f.read()
        
        
        with os.open(os.path.join(os.path.join(os.path.dirname(__file__), '..', "prompts", "schema.json"))) as f:
                     schema=json.dumps()

        
        print("Calling LLM...")
        chapter=output
        user_prompt_filled= user_prompt.replace("{chapter}", chapter)
        gpt = ChatOpenAI(model="gpt-4.1", temperature=0.1).with_structured_output(schema=schema, strict=True)
        messages = [{"role": "system", "content": """Your goal is to detect the following variables if present in the text, if not return an empty string for that variable.
                    Here the variable that you have to detect: 
                    sponsor_name
                    study_acronym
                    tested_imp
                    comparative_drug
                    study_type
                    interventional_study_phase
                    study_design
                    comparison
                    aim_of_study
                    target_disease
                    randomization_ratio
                    randomization_blocks
                    randomization_stratification
                    apixaban_dose_initial
                    apixaban_dose_maintenance
                    dalteparin_dose_initial
                    dalteparin_dose_maintenance
                    dalteparin_max_daily_dose
                    apixaban_form
                    dalteparin_form
                    visit_schedule
                    primary_efficacy_outcome
                    secondary_efficacy_outcomes
                    primary_safety_outcome
                    major_bleeding_definition
                    secondary_safety_outcomes
                    maximum_sample_size_per_arm
                    inclusion_criteria
                    exclusion_criteria"""}
                    , {"role": "user", "content": user_prompt_filled}]
    
        response = a_invoke_model(gpt, messages)
        # crare codice che prende output e ceerca le variabili, mi restituisce un json con nome capitolo + cìvariabile
        async with aiofiles.open(os.path.join(file_path,f"{chapter_title}_variables.json"),'w',encoding='utf-8') as f:
            await f.write(json.dumps(response, indent=4))

    except Exception as e:
        print(f"Error in {chapter_title}: {e}")


async def main():
    evaluator = EvaluatorAgent()
    process_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "process"))

    for root, dirs, files in os.walk(process_dir):
        for file in files:
          if file.endswith(".docx"):
              print(f"Processing file: {file}")
              file_path = os.path.join(root, file)
              input_data = ""
              doc=Document(file_path)
              for para in doc.paragraphs:
                  if para.text:
                      input_data += str(para.text) + "\n"

    chapters_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "chapters_md"))
    tasks = []
    cleaned_title_list=[]
    for root, dirs, files in os.walk(chapters_dir):
        for file in files:
            if file != "full_output.md":
                chapter_title, ext = os.path.splitext(file)
                cleaned_title = re.sub(r'^\d+_\d+_', '', chapter_title)

                # Remove leading hashes and spaces (# or ##)
                cleaned_title = re.sub(r'^#+\s*', '', cleaned_title)
                if "##" in cleaned_title:
                      cleaned_title = cleaned_title.split('##', 1)[1].lstrip()
                cleaned_title = re.sub(r'^(\d+\.\d+)(\s+)', r'\1.\2', cleaned_title)

                cleaned_title_list.append(cleaned_title)

    print(f"CLEANED_Title: {cleaned_title_list}")
    sys.exit()
    for root, dirs, files in os.walk(chapters_dir):
        for file in files:
            if file != "full_output.md":
                chapter_title, ext = os.path.splitext(file)
                cleaned_title= chapter_title.lstrip("# ").lstrip("# ")
                file_path = os.path.join(root, file)
                tasks.append(evaluate_chapter(file_path, chapter_title,cleaned_title, evaluator, prompt, input_data))
        

    await asyncio.gather(*tasks)
                # Esegui la valutazione

async def estract_prompt(title, all_titles):
    txt_file_path=os.path.join(os.path.dirname(__file__), "..", "Protocol_instructions", "CPT_CoreBWE_v010.txt") 
    with open(txt_file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    print("finiscing reading")

    try:
        start_index = next(i for i, line in enumerate(lines) if title in line)
    except StopIteration:
        return ""  # Title not found

    # Find the index of the next title
    next_titles = [t for t in all_titles if t != title]
    #print(f"next titles: {next_titles}")
    end_index = len(lines)
    for i, line in enumerate(lines[start_index+1:], start=start_index+1):
        for nt in next_titles:
            if nt in line:  # keep exact text match, no normalization
                end_index = i
                break
        if end_index != len(lines):
            break

    # Extract lines from start_index to end_index
    extracted_lines = lines[start_index:end_index]
    return "".join(extracted_lines).strip()
     
     
                 
# Run
if __name__ == "__main__":
    # all_titles= ['1. Protocol Summary', '1.1. Synopsis', '1.2. Schema', '1.3. Schedule of Activities (SoA)', '2. Introduction', '2.1. Study Rationale', '2.2 Background', '2.3 Benefit_Risk Assessment', '3. Objectives, Endpoints, and Estimands', '3.1 Estimand(s) for Primary Objective(s)', '3.2 Estimands for Secondary Objective(s)', '3.3 Estimands for [Tertiary_Exploratory_Other] Objectives', '4. Study Design', '4.1 Overall Design', '4.2 Scientific Rationale for Study Design', '4.3 Justification for Dose', '4.4 End-of-Study Definition', '5. Study Population', '5.1 Inclusion Criteria', '5.2 Exclusion Criteria', '5.3 Lifestyle Considerations', '5.4 Screen Failures', '5.5 Criteria for Temporarily Delaying [Enrollment_', '6. Study Intervention(s) and Concomitant Therapy', '6.2 Preparation, Handling, Storage, and Accountability', '6.3 Assignment to Study Intervention', '6.4 [Blinding, Masking]', '6.5 Study Intervention Compliance', '6.6 Dose Modification', '6.7 Continued Access to Study Intervention after the End of', '6.8 Treatment of Overdose', '6.9 Prior and Concomitant Therapy', '7. Discontinuation of Study Intervention and', '7.1 Discontinuation of Study Intervention', '7.2 Participant Discontinuation_Withdrawal from the Study', '7.3 Lost to Follow up', '8. Study Assessments and Procedures', '8.1 Administrative [and General_Baseline] Procedures', '8.2 [Efficacy and_or Immunogenicity] Assessments', '8.3 Safety Assessments', '8.4 Adverse Events (AEs) Serious Adverse Events (SAEs),', '8.5 Pharmacokinetics', '8.6 Pharmacodynamics', '8.7 Genetics', '8.8 Biomarkers', '8.9 Immunogenicity Assessments', '8.10 [Health Economics OR Medical Resource Utilization and', '9. Statistical Considerations', '9.1 General Considerations', '9.2 Analysis Sets', '9.3 Analyses Supporting Primary Objective(s)', '9.4 Analyses Supporting Secondary Objective(s)', '9.5 Analyses Supporting Tertiary_Exploratory_Other', '9.6 Other Safety Analyses', '9.7 Other Analyses', '9.8 Interim Analyses', '9.9 Sample Size Determination', '10.1 Appendix 1_ Regulatory, Ethical, and Study Oversight', '10.2 Appendix 2_ Clinical Laboratory Tests', '10.3 Appendix 3_ AEs and SAEs_ Definitions and Procedures', '10.4 Appendix 4_ Contraceptive and Barrier Guidance', '10.5 Appendix 5_ Genetics', '10.6 Appendix 6_ Liver Safety_ Suggestions and Guidelines']
    asyncio.run(main())
    # a= asyncio.run(estract_prompt('1.3. Schedule of Activities (SoA)', all_titles))
    # print(a)

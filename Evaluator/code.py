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
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolCall 
import asyncio
import aiofiles
import os
import logging
import json
from docx import Document

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
                                # "faithfulness-selene",
                                "ans-rel-ragas",
                                "ans-rel-deepeval",
                                # "ans-rel-selene"
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



async def evaluate_chapter(file_path, chapter_title, evaluator, prompt, input_data):
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
    for root, dirs, files in os.walk(chapters_dir):
        for file in files:
            if file != "full_output.md":
                chapter_title, ext = os.path.splitext(file)
                file_path = os.path.join(root, file)
                tasks.append(evaluate_chapter(file_path, chapter_title, evaluator, prompt, input_data))
        

    await asyncio.gather(*tasks)
                # Esegui la valutazione
               
# Run
if __name__ == "__main__":
    asyncio.run(main())

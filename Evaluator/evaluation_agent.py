import asyncio
import sys
import os

import aiofiles
src_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
output_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','outputs'))
docs_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','docs'))
sys.path.append(src_path)
import json
#from utils.TemplateAgent import Agent
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.tools import tool

from .Evaluator import Evaluator
from .SeleneEvaluator import SeleneEvaluator
from .RagasEvaluator import RagasEvaluator
#from utils.CrossEntropyEvaluator import EntropyEvaluator
from .DeepEvaluator import DeepEval
#from utils.MockEvaluator import MockEvaluator
#from utils.CrossEntropyEvaluator import EntropyEvaluator
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolCall 
#from selfhealingagent.SelfHealing import SelfHealing

class EvaluatorAgent():
    """
    EvaluatorAgent handles automated evaluation of LLM-generated outputs using multiple metrics.

    Attributes:
        metrics (dict): Dictionary of evaluation metric instances mapped by string identifiers.
        expected_files (list): List of required file names within each evaluation directory.
        choosen_metrics (list): List of metric identifiers to apply for evaluation.
    """
    
    metrics:dict[str, Evaluator]={
        "faithfulness-ragas":RagasEvaluator('faithfulness'),
        "ans-rel-ragas":RagasEvaluator('ResponseRelevancy'),
        "faithfulness-deepeval":DeepEval("faithfulness"),
        "ans-rel-deepeval":DeepEval("answer_relevancy"),
        "faithfulness-selene":SeleneEvaluator("atla_default_faithfulness"),
        "ans-rel-selene":SeleneEvaluator("atla_default_relevance")
        #"crossentropy":EntropyEvaluator()
        #"mock-metric":MockEvaluator({"mock-score":0.6, "mock-reason":"all words should be preceeded by 'cat'"},{"mock-warning":True})
    }

    expected_files=["prompt.json","output.json","logprobs.json"]

    def __init__(self):
        """
        Initializes the EvaluatorAgent with predefined evaluation metrics.
        """
        self.choosen_metrics=["faithfulness-ragas",
                                "faithfulness-deepeval",
                                # "faithfulness-selene",
                                "ans-rel-ragas",
                                "ans-rel-deepeval",
                                # "ans-rel-selene",
                                #"crossentropy",
                                #"mock-metric"
                                ]
        

    def invoke(self, state:MessagesState):
        """
        Synchronous wrapper to run the asynchronous evaluation.

        Args:
            state (MessagesState): The current message state for LangGraph.

        Returns:
            dict: Contains updated messages with evaluation results.
        """
        print("Running Evaluation")
        return asyncio.run(self.ainvoke(state))

    async def ainvoke(self, state:MessagesState):
        """
        Asynchronous evaluation trigger function used in LangGraph node.

        Args:
            state (MessagesState): The current state containing message history and tool calls.

        Returns:
            dict: Updated message state including potential healing tool calls.
        """

        user_id=state["messages"][-1].additional_kwargs.get('uuid')

        print(f"Running evaluation with id: {user_id}")
        if tool_calls:=state["messages"][-1].tool_calls:

            tool_call=[tool for tool in tool_calls if tool["name"]=="EvalAgent"][0]

            ret_tool_calls=[]
            #IF the message contains an evaluation tool call...
            if tool_call["name"]=="EvalAgent":
                input_dir=tool_call['args']['input_dir']
                metrics=tool_call['args']['metrics']

                tasks=[]
                #Explore the directory to find folders containing prompt and output to evaluate...
                for root, _, filenames in os.walk(input_dir):
                    if all([exp_file in filenames for exp_file in self.expected_files]):
                        
                        tasks.append(asyncio.create_task(self.evaluate(root, tool_call)))

                ret_tool_calls=await asyncio.gather(*tasks)

                ret_tool_calls=list([tool_call for tool_call in ret_tool_calls if tool_call])
                if ret_tool_calls:
                    return {"messages":[AIMessage("Evaluation generated, warnings detected, proceed to healing", 
                                                  tool_calls=ret_tool_calls, 
                                                  warning_count=len(ret_tool_calls), 
                                                  additional_kwargs=state["messages"][-1].additional_kwargs)]}
                else:
                    return {"messages":[AIMessage("Evaluation generated, no warnings detected", 
                                                  warning_count=0 , 
                                                  additional_kwargs=state["messages"][-1].additional_kwargs)]}
                
        return {"messages":[AIMessage("No evaluation necessary!" , 
                                      additional_kwargs=state["messages"][-1].additional_kwargs)]}
    
    async def evaluate(self, root, tool_call):
        """
        Evaluates a single prompt/output folder using multiple metrics.

        Args:
            root (str): Absolute path to the folder containing prompt/output to evaluate.
            tool_call (ToolCall): The tool call object containing parameters like input_dir.

        Returns:
            dict or None: Tool call for healing if warnings are found, otherwise None.
        """
        # print(f"Evaluating dir: {root}")
        async with aiofiles.open(os.path.join(root, "prompt.json")) as f:
            prompt=json.loads(await f.read())
        async with aiofiles.open(os.path.join(root, "output.json")) as f:
            output=json.loads(await f.read())

        final_score={}
        final_warnings={}
        
        metric_coroutines=[]
        #Performs evaluation for provided metrics...
        for metric in self.choosen_metrics:
            metric_coroutines.append(asyncio.create_task(self.metrics[metric].evaluate(str(output['assistant']), 
                                            input_prompt=prompt['system']+'\n\n'+prompt['user'],
                                            context=prompt.get('retrieved', ""),
                                            folder_name=root)))
            
        results=await asyncio.gather(*metric_coroutines)

        for result in results:
            scores, warnings=result
            final_score= final_score | scores
            final_warnings= final_warnings | warnings

        #Saves evaluation results...
        async with aiofiles.open(os.path.join(root,"eval.json"),'w',encoding='utf-8') as f:
            await f.write(json.dumps(final_score, indent=4))
        async with aiofiles.open(os.path.join(root,"warn.json"),'w',encoding='utf-8') as f:
            await f.write(json.dumps(final_warnings, indent=4))

        #If any evaluation is below threshold (warning issued) forwards 
        #evaluator's reason to healing tool
        #NOTE: return message will contain multiple tool calls depending
        #      0<=heal_tool_count<=generated_content_count
        #      where `generated_content_count` is the number of folders containing 
        #      prompt.json and output.json

        reasons=[]
        for key, value in final_warnings.items():
            if value and key.replace("warning","reason") in final_score:
                reasons.append(final_score[key.replace("warning","reason")])
                # print(f"Reason added: {reasons[-1]}")

        if reasons:
            ret_tool_call={
                "name":"heal",
                "id":f"heal_{tool_call['id']}",
                "args":{"input_dir":root,
                        "user":None,
                        "reasons":reasons},
                "type":"tool_call"
            }   
                        
            return ret_tool_call
        return None
                        
if __name__ == "__main__":
    agent = EvaluatorAgent()
    
    graph_builder=StateGraph(MessagesState)
    graph_builder.add_node("EvalAgent", agent.ainvoke)
    graph_builder.add_edge(START, "EvalAgent")
    graph_builder.add_edge("EvalAgent", END)
    graph=graph_builder.compile()

 # Create an initial message with the 'eval' tool call

    tool_call = ToolCall(
        name="EvalAgent",
        args={"input_dir": os.path.join(output_path, "agent2_None"),},
        id="tool_call_eval"
    )

    # Create message with proper ToolCall instance
    message = AIMessage(
        content='',
        tool_calls=[tool_call]
    )
    # Execute the graph asynchronously
    async def main():
        result = await graph.ainvoke({"messages": [message]})
        print("Evaluation Result:", result)

    asyncio.run(main())

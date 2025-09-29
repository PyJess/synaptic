import os
import asyncio
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from ragas.metrics import AspectCritic, Faithfulness, ResponseRelevancy
from ragas import SingleTurnSample
from Evaluator import Evaluator

# Initialize necessary components for Ragas
evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
evaluator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())

output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','outputs'))

class RagasEvaluator(Evaluator):
    """
    Evaluator class using Ragas metrics for evaluating LLM outputs.

    Attributes:
        metric_name (str): Name of the metric to use for evaluation.
        metric (AspectCritic): The metric object initialized with the specified metric name.
    """

    def __init__(self, metric="faithfulness"):
        """
        Initializes the RagasEvaluator with a specified metric.

        Args:
            metric (str): The name of the metric to use (default: "faithfulness").
        """
        super().__init__()
        self.metric_name = metric
        # Initialize the metric as an AspectCritic with the given name and LLM
        self.metric = AspectCritic(
            name=self.metric_name,
            llm=evaluator_llm,
            definition="Verify if the response is faithful."
        )
        # Alternative: self.metric = Faithfulness(name=metric_name, llm=evaluator_llm)

    async def evaluate(self, output_prompt, input_prompt=None, context=None, result=None, **kwargs):
        """
        Asynchronously evaluates the output of an LLM using the specified Ragas metric.

        Args:
            output_prompt (str): The generated response to evaluate.
            input_prompt (str, optional): The original user input prompt. Defaults to None.
            context (list or str, optional): The context(s) retrieved for the response. Can be a string or a list of strings. Defaults to None.
            result: Unused, kept for compatibility.
            **kwargs: Additional keyword arguments (unused).

        Returns:
            tuple: A tuple containing:
                - eval_dict (dict): Dictionary with the metric score.
                - warnings (dict): Dictionary with a warning flag if the score is below threshold.

        Notes:
            - The function expects absolute or relative paths only for internal file operations (not as parameters).
            - The context parameter is converted to a list if it is not already one.
            - Uses Ragas' AspectCritic metric for evaluation.
        """
        # Re-initialize the metric for each evaluation to ensure statelessness
        metric = AspectCritic(
            name=self.metric_name,
            llm=evaluator_llm,
            definition="Verify if the response is faithful."
        )

        try:
            # Ensure context is a list (required by SingleTurnSample)
            if not isinstance(context, list):
                context = [context] if context else []

            metric_name = self.metric_name

            # Create a SingleTurnSample object for evaluation
            test_data = SingleTurnSample(
                user_input=input_prompt or "",
                response=output_prompt,
                retrived_contexts=context
            )

            # Evaluate the response using the selected metric
            evaluation_output = await metric.single_turn_ascore(test_data)

            # Prepare the evaluation result dictionary
            eval_dict = {
                f"{self.metric_name}-Ragas-score": evaluation_output,
            }

            # Prepare the warnings dictionary (score threshold set at 0.8)
            warnings = {
                f"{self.metric_name}-Ragas-warning": evaluation_output < 0.8
            }

        except Exception as e:
            # Print and return empty results in case of error
            print(f"An error occurred: {e}")
            return {}, {}

        return eval_dict, warnings
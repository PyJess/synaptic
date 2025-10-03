import asyncio
from atla import Atla, BadRequestError
from Evaluator import Evaluator
import os

'''
Supported metrics:
- atla_default_faithfulness
- atla_default_logical_coherence
- atla_default_helpfulness
- atla_default_relevance
'''

class SeleneEvaluator(Evaluator):
    """
    Evaluator class that uses the Atla Selene model to assess outputs based on a selected metric.
    """

    def __init__(self, metric="atla_default_logical_coherence"):
        """
        Initializes the SeleneEvaluator.

        Parameters:
            metric (str): The evaluation metric to use. 
                          Supported values include:
                          'atla_default_faithfulness', 
                          'atla_default_logical_coherence', 
                          'atla_default_helpfulness', 
                          'atla_default_relevance'.
                          Defaults to 'atla_default_logical_coherence'.
        """
        self.atla = Atla(api_key="pylf_v1_eu_LqkjqcVJFjQQjy3bMxKRrDQnnkgxpkVx8k4kPt0lt8FD")
        self.metric = metric

    async def evaluate(self, output_prompt, input_prompt=None, context=None, **kwargs):
        """
        Evaluates the output asynchronously using the Atla Selene evaluation API.

        Parameters:
            output_prompt (str): The generated output to be evaluated.
            input_prompt (str, optional): The input prompt given to the model.
            context (str, optional): Additional context for the evaluation.
            **kwargs: Additional keyword arguments (not used).

        Returns:
            tuple: 
                - eval_dict (dict): Contains the normalized score and critique.
                - warnings (dict): Contains a warning flag if the score is less than 4.
        """
        # Run the synchronous API call in a separate thread
        return await asyncio.to_thread(
            self._evaluate_sync,
            output_prompt,
            input_prompt,
            context
        )
    
    def _evaluate_sync(self, output_prompt, input_prompt, context):
        """
        Internal synchronous method that calls the Atla API.
        
        How it works:
            - Calls the Atla API to create an evaluation.
            - Retrieves the evaluation result, including a score and critique.
            - Normalizes the score to a 0-1 scale (original score is out of 5).
            - Returns evaluation results and warnings.
        """
        try:
            evaluation = self.atla.evaluation.create(
                model_id="atla-selene",
                model_input=input_prompt,
                model_output=output_prompt,
                model_context=context,
                metric_name=self.metric
            ).result.evaluation
            
            # Prepare the evaluation dictionary with normalized score and critique
            eval_dict = {
                f'{self.metric}-selene-score': float(evaluation.score) / 5.0,
                f'{self.metric}-selene-reason': evaluation.critique
            }

            # Prepare warnings if the score is less than 4
            warnings = {
                f'{self.metric}-selene-warning': float(evaluation.score) < 4
            }

        except BadRequestError as e:
            # Handle API errors gracefully
            eval_dict = {
                f'{self.metric}-selene-score': 1.0,
                f'{self.metric}-selene-reason': f"BadRequest: {str(e)}"
            }
            warnings = {
                f'{self.metric}-selene-warning': True
            }
        except Exception as e:
            # Catch any other unexpected errors
            eval_dict = {
                f'{self.metric}-selene-score': 1.0,
                f'{self.metric}-selene-reason': f"Error: {str(e)}"
            }
            warnings = {
                f'{self.metric}-selene-warning': True
            }

        return eval_dict, warnings
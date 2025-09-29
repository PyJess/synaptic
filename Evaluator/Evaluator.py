
from typing import Any


class Evaluator():
    """Template class for agent evaluators, this can be combined and  will be called after the agent runs the completion"""
    def __init__(self):
        pass

    async def evaluate(self, output_prompt, input_prompt, context=None):
        """Template function for evaluator"""
        pass
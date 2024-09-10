"""The interface to the OpenAI API."""

import os

from ..framework.provider_interface import ProviderInterface


class OpenAIInterface(ProviderInterface):
    """Implements the ProviderInterface for interacting with OpenAI's APIs."""

    def __init__(self):
        """Set up the OpenAI client using the API key obtained from the user's environment."""
        import openai

        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def chat_completion_create(self, messages=None, model=None, temperature=0):
        """Request chat completions from the OpenAI API.

        Args:
        ----
            model (str): Identifies the specific provider/model to use.
            messages (list of dict): A list of message objects in chat history.
            temperature (float): The temperature to use in the completion.

        Returns:
        -------
            The API response with the completion result.

        """
        return self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )

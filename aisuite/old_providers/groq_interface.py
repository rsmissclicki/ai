"""The interface to the Groq API."""

import os

from ..framework.provider_interface import ProviderInterface


class GroqInterface(ProviderInterface):
    """Implements the ProviderInterface for interacting with Groq's APIs."""

    def __init__(self):
        """Set up the Groq client using the API key obtained from the user's environment."""
        import groq

        self.groq_client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

    def chat_completion_create(self, messages=None, model=None, temperature=0):
        """Request chat completions from the Groq API.

        Args:
        ----
            model (str): Identifies the specific provider/model to use.
            messages (list of dict): A list of message objects in chat history.
            temperature (float): The temperature to use in the completion.

        Returns:
        -------
            The API response with the completion result.

        """
        return self.groq_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )

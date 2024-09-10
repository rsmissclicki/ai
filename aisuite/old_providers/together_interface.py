"""The interface to the Together API."""

import os

from ..framework.provider_interface import ProviderInterface

_TOGETHER_BASE_URL = "https://api.together.xyz/v1"


class TogetherInterface(ProviderInterface):
    """Implements the ProviderInterface for interacting with Together's APIs."""

    def __init__(self):
        """Set up the Together client using the API key obtained from the user's environment."""
        from openai import OpenAI

        self.together_client = OpenAI(
            api_key=os.getenv("TOGETHER_API_KEY"),
            base_url=_TOGETHER_BASE_URL,
        )

    def chat_completion_create(self, messages=None, model=None, temperature=0):
        """Request chat completions from the Together API.

        Args:
        ----
            model (str): Identifies the specific provider/model to use.
            messages (list of dict): A list of message objects in chat history.
            temperature (float): The temperature to use in the completion.

        Returns:
        -------
            The API response with the completion result.

        """
        return self.together_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )

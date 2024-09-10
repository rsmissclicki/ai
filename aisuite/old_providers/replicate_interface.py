"""The interface to the Replicate API."""

import os

from ..framework.provider_interface import ProviderInterface

_REPLICATE_BASE_URL = "https://openai-proxy.replicate.com/v1"


class ReplicateInterface(ProviderInterface):
    """Implements the ProviderInterface for interacting with Replicate's APIs."""

    def __init__(self):
        """Set up the Replicate client using the API key obtained from the user's environment."""
        from openai import OpenAI

        self.replicate_client = OpenAI(
            api_key=os.getenv("REPLICATE_API_KEY"),
            base_url=_REPLICATE_BASE_URL,
        )

    def chat_completion_create(self, messages=None, model=None, temperature=0):
        """Request chat completions from the Replicate API.

        Args:
        ----
            model (str): Identifies the specific provider/model to use.
            messages (list of dict): A list of message objects in chat history.
            temperature (float): The temperature to use in the completion.

        Returns:
        -------
            The API response with the completion result.

        """
        return self.replicate_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )

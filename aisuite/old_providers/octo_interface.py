"""The interface to the Octo API."""

import os

from ..framework.provider_interface import ProviderInterface

_OCTO_BASE_URL = "https://text.octoai.run/v1"


class OctoInterface(ProviderInterface):
    """Implements the ProviderInterface for interacting with Octo's APIs."""

    def __init__(self):
        """Set up the Octo client using the API key obtained from the user's environment."""
        from openai import OpenAI

        self.octo_client = OpenAI(
            api_key=os.getenv("OCTO_API_KEY"),
            base_url=_OCTO_BASE_URL,
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
        return self.octo_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )

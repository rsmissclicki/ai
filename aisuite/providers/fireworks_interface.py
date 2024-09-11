"""The interface to the Fireworks API."""

import os

from ..framework.provider_interface import ProviderInterface


class FireworksInterface(ProviderInterface):
    """Implements the ProviderInterface for interacting with Fireworks's APIs."""

    def __init__(self):
        """Set up the Fireworks client using the API key obtained from the user's environment."""
        from fireworks.client import Fireworks

        self.fireworks_client = Fireworks(api_key=os.getenv("FIREWORKS_API_KEY"))

    def chat_completion_create(self, messages=None, model=None, temperature=0):
        """Request chat completions from the Fireworks API.

        Args:
        ----
            model (str): Identifies the specific provider/model to use.
            messages (list of dict): A list of message objects in chat history.
            temperature (float): The temperature to use in the completion.

        Returns:
        -------
            The API response with the completion result.

        """
        return self.fireworks_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )

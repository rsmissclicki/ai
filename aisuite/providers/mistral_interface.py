import os

from aisuite.framework import ProviderInterface


class MistralInterface(ProviderInterface):
    """Implements the provider interface for Mistral."""

    def __init__(self):
        from mistralai.client import MistralClient

        self.mistral_client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

    def chat_completion_create(self, messages=None, model=None, temperature=0):
        """Request chat completions from the Mistral API.

        Args:
        ----
            model (str): Identifies the specific provider/model to use.
            messages (list of dict): A list of message objects in chat history.
            temperature (float): The temperature to use in the completion.

        Returns:
        -------
            The API response with the completion result.

        """
        from mistralai.models.chat_completion import ChatMessage

        messages = [
            ChatMessage(role=message["role"], content=message["content"])
            for message in messages
        ]
        return self.mistral_client.chat(
            model=model,
            messages=messages,
            temperature=temperature,
        )

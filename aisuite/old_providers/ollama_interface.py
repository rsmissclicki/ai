"""The interface to the Ollama API."""

from aisuite.framework import ProviderInterface, ChatCompletionResponse
from httpx import ConnectError
import os


class OllamaInterface(ProviderInterface):
    """Implements the ProviderInterface for interacting with the Ollama API."""

    _OLLAMA_STATUS_ERROR_MESSAGE = "Ollama is likely not running. Start Ollama by running `ollama serve` on your host."

    def __init__(
        self, server_url=os.getenv("OLLAMA_API_URL", "http://localhost:11434")
    ):
        """Set up the Ollama API client with the key from the user's environment."""
        from ollama import Client

        self.ollama_client = Client(host=server_url)

    def chat_completion_create(self, messages=None, model=None, temperature=0):
        """Request chat completions from Ollama.

        Args:
        ----
            model (str): Identifies the specific provider/model to use.
            messages (list of dict): A list of message objects in chat history.
            temperature (float): The temperature to use in the completion.

        Raises:
        ------
            RuntimeError: If the Ollama server is not reachable,
                we catch the ConnectError from the underlying httpx library
                used by the Ollama client.

        Returns:
        -------
            The ChatCompletionResponse with the completion result.

        """
        try:
            response = self.ollama_client.chat(
                model=model,
                messages=messages,
                options={"temperature": temperature},
            )
        except ConnectError:
            raise RuntimeError(self._OLLAMA_STATUS_ERROR_MESSAGE)

        text_response = response["message"]["content"]
        chat_completion_response = ChatCompletionResponse()
        chat_completion_response.choices[0].message.content = text_response

        return chat_completion_response

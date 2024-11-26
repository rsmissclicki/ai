import httpx
import os
from aisuite.provider import Provider, LLMError


class FeatherlessProvider(Provider):
    BASE_URL = "https://api.featherless.ai/v1/chat/completions"

    def __init__(self, **config):
        """
        Initialize the Featherless provider with the given configuration.
        Pass the entire configuration dictionary to the OpenAI client constructor.
        """
        # Ensure API key is provided either in config or via environment variable
        self.api_key = os.getenv("FEATHERLESS_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Featherless API key is missing. Please provide it in the config"
            )

    def chat_completions_create(self, model, messages, **kwargs):

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": model,
            "messages": messages,
            **kwargs,  # Pass any additional arguments to the API
        }

        try:
            response = httpx.post(self.BASE_URL, json=data, headers=headers, timeout=30)
            response.raise_for_status()
        except httpx.HTTPStatusError as http_err:
            raise LLMError(f"Featherless request failed: {http_err}")
        except Exception as e:
            raise LLMError(f"An error occurred: {e}")

        return response.json()

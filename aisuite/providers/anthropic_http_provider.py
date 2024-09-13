import os
import httpx
from aisuite.provider import Provider, LLMError
from aisuite.framework import ChatCompletionResponse

# Define a constant for the default max_tokens value
DEFAULT_MAX_TOKENS = 4096


class AnthropicProvider(Provider):
    """
    Anthropic Provider using httpx for direct API calls instead of the SDK.
    """

    BASE_URL = "https://api.anthropic.com/v1/messages"
    API_VERSION = "2023-06-01"

    def __init__(self, **config):
        """
        Initialize the Anthropic provider with the given configuration.
        The API key is fetched from the config or environment variables.
        """
        self.api_key = config.get("api_key") or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key is missing. Please provide it in the config or set the ANTHROPIC_API_KEY environment variable."
            )

        # Optionally set a custom timeout (default to 30s)
        self.timeout = config.get("timeout", 30)

    def chat_completions_create(self, model, messages, **kwargs):
        """
        Makes a request to the Anthropic chat completions endpoint using httpx.
        """
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": self.API_VERSION,
            "content-type": "application/json",
        }

        # Extract and handle system message if present
        system_message = None
        if messages[0]["role"] == "system":
            system_message = messages[0]["content"]
            messages = messages[1:]

        # Set default max_tokens if not provided
        kwargs.setdefault("max_tokens", DEFAULT_MAX_TOKENS)

        data = {
            "model": model,
            "messages": messages,
            "system": system_message,
            **kwargs,  # Pass any additional arguments to the API
        }

        try:
            # Make the request to the Anthropic API
            response = httpx.post(
                self.BASE_URL, json=data, headers=headers, timeout=self.timeout
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as http_err:
            raise LLMError(f"Anthropic API request failed: {http_err}")
        except Exception as e:
            raise LLMError(f"An error occurred: {e}")

        # Return the normalized response
        return self._normalize_response(response.json())

    def _normalize_response(self, response_data):
        """
        Normalize the Anthropic API response to a common format (ChatCompletionResponse).
        """
        normalized_response = ChatCompletionResponse()
        normalized_response.choices[0].message.content = response_data["content"][0][
            "text"
        ]
        return normalized_response

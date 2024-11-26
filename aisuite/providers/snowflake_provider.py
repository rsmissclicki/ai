import os
import httpx
from aisuite.provider import Provider, LLMError
from aisuite.framework import ChatCompletionResponse
from functools import cached_property


class SnowflakeProvider(Provider):
    """
    Snowflake Cortex Provider using httpx for direct API calls instead
    of using the snowflake-ml-python library. At the time of writing,
    the snowflake-ml-python library does not support python 3.12. It's
    also fairly large and has a lot of dependencies that increase the
    size of the package. This provider provides the same chat completion
    functionality using httpx following the work done on the snowflake-ml-python
    library as a guide.

    To set up Authentication and Authorization, follow the steps provided by
    Snowflake here:
        - https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-llm-rest-api#setting-up-authentication
    """

    def __init__(self, **config: dict) -> None:
        """
        Initialize the Snowflake provider with the given configuration.
        The Bearer token and Account Identifier are fetched from the config
        if available, otherwise it falls back to environment variables.
        """
        self.jwt_token: str = config.get(
            "snowflake_jwt_token", os.getenv("SNOWFLAKE_JWT_TOKEN")
        )
        self.account_identifier: str = config.get(
            "snowflake_account_identifier", os.getenv("SNOWFLAKE_ACCOUNT_IDENTIFIER")
        )

        if not self.jwt_token:
            raise ValueError(
                "Snowflake JWT Bearer Token is missing. Please provide it in the config or set the SNOWFLAKE_JWT_TOKEN environment variable."
            )

        if not self.account_identifier:
            raise ValueError(
                "Snowflake Account Identifier is missing. Please provide it in the config or set the SNOWFLAKE_ACCOUNT_IDENTIFIER environment variable."
            )

        # Optionally set a custom timeout (default to 30s)
        self.timeout: int = int(config.get("timeout", 30))
        self.complete_url: str = (
            f"https://{self.account_identifier}.snowflakecomputing.com/api/v2/cortex/inference:complete"
        )

    @cached_property
    def headers(self) -> dict[str, str]:
        """
        Return the headers to be used in the request.
        """
        return {
            "X-Snowflake-Authorization-Token-Type": "KEYPAIR_JWT",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }

    def _normalize_response(self, response_data: dict) -> ChatCompletionResponse:
        """
        Parses the Snowflake Cortex COMPLETE response and normalizes the
        response to a common format (ChatCompletionResponse).

        Snowflake Cortex COMPLETE response:
            - https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-llm-rest-api#id1
        """
        normalized_response = ChatCompletionResponse()
        normalized_response.choices[0].message.content = response_data["choices"][0][
            "delta"
        ]["content"]
        return normalized_response

    def chat_completions_create(
        self, model: str, messages: list[dict[str, str]], **kwargs
    ) -> ChatCompletionResponse:
        """
        Makes a request to the Snowflake Cortex COMPLETE endpoint using httpx.
        See available optional json arguments here:
            - https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-llm-rest-api#optional-json-arguments
        """

        data = {
            "model": model,
            "messages": messages,
            **kwargs,  # Pass any additional arguments to the API
        }

        try:
            # Make the request to Snowflake Cortex COMPLETE endpoint.
            response = httpx.post(
                self.complete_url, json=data, headers=self.headers, timeout=self.timeout
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as http_err:
            raise LLMError(f"Snowflake Cortex request failed: {http_err}")
        except Exception as e:
            raise LLMError(f"An error occurred: {e}")

        # Return the normalized response
        return self._normalize_response(response.json())

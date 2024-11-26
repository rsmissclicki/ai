from aisuite.provider import Provider
from aisuite.framework import ChatCompletionResponse
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole
import os 

DEFAULT_MAX_TOKENS = 4096

class DatabricksProvider(Provider):
    def __init__(self, **config):
        """
        Initialize the Databricks provider with the given configuration.
        Pass the entire configuration dictionary.
        """
        config.setdefault("host", os.getenv("DATABRICKS_HOST"))
        config.setdefault("token", os.getenv("DATABRICKS_TOKEN"))
        config.setdefault("client_id", os.getenv("DATABRICKS_CLIENT_ID"))
        config.setdefault("client_secret", os.getenv("DATABRICKS_CLIENT_SECRET"))

        if not config["host"]: 
            raise ValueError(
                " Host is missing. Please provide it in the config or set the DATABRICKS_HOST environment variable."
            )
        
        if not (config["client_id"] and config["client_secret"]): 
            if not config["token"]:
                # no auth at all
                raise ValueError(
                    " Authentication is missing. Please provide client id and secret or token in the config or set the DATABRICKS_CLIENT_ID and DATABRICKS_CLIENT_SECRET or DATABRICKS_TOKEN environment variable."
                )


        self.w = WorkspaceClient(**config)

    def chat_completions_create(self, model, messages, **kwargs):
        if messages[0]["role"] == "system":
            system_message_content = [ChatMessage(role=ChatMessageRole.SYSTEM, content=messages[0]["content"])]
            messages = messages[1:]
            user_messages = [ChatMessage(role=ChatMessageRole.USER, content=messages[m]['content']) for m in range(len(messages))]
            messages_formatted = system_message_content + user_messages
        else:
            messages_formatted = [ChatMessage(role=ChatMessageRole.USER, content=messages[m]['content']) for m in range(len(messages))]

        if "max_tokens" not in kwargs:
            kwargs["max_tokens"] = DEFAULT_MAX_TOKENS

        return self.normalize_response(self.w.serving_endpoints.query(
            name=model, 
            messages = messages_formatted, 
            **kwargs
        ))


    def normalize_response(self, response):
        """Normalize the response from the Databricks SDK to match OpenAI's response format."""
        normalized_response = ChatCompletionResponse()
        normalized_response.choices[0].message.content = response.choices[0].message.content
        return normalized_response
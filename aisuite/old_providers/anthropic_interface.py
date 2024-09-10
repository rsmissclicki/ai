"""The interface to the Anthropic API."""

import os

from aisuite.framework import ProviderInterface, ChatCompletionResponse


class AnthropicInterface(ProviderInterface):
    """Implements the ProviderInterface for interacting with the Anthropic API."""

    def __init__(self):
        """Set up the Anthropic API client with the key from the user's environment"""
        import anthropic

        self.anthropic_client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    def chat_completion_create(self, messages=None, model=None, temperature=0):
        """Request chat completions from the Anthropic API.

        Args:
        ----
            model (str): Identifies the specific provider/model to use.
            messages (list of dict): A list of message objects in chat history.
            temperature (float): The temperature to use in the completion.

        Returns:
        -------
            The ChatCompletionResponse with the completion result.

        """
        anthropic_messages = []
        system_message = None
        for msg in messages:
            if "role" in msg and "content" in msg:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    temp_msg = msg.copy()
                    temp_msg["content"] = [
                        {"type": "text", "text": temp_msg["content"]}
                    ]
                    anthropic_messages.append(temp_msg)

        if system_message is None:
            response = self.anthropic_client.messages.create(
                messages=anthropic_messages,
                model=model,
                max_tokens=4096,
                temperature=temperature,
            )
        else:
            response = self.anthropic_client.messages.create(
                messages=anthropic_messages,
                model=model,
                system=system_message,
                max_tokens=4096,
                temperature=temperature,
            )

        text_response = response.content[0].text

        chat_completion_response = ChatCompletionResponse()
        chat_completion_response.choices[0].message.content = text_response

        return chat_completion_response

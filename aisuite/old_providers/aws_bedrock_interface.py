"""The interface to the Together API."""

import os
from urllib.request import urlopen
import json

from ..framework.provider_interface import ProviderInterface


def convert_messages_to_llama3_prompt(messages):
    """
    Convert a list of messages to a prompt in Llama 3 instruction format.

    Args:
    messages (list of dict): List of messages where each message is a dictionary
                            with 'role' ('system', 'user', 'assistant') and 'content'.

    Returns:
    str: Formatted prompt for Llama 3.
    """
    prompt = "<|begin_of_text|>"
    for message in messages:
        prompt += f"<|start_header_id|>{message['role']}<|end_header_id|>{message['content']}<|eot_id|>\n"

    prompt += "<|start_header_id|>assistant<|end_header_id|>"

    return prompt


class RecursiveNamespace:
    """
    Convert dictionaries to objects with attribute access, including nested dictionaries.
    This class is used to simulate the OpenAI chat.completions.create's return type, so
    response.choices[0].message.content works consistenly for AWS Bedrock's LLM return of a string.
    """

    def __init__(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                value = RecursiveNamespace(value)
            elif isinstance(value, list):
                value = [
                    RecursiveNamespace(item) if isinstance(item, dict) else item
                    for item in value
                ]
            setattr(self, key, value)

    @classmethod
    def from_dict(cls, data):
        return cls(data)

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, RecursiveNamespace):
                value = value.to_dict()
            elif isinstance(value, list):
                value = [
                    item.to_dict() if isinstance(item, RecursiveNamespace) else item
                    for item in value
                ]
            result[key] = value
        return result


class AWSBedrockInterface(ProviderInterface):
    """Implements the ProviderInterface for interacting with AWS Bedrock's APIs."""

    def __init__(self):
        """Set up the AWS Bedrock client using the AWS access key id and secret access key obtained from the user's environment."""
        import boto3

        self.aws_bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=os.getenv("AWS_REGION_NAME"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def chat_completion_create(self, messages=None, model=None, temperature=0):
        """Request chat completions from the AWS Bedrock API.

        Args:
        ----
            model (str): Identifies the specific provider/model to use.
            messages (list of dict): A list of message objects in chat history.
            temperature (float): The temperature to use in the completion.

        Returns:
        -------
            The API response with the completion result.

        """
        body = json.dumps(
            {
                "prompt": convert_messages_to_llama3_prompt(messages),
                "temperature": temperature,
            }
        )
        accept = "application/json"
        content_type = "application/json"
        response = self.aws_bedrock_client.invoke_model(
            body=body, modelId=model, accept=accept, contentType=content_type
        )
        response_body = json.loads(response.get("body").read())
        generation = response_body.get("generation")

        response_data = {
            "choices": [
                {
                    "message": {"content": generation},
                }
            ],
        }

        return RecursiveNamespace.from_dict(response_data)

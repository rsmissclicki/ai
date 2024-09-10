import boto3
from aisuite.provider import Provider, LLMError
from aisuite.framework import ChatCompletionResponse


# Used to call the AWS Bedrock converse API
# Converse API provides consistent API, that works with all Amazon Bedrock models that support messages.
# Eg: anthropic.claude-v2,
#     meta.llama3-70b-instruct-v1:0,
#     mistral.mixtral-8x7b-instruct-v0:1
# The model value can be a baseModelId or provisionedModelArn.
# Using a base model id gives on-demand throughput.
# Use CreateProvisionedModelThroughput API to get provisionedModelArn for higher throughput.
# https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html
class AWSBedrockProvider(Provider):
    def __init__(self, **config):
        """
        Initialize the AWS Bedrock provider with the given configuration.
        Pass the entire configuration dictionary to the Anthropic Bedrock client constructor.
        """
        # Anthropic Bedrock client will use the default AWS credential providers, such as
        # using ~/.aws/credentials or the "AWS_SECRET_ACCESS_KEY" and "AWS_ACCESS_KEY_ID" environment variables.
        # If region is not set, it will use a default to us-west-1 which can lead to error -
        #   "Could not connect to the endpoint URL"
        # It does not like parameters passed to the constructor.
        self.client = boto3.client("bedrock-runtime", region_name="us-west-2")
        # Maintain a list of Inference Parameters which Bedrock supports.
        # https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InferenceConfiguration.html
        self.inference_parameters = [
            "maxTokens",
            "temperature",
            "topP",
            "stopSequences",
        ]

    def normalize_response(self, response):
        """Normalize the response from the Bedrock API to match OpenAI's response format."""
        norm_response = ChatCompletionResponse()
        norm_response.choices[0].message.content = response["output"]["message"][
            "content"
        ][0]["text"]
        return norm_response

    def chat_completions_create(self, model, messages, **kwargs):
        # Any exception raised by Anthropic will be returned to the caller.
        # Maybe we should catch them and raise a custom LLMError.
        # https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html
        system_message = None
        if messages[0]["role"] == "system":
            system_message = [{"text": messages[0]["content"]}]
            messages = messages[1:]

        formatted_messages = []
        for message in messages:
            # QUIETLY Ignore any "system" messages except the first system message.
            if message["role"] != "system":
                formatted_messages.append(
                    {"role": message["role"], "content": [{"text": message["content"]}]}
                )

        # Maintain a list of Inference Parameters which Bedrock supports.
        # These fields need to be passed using inferenceConfig.
        # Rest all other fields are passed as additionalModelRequestFields.
        inference_config = {}
        additional_model_request_fields = {}

        # Iterate over the kwargs and separate the inference parameters and additional model request fields.
        for key, value in kwargs.items():
            if key in self.inference_parameters:
                inference_config[key] = value
            else:
                additional_model_request_fields[key] = value

        # Call the Bedrock Converse API.
        response = self.client.converse(
            modelId=model,  # baseModelId or provisionedModelArn
            messages=formatted_messages,
            system=system_message,
            inferenceConfig=inference_config,
            additionalModelRequestFields=additional_model_request_fields,
        )
        return self.normalize_response(response)

import unittest
from unittest.mock import patch
from aisuite import Client
from aisuite import ProviderNames


class TestClient(unittest.TestCase):

    @patch("aisuite.providers.openai_provider.OpenAIProvider.chat_completions_create")
    @patch(
        "aisuite.providers.aws_bedrock_provider.AWSBedrockProvider.chat_completions_create"
    )
    @patch("aisuite.providers.azure_provider.AzureProvider.chat_completions_create")
    @patch(
        "aisuite.providers.anthropic_provider.AnthropicProvider.chat_completions_create"
    )
    def test_client_chat_completions(
        self, mock_anthropic, mock_azure, mock_bedrock, mock_openai
    ):
        # Mock responses from providers
        mock_openai.return_value = "OpenAI Response"
        mock_bedrock.return_value = "AWS Bedrock Response"
        mock_azure.return_value = "Azure Response"
        mock_anthropic.return_value = "Anthropic Response"

        # Provider configurations
        provider_configs = {
            ProviderNames.OPENAI: {"api_key": "test_openai_api_key"},
            ProviderNames.AWS_BEDROCK: {
                "aws_access_key": "test_aws_access_key",
                "aws_secret_key": "test_aws_secret_key",
                "aws_session_token": "test_aws_session_token",
                "aws_region": "us-west-2",
            },
            ProviderNames.AZURE: {
                "api_key": "azure-api-key",
            },
        }

        # Initialize the client
        client = Client()
        client.configure(provider_configs)
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
        ]

        # Test OpenAI model
        open_ai_model = ProviderNames.OPENAI + ":" + "gpt-4o"
        openai_response = client.chat.completions.create(
            open_ai_model, messages=messages
        )
        self.assertEqual(openai_response, "OpenAI Response")
        mock_openai.assert_called_once()

        # Test AWS Bedrock model
        bedrock_model = ProviderNames.AWS_BEDROCK + ":" + "claude-v3"
        bedrock_response = client.chat.completions.create(
            bedrock_model, messages=messages
        )
        self.assertEqual(bedrock_response, "AWS Bedrock Response")
        mock_bedrock.assert_called_once()

        azure_model = ProviderNames.AZURE + ":" + "azure-model"
        azure_response = client.chat.completions.create(azure_model, messages=messages)
        self.assertEqual(azure_response, "Azure Response")
        mock_azure.assert_called_once()

        anthropic_model = ProviderNames.ANTHROPIC + ":" + "anthropic-model"
        anthropic_response = client.chat.completions.create(
            anthropic_model, messages=messages
        )
        self.assertEqual(anthropic_response, "Anthropic Response")
        mock_anthropic.assert_called_once()

        # Test that new instances of Completion are not created each time we make an inference call.
        compl_instance = client.chat.completions
        next_compl_instance = client.chat.completions
        assert compl_instance is next_compl_instance

    @patch("aisuite.providers.openai_provider.OpenAIProvider.chat_completions_create")
    def test_invalid_provider_in_client_config(self, mock_openai):
        # Testing an invalid provider name in the configuration
        invalid_provider_configs = {
            "INVALID_PROVIDER": {"api_key": "invalid_api_key"},
        }

        # Expect ValueError when initializing Client with invalid provider
        with self.assertRaises(ValueError) as context:
            client = Client(invalid_provider_configs)

        # Verify the error message
        self.assertIn(
            "Provider INVALID_PROVIDER is not a valid provider",
            str(context.exception),
        )

    @patch("aisuite.providers.openai_provider.OpenAIProvider.chat_completions_create")
    def test_invalid_model_format_in_create(self, mock_openai):
        # Valid provider configurations
        provider_configs = {
            ProviderNames.OPENAI: {"api_key": "test_openai_api_key"},
        }

        # Initialize the client with valid provider
        client = Client(provider_configs)
        client.configure(provider_configs)

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Tell me a joke."},
        ]

        # Invalid model format
        invalid_model = "invalidmodel"

        # Expect ValueError when calling create with invalid model format
        with self.assertRaises(ValueError) as context:
            client.chat.completions.create(invalid_model, messages=messages)

        # Verify the error message
        self.assertIn(
            "Invalid model format. Expected 'provider:model'", str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()

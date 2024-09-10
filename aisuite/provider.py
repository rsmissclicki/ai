from abc import ABC, abstractmethod
from enum import Enum
import importlib


class LLMError(Exception):
    """Custom exception for LLM errors."""

    def __init__(self, message):
        super().__init__(message)


class Provider(ABC):
    @abstractmethod
    def chat_completions_create(self, model, messages):
        """Abstract method for chat completion calls, to be implemented by each provider."""
        pass


class ProviderNames(str, Enum):
    OPENAI = "openai"
    AWS_BEDROCK = "aws-bedrock"
    ANTHROPIC = "anthropic"
    AZURE = "azure"


class ProviderFactory:
    """Factory to register and create provider instances based on keys."""

    _provider_info = {
        ProviderNames.OPENAI: ("aisuite.providers.openai_provider", "OpenAIProvider"),
        ProviderNames.AWS_BEDROCK: (
            "aisuite.providers.aws_bedrock_provider",
            "AWSBedrockProvider",
        ),
        ProviderNames.ANTHROPIC: (
            "aisuite.providers.anthropic_provider",
            "AnthropicProvider",
        ),
        ProviderNames.AZURE: ("aisuite.providers.azure_provider", "AzureProvider"),
    }

    @classmethod
    def create_provider(cls, provider_key, config):
        """Dynamically import and create an instance of a provider based on the provider key."""
        if not isinstance(provider_key, ProviderNames):
            raise ValueError(
                f"Provider {provider_key} is not a valid ProviderNames enum"
            )

        module_name, class_name = cls._get_provider_info(provider_key)
        if not module_name:
            raise ValueError(f"Provider {provider_key.value} is not supported")

        # Lazily load the module
        try:
            module = importlib.import_module(module_name)
        except ImportError as e:
            raise ImportError(f"Could not import module {module_name}: {str(e)}")

        # Instantiate the provider class
        provider_class = getattr(module, class_name)
        return provider_class(**config)

    @classmethod
    def _get_provider_info(cls, provider_key):
        """Return the module name and class name for a given provider key."""
        return cls._provider_info.get(provider_key, (None, None))

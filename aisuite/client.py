from .provider import ProviderFactory, ProviderNames


class Client:
    def __init__(self, provider_configs: dict = {}):
        """
        Initialize the client with provider configurations.
        Use the ProviderFactory to create provider instances.
        """
        self.providers = {}
        self.provider_configs = provider_configs
        for provider_key, config in provider_configs.items():
            # Check if the provider key is a valid ProviderNames enum
            if not isinstance(provider_key, ProviderNames):
                raise ValueError(
                    f"Provider {provider_key} is not a valid ProviderNames enum"
                )
            # Store the value of the enum in the providers dictionary
            self.providers[provider_key.value] = ProviderFactory.create_provider(
                provider_key, config
            )

        self._chat = None

    def configure(self, provider_configs: dict = None):
        """
        Configure the client with provider configurations.
        """
        if provider_configs is None:
            return

        self.provider_configs.update(provider_configs)

        for provider_key, config in self.provider_configs.items():
            if not isinstance(provider_key, ProviderNames):
                raise ValueError(
                    f"Provider {provider_key} is not a valid ProviderNames enum"
                )
            self.providers[provider_key.value] = ProviderFactory.create_provider(
                provider_key, config
            )

    @property
    def chat(self):
        """Return the chat API interface."""
        if not self._chat:
            self._chat = Chat(self)
        return self._chat


class Chat:
    def __init__(self, client: "Client"):
        self.client = client

    @property
    def completions(self):
        """Return the completions interface."""
        return Completions(self.client)


class Completions:
    def __init__(self, client: "Client"):
        self.client = client

    def create(self, model: str, messages: list, **kwargs):
        """
        Create chat completion based on the model, messages, and any extra arguments.
        """
        # Check that correct format is used
        if ":" not in model:
            raise ValueError(
                f"Invalid model format. Expected 'provider:model', got '{model}'"
            )

        # Extract the provider key from the model identifier, e.g., "aws-bedrock:model-name"
        provider_key, model_name = model.split(":", 1)

        if provider_key not in ProviderNames._value2member_map_:
            raise ValueError(
                f"Provider {provider_key} is not a valid ProviderNames enum"
            )

        if provider_key not in self.client.providers:
            config = {}
            if provider_key in self.client.provider_configs:
                config = self.client.provider_configs[provider_key]
            self.client.providers[provider_key] = ProviderFactory.create_provider(
                ProviderNames(provider_key), config
            )

        provider = self.client.providers.get(provider_key)
        if not provider:
            raise ValueError(f"Could not load provider for {provider_key}.")

        # Delegate the chat completion to the correct provider's implementation
        # Any additional arguments will be passed to the provider's implementation.
        # Eg: max_tokens, temperature, etc.
        return provider.chat_completions_create(model_name, messages, **kwargs)

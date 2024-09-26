# aisuite

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Simple, unified interface to multiple Generative AI providers.

`aisuite` is an tool designed for researchers who need to evaluate and compare the responses of
multiple LLMs through a standardized interface. Based on the OpenAI interface standard, `aisuite`
makes it easy to interact with the most popular LLMs and compare the results of their chat based
functionality, with support for more interfaces coming in the near future.

Currently supported providers are -
OpenAI, Anthropic, Azure, Google, AWS, Groq, Mistral, HuggingFace and Ollama.
Internally, aisuite uses either the HTTP endpoint or the SDK for making calls to the provider.

## Installation

This installs just the base package without installing any provider's SDK.

```shell
pip install aisuite
```

This installs anthropic along with anthropic
```shell
pip install aisuite[anthropic]
```

This installs all the provider specific libraries
```shell
pip install aisuite[all]
```

## Set up

This library provides a thin wrapper around python client libraries to interact with
various Generative AI providers allowing creators to seamlessly swap out or test responses
from a number of LLMs without changing their code.

To get started you will need the API Keys for the providers you intend to use. You also need to
install the provider specific library to use either separately or when installing aisuite.

The API Keys are expected to be in the host ENV and can be set manually or by using a tool such
as [`python-dotenv`](https://pypi.org/project/python-dotenv/) or [`direnv`](https://direnv.net/).

For example if you wanted to use Antrophic's Claude 3.5 Sonnet in addition to OpenAI's ChatGPT 4o
you would first need to set the API keys:

```shell
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

In your python code:

```python
import aisuite as ai
client = ai.Client()

models = ["openai:gpt-4o", "anthropic:claude-3-5-sonnet-20240620"]

messages = [
    {"role": "system", "content": "Respond in Pirate English."},
    {"role": "user", "content": "Tell me a joke."},
]

for model in models:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.75
    )
    print(response.choices[0].message.content)

```
Note that the model name in the create() call needs to be replaced with `<provider>:<model-name>`
aisuite will call the appropriate provider with the right parameters based on the provider value.

For more examples, check out the `examples` directory where you will find several
notebooks that you can run to experiment with the interface.

## License

aisuite is released under the MIT License. You are free to use, modify, and distribute
the code for both commercial and non-commercial purposes.

## Contributing

If you would like to contribute, please read our [Contributing Guide](CONTRIBUTING.md)



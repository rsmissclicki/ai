# Snowflake

To use Snowflake with `aisuite`, you’ll need an [Snowflake Account](https://signup.snowflake.com/). Once your account is set up, you should follow the [Authorization & Authentication sections](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-llm-rest-api#setting-up-authentication) of the Snowflake documentation. This will walk you through the process of creating a Snowflake user that can access the Cortex REST API. Follow these instructions through creating a Snowflake JWT Token. Export the token and your Snowflake account identifier as environment variables:


```shell
export SNOWFLAKE_JWT_TOKEN="your-snowflake-jwt"
export SNOWFLAKE_ACCOUNT_IDENTIFIER="your-snowflake-account-identifier"
```

## Create a Chat Completion

Install the `httpx` Python client:

Example with pip:
```shell
pip install httpx
```

Example with poetry:
```shell
poetry add httpx
```

In your code:

> [List of available models](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-llm-rest-api#required-json-arguments) in Snowflake Cortex

```python
import aisuite as ai
client = ai.Client()

provider = "snowflake"
model_id = "llama3.1-8b"

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What’s the weather like in San Francisco?"},
]

response = client.chat.completions.create(
    model=f"{provider}:{model_id}",
    messages=messages,
)

print(response.choices[0].message.content)
```

Happy coding! If you’d like to contribute, please read our [Contributing Guide](CONTRIBUTING.md).

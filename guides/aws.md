# AWS

To use AWS Bedrock with `aisuite` you will need to create an AWS account and
navigate to https://console.aws.amazon.com/bedrock/home. This route
will be redirected to your default region. In this example the region has been set to
`us-west-2`. Anywhere the region is specified can be replaced with your desired region.

Navigate to the [overview](https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/overview) page
directly or by clicking on the `Get started` link.

## Foundation Model Access

You will first need to give your AWS account access to the foundation models by
visiting the [modelaccess](https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/modelaccess)
page to enable the models you would like to use. 

After enabling the foundation models, navigate to [providers page](https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/providers) 
and select the provider of the model you would like to use. From this page select the specific model you would like to use and 
make note of the `Model ID` (currently located near the bottom) this will be used when using the chat completion example below.

Once that has been enabled set your Access Key and Secret in the env variables:

```shell
export AWS_ACCESS_KEY="your-access-key"
export AWS_SECRET_KEY="your-secret-key"
export AWS_REGION_NAME="region-name" 
```
*Note: AWS_REGION_NAME is optional, a default of `us-west-2` has been set for easy of use*
*Note: For AWS_REGION_NAME, you can specify multiple regions using forward slash as separator (e.g. "us-east-1/us-west-2"). When the quota limit is reached in one region, the system will automatically rotate to the next available region.*

## Multi-Region Support

The library supports multi-region failover capabilities. When configuring AWS_REGION_NAME, you can specify multiple regions with forward slashes:

```shell
# Example of multi-region configuration
export AWS_REGION_NAME="us-east-1/us-west-2/ap-southeast-1"
```

When using this configuration:
- The system will attempt to use the first region (us-east-1) by default
- If quota limits are reached in the current region, it will automatically rotate to the next region in the list
- This rotation continues until a successful request is made or all regions are exhausted
- The rotation is handled transparently to your application code

## Create a Chat Completion

Install the boto3 client using your package installer

Example with pip
```shell
pip install boto3
```

Example with poetry
```shell
poetry add boto3
```

In your code:
```python
import aisuite as ai
client = ai.Client()

provider = "aws"
model_id = "meta.llama3-1-405b-instruct-v1:0" # Model ID from above

messages = [
    {"role": "system", "content": "Respond in Pirate English."},
    {"role": "user", "content": "Tell me a joke."},
]

response = client.chat.completions.create(
    model=f"{provider}:{model_id}",
    messages=messages,
)

print(response.choices[0].message.content)
```

Happy coding! If you would like to contribute, please read our [Contributing Guide](CONTRIBUTING.md).

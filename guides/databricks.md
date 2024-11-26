# Databricks Model Serving

To use Databricks Model Serving with the `aisuite` library, you'll first need to create a Google Cloud account and set up your environment to work with Google Cloud.

## Create a Databricks Workspace

A workspace is a Databricks deployment in a cloud service account. It provides a unified environment for working with Databricks assets for a specified set of users.

You can create a Databricks worksapce in your preferred cloud provider; please read more at the documentation listed here: 
- [Databricks Documentation - AWS](https://docs.databricks.com/en/index.html)
- [Azure Databricks Documentation - Azure](https://learn.microsoft.com/en-us/azure/databricks/) 
- [Databricks Documentation - Google Cloud](https://docs.gcp.databricks.com/en/index.html)

## Authentication Options
### Option 1: Personal Access Token

To create a Databricks personal access token for your Databricks workspace user, do the following:

1. In your Databricks workspace, click your Databricks username in the top bar, and then select Settings from the drop down.
2. Click Developer.
3. Next to Access tokens, click Manage.
4. Click Generate new token.
5. (Optional) Enter a comment that helps you to identify this token in the future, and change the token’s default lifetime of 90 days. To create a token with no lifetime (not recommended), leave the Lifetime (days) box empty (blank).
6. Click Generate.
7. Copy the displayed token to a secure location, and then click Done.

[Reference Documentation - AWS](https://docs.databricks.com/en/dev-tools/auth/pat.html)  
[Reference Documentation - Azure](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/auth/pat)  
[Reference Documentation - Google Cloud](https://docs.gcp.databricks.com/en/dev-tools/auth/pat.html)

Add it to your environment as follows: 

```shell
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="your-access-token"
```

### Option 2: Service Principal Authentication (recommended)

To create a service principal in Databricks, you must be an Account admin or a workspace admin. This step describes creating a service principal in a workspace. To use the account console, see [Manage service principals in your account](https://docs.databricks.com/en/admin/users-groups/service-principals.html#add-sp-account).

1. As a workspace admin, log in to the Databricks workspace.
2. Click your username in the top bar of the Databricks workspace and select Settings.
3. Click on the Identity and access tab.
4. Next to Service principals, click Manage.
5. Click Add service principal.
6. Click the drop-down arrow in the search box and then click Add new.
7. Enter a name for the service principal.
8. Click Add.

The service principal is added to both your workspace and the Databricks account.

Before you can use OAuth to authenticate to Databricks, you must first create an OAuth secret, which can be used to generate OAuth access tokens. 

1. On your service principal’s details page click the Secrets tab.
2. Under OAuth secrets, click Generate secret.
3. Copy the displayed Secret and Client ID, and then click Done.

The secret will only be revealed once during creation. The client ID is the same as the service principal’s application ID.

[Reference Documentation - AWS](https://docs.databricks.com/en/dev-tools/auth/oauth-m2m.html)
[Reference Documentation - Azure](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/auth/oauth-m2m) 
[Reference Documentation - Google Cloud](https://docs.gcp.databricks.com/en/dev-tools/auth/oauth-m2m.html)

Add it to your environment as follows: 

```shell
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_CLIENT_ID="your-client-id"
export DATABRICKS_CLIENT_SECRET="your-client-secret"
```

## Create a Chat Completion

Sample code:
```python
import aisuite as ai
client = ai.Client()

models = ["databricks:databricks-dbrx-instruct"]

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

import os
import json
import httpx
import google.auth
from google.auth.transport.requests import Request
from aisuite.provider import Provider
from aisuite.framework import ChatCompletionResponse


class GoogleHttpProvider(Provider):
    def __init__(self, **config):
        """
        Initializes the GoogleHttpProvider for Gemini.
        Checks for either the GCLOUD_APPLICATION_CREDENTIALS environment variable or the GCLOUD_ACCESS_TOKEN environment variable.
        Also checks for the ENDPOINT, REGION, and PROJECT_ID values from either config or environment variables.
        """
        # Check for GCLOUD_ACCESS_TOKEN environment variable.
        # Run `gcloud auth print-access-token` to set this value. Not recommended for production deployment scenarios.
        self.access_token = os.environ.get("GCLOUD_ACCESS_TOKEN")
        self.project_id = ""

        # If no manual token is provided, use google-auth for credentials
        if not self.access_token:
            if "GCLOUD_APPLICATION_CREDENTIALS" not in os.environ:
                raise EnvironmentError(
                    "Neither 'GCLOUD_ACCESS_TOKEN' nor 'GCLOUD_APPLICATION_CREDENTIALS' is set. "
                    "Please set 'GCLOUD_ACCESS_TOKEN' by running 'gcloud auth print-access-token' or "
                    "set 'GCLOUD_APPLICATION_CREDENTIALS' to the path of your service account JSON key file."
                )

            # Load default credentials and project information from google-auth
            self.credentials, self.project_id = google.auth.default()

            # Refresh credentials to get the access token
            self.credentials.refresh(Request())
            self.access_token = self.credentials.token

        # Set region, and project_id from config or environment variables
        self.region = config.get("region", os.environ.get("GOOGLE_REGION"))
        self.project_id = config.get(
            "project_id", os.environ.get("GOOGLE_PROJECT_ID", self.project_id)
        )

        # Validate that all required values are present
        if not self.region:
            raise ValueError(
                "Missing 'region'. Please set the 'REGION' environment variable or provide it in the config."
            )
        if not self.project_id:
            raise ValueError(
                "Missing 'project_id'. Please set the 'PROJECT_ID' environment variable or provide it in the config."
            )

    def chat_completions_create(self, model, messages, **kwargs):
        """
        Creates chat completions by sending a request to the Google Cloud API for Gemini.
        Adapts the message structure to match Gemini's input format.
        """
        url = f"https://{self.region}-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/{self.region}/publishers/google/models/{model}:generateContent"

        contents = []
        for message in messages:
            role = message["role"]
            if role == "system":
                role = "user"  # Gemini doesn't have a system role, map it to user
            elif role == "assistant":
                role = "model"  # Convert assistant to model

            contents.append({"role": role, "parts": [{"text": message["content"]}]})

        data = {"contents": contents, **kwargs}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        try:
            with httpx.Client() as client:
                resp = client.post(url, json=data, headers=headers, timeout=None)

                # Raise for any HTTP error status
                resp.raise_for_status()

                # Parse the JSON response
                resp_json = resp.json()

                # Create the single choice with the concatenated message
                completion_response = ChatCompletionResponse()
                completion_response.choices[0].message.content = resp_json[
                    "candidates"
                ][0]["content"]["parts"][0]["text"]

                return completion_response

        except httpx.HTTPStatusError as e:
            # Handle non-2xx HTTP status codes
            error_message = f"Request failed with status code {e.response.status_code}: {e.response.text}"
            raise Exception(error_message)

        except httpx.RequestError as e:
            # Handle connection-related errors
            error_message = (
                f"An error occurred while requesting {e.request.url!r}: {str(e)}"
            )
            raise Exception(error_message)

        except json.JSONDecodeError as e:
            # Handle issues with parsing the response
            error_message = "Failed to parse JSON response: " + str(e)
            raise Exception(error_message)

        except Exception as e:
            # Catch-all for any other exceptions
            error_message = f"An unexpected error occurred: {str(e)}"
            raise Exception(error_message)

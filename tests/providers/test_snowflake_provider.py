import pytest
from unittest.mock import patch, MagicMock
from aisuite.providers.snowflake_provider import SnowflakeProvider
from aisuite.framework import ChatCompletionResponse


@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    """Fixture to set environment variables for tests."""
    monkeypatch.setenv("SNOWFLAKE_JWT_TOKEN", "test-jwt-token")
    monkeypatch.setenv("SNOWFLAKE_ACCOUNT_IDENTIFIER", "test-account-id")


def test_missing_env_vars():
    """Test that an error is raised if required environment variables are missing."""
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(ValueError) as exc_info:
            SnowflakeProvider()
        assert "Snowflake JWT Bearer Token is missing" in str(exc_info.value)


def test_chat_completions_create():
    """Test that chat completions are requested successfully."""

    user_greeting = "Hello!"
    message_history = [{"role": "user", "content": user_greeting}]
    selected_model = "our-favorite-model"
    response_text_content = "mocked-text-response-from-model"

    provider = SnowflakeProvider()
    mock_response_data = {"choices": [{"delta": {"content": response_text_content}}]}

    with patch(
        "httpx.post",
        return_value=MagicMock(status_code=200, json=lambda: mock_response_data),
    ) as mock_post:
        response = provider.chat_completions_create(
            model=selected_model,
            messages=message_history,
            temperature=0.75,
            top_p=0.9,
            max_tokens=1234,
        )

        mock_post.assert_called_once_with(
            "https://test-account-id.snowflakecomputing.com/api/v2/cortex/inference:complete",
            json={
                "model": selected_model,
                "messages": message_history,
                "temperature": 0.75,
                "top_p": 0.9,
                "max_tokens": 1234,
            },
            headers=provider.headers,
            timeout=30,
        )

        assert isinstance(response, ChatCompletionResponse)
        assert response.choices[0].message.content == response_text_content

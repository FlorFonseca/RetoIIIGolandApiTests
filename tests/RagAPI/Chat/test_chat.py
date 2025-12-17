import requests
import pytest
from unittest.mock import patch
from mock_chat_api import MockChatAPI

BASE_CHAT_ENDPOINT = "/chat"

# Fixture de mock para RAG / Chat API

@pytest.fixture(autouse=True)
def mock_chat_api(use_mock):
    """
    Aplica el mock de Chat API para todos los tests de este módulo.
    """
    if use_mock:
        mock_api = MockChatAPI()
        with patch("requests.post", side_effect=mock_api.post):
            yield
    else:
        yield

# TESTS Chat (POST /chat/:session)

def test_post_message_success(url):
    request_body = {
        "threadId": "t-123",
        "runId": "r-456",
        "messages": [
            {"role": "user", "content": "Hola"}
        ],
        "tools": [],
        "context": [],
        "forwardedProps": {},
        "state": {}
    }

    response = requests.post(
        f"{url}{BASE_CHAT_ENDPOINT}/session",
        json=request_body,
        stream=True
    )

    body = response.json()

    assert response.status_code == 200
    assert "data" in body
    assert body["data"]["type"] == "RUN_FINISHED"
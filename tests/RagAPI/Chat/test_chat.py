import requests
import pytest

BASE_CHAT_ENDPOINT = "/chat"

# TESTS Chat (POST /chat/:session)

def test_01_post_message_success(url):
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
        json=request_body
    )

    body = response.json()

    assert response.status_code == 200
    assert "events" in body
    assert body["events"][-1]["data"]["type"] == "RUN_FINISHED"

def test_02_chat_event_order(url):
    payload = {
        "threadId": "t-1",
        "runId": "r-1",
        "messages": [{"role": "user", "content": "Hola"}],
        "tools": [],
        "context": [],
        "forwardedProps": {},
        "state": {}
    }

    r = requests.post(f"{url}{BASE_CHAT_ENDPOINT}/session", json=payload)
    events = r.json()["events"]

    types = [e["data"]["type"] for e in events]

    assert types == [
        "RUN_STARTED",
        "TEXT_MESSAGE_START",
        "TEXT_MESSAGE_CONTENT",
        "TEXT_MESSAGE_END",
        "RUN_FINISHED"
    ]

def test_03_chat_missing_field(url):
    payload = {
        "threadId": "t-123",
        "runId": "r-456",
        # messages falta
        "tools": [],
        "context": [],
        "forwardedProps": {},
        "state": {}
    }

    r = requests.post(f"{url}{BASE_CHAT_ENDPOINT}/session", json=payload)

    assert r.status_code == 422
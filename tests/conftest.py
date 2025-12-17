import pytest
import requests

from DocsAPI.mock_docs_api import MockDocsAPI
from ProcessAPI.mock_process_api import MockProcessAPI
from RagAPI.Chat.mock_chat_api import MockChatAPI

USE_MOCK = True # Define si va contra mocks o contra la API real
REAL_URL = "http://localhost:8000/api"


@pytest.fixture(scope="session")
def use_mock():
    return USE_MOCK


@pytest.fixture(scope="session")
def base_url(use_mock):
    return REAL_URL if not use_mock else "http://mock"


@pytest.fixture(scope="session")
def url(base_url):
    return base_url


@pytest.fixture(autouse=True)
def mock_requests(monkeypatch, use_mock):
    """
    Intercepta requests.get / post / delete cuando USE_MOCK=True
    """
    if not use_mock:
        return

    docs_api = MockDocsAPI()
    process_api = MockProcessAPI()
    chat_api = MockChatAPI()

    def mock_get(url, **kwargs):
        if "/get_docs" in url or "/get_single_doc" in url or "/get/" in url:
            return docs_api.get(url, **kwargs)
        if "/post/" in url:
            return process_api.get(url, **kwargs)
        return requests.Response()

    def mock_post(url, **kwargs):
        if "/create_doc" in url:
            return docs_api.post(url, **kwargs)
        if "/chat" in url:
            return chat_api.post(url, **kwargs)
        return requests.Response()

    def mock_delete(url, **kwargs):
        if "/delete_doc" in url:
            return docs_api.delete(url, **kwargs)
        return requests.Response()

    # Reemplaza cada request por la del mock
    monkeypatch.setattr(requests, "get", mock_get)
    monkeypatch.setattr(requests, "post", mock_post)
    monkeypatch.setattr(requests, "delete", mock_delete)
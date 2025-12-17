import pytest
from unittest.mock import patch
from mock_server import MockDocsAPI

USE_MOCK = True
REAL_URL = "http://localhost:8000/api"
mock_api = MockDocsAPI()

@pytest.fixture(autouse=True)
def setup_mock():
    if USE_MOCK:
        with patch('requests.get', side_effect=mock_api.get), \
             patch('requests.post', side_effect=mock_api.post), \
             patch('requests.delete', side_effect=mock_api.delete):
            yield
    else:
        yield

def pytest_configure(config):
    print(f"\n{'='*60}")
    print(f"Modo de testing: {'MOCK' if USE_MOCK else 'API REAL'}")
    if not USE_MOCK:
        print(f"URL: {REAL_URL}")
    print(f"{'='*60}\n")

@pytest.fixture
def url():
    return "" if USE_MOCK else REAL_URL

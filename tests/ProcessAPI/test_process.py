import requests
import pytest
from unittest.mock import patch
from mock_process_api import MockProcessAPI

BASE_PROCESS_ENDPOINT = "/post"

# Fixture: mock de Process API

@pytest.fixture(autouse=True)
def mock_process_api(use_mock):
    if use_mock:
        mock_api = MockProcessAPI()
        with patch("requests.get", side_effect=mock_api.get):
            yield
    else:
        yield

# TESTS ProcessDoc

def test_process_doc_success(url):
    response = requests.get(f"{url}{BASE_PROCESS_ENDPOINT}/123")

    assert response.status_code == 200
    assert response.json()["result"] is True


def test_process_doc_invalid_id(url):
    response = requests.get(f"{url}{BASE_PROCESS_ENDPOINT}/abc")

    assert response.status_code == 400
    assert response.json()["result"] == "Error"


def test_process_doc_not_found(url):
    response = requests.get(f"{url}/invalid_endpoint/123")

    assert response.status_code == 404
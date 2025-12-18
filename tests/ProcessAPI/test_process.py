import requests
import pytest

BASE_PROCESS_ENDPOINT = "/post"

# TESTS ProcessDoc

def test_01_process_doc_success(url):
    response = requests.get(f"{url}{BASE_PROCESS_ENDPOINT}/123")

    assert response.status_code == 200
    assert response.json()["result"] is True

def test_02_process_doc_invalid_id(url):
    response = requests.get(f"{url}{BASE_PROCESS_ENDPOINT}/abc")

    assert response.status_code == 400
    assert response.json()["result"] == "Error"

def test_03_process_doc_not_found(url):
    response = requests.get(f"{url}/invalid_endpoint/123")

    assert response.status_code == 404
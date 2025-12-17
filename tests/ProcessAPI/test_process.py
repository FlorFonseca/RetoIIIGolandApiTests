import requests
from unittest.mock import patch, Mock

BASE_PROCESS_ENDPOINT = "/post"

# ProcessDoc (GET /post/:iddoc)

@patch("requests.get")
def test_process_doc_success(mock_get):
    mock_get.return_value = Mock(
        status_code=200,
        json=lambda: {"result": True}
    )

    response = requests.get(f"{BASE_PROCESS_ENDPOINT}/123")

    assert response.status_code == 200
    assert response.json()["result"] is True


@patch("requests.get")
def test_process_doc_error(mock_get):
    mock_get.return_value = Mock(
        status_code=500,
        json=lambda: {"result": "Error"}
    )

    response = requests.get(f"{BASE_PROCESS_ENDPOINT}/123")

    assert response.status_code == 500
    assert response.json()["result"] == "Error"


@patch("requests.get")
def test_process_doc_invalid_id(mock_get):
    mock_get.return_value = Mock(
        status_code=400,
        json=lambda: {"result": "Error"}
    )

    response = requests.get(f"{BASE_PROCESS_ENDPOINT}/abc")

    assert response.status_code == 400
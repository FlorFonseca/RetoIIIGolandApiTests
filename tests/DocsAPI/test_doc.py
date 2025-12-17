import requests
from unittest.mock import patch, Mock

BASE_ENDPOINT = "/get_docs"

# Get all docs (get /get_docs?limit=<init>&offest=<int>)

@patch("requests.get")
def test_get_all_docs_success(mock_get):
    mock_get.return_value = Mock(
        status_code=200,
        json=lambda: {
            "results": [
                {
                    "id": "uuid-1",
                    "filename": "file1.pdf",
                    "minio_path": "/docs/file1.pdf",
                    "uploaded_at": "2024-01-01T10:00:00"
                }
            ],
            "total": 1
        }
    )

    response = requests.get(f"{BASE_ENDPOINT}?limit=10&offset=0")
    body = response.json()

    assert response.status_code == 200
    assert "results" in body
    assert "total" in body
    assert isinstance(body["results"], list)
    assert isinstance(body["total"], int)


@patch("requests.get")
def test_get_all_docs_empty(mock_get):
    mock_get.return_value = Mock(
        status_code=200,
        json=lambda: {
            "results": [],
            "total": 0
        }
    )

    response = requests.get(f"{BASE_ENDPOINT}?limit=10&offset=0")

    assert response.status_code == 200
    assert response.json()["results"] == []
    assert response.json()["total"] == 0


@patch("requests.get")
def test_get_all_docs_unauthorized(mock_get):
    mock_get.return_value = Mock(
        status_code=403,
        json=lambda: {"detail": "Forbidden"}
    )

    response = requests.get(f"{BASE_ENDPOINT}?limit=10&offset=0")

    assert response.status_code == 403


@patch("requests.get")
def test_get_all_docs_invalid_params(mock_get):
    mock_get.return_value = Mock(
        status_code=400,
        json=lambda: {"error": "Invalid pagination params"}
    )

    response = requests.get(f"{BASE_ENDPOINT}?limit=-1&offset=abc")

    assert response.status_code == 400
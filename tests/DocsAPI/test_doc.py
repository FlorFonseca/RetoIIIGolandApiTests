# Para correr y crear el archivo html: pytest --html=report.html --self-contained-html

import pytest
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


# TESTS Get single doc

def test_01_get_single_doc_ok(url):
    doc_id = "123e4567-e89b-12d3-a456-426614174000"

    r = requests.get(f'{url}/get_single_doc/{doc_id}')
    assert r.status_code == 200
    body = r.json()

    assert "id" in body
    assert "filename" in body
    assert "minio_path" in body
    assert "uploaded_at" in body

    assert isinstance(body["id"], str)
    assert isinstance(body["filename"], str)
    assert isinstance(body["minio_path"], str)
    assert isinstance(body["uploaded_at"], str)

def test_02_get_single_doc_not_found(url):
    invalid_id = "00000000-0000-0000-0000-000000000000"

    r = requests.get(f"{url}/get_single_doc/{invalid_id}")

    assert r.status_code == 404

def test_03_get_single_doc_invalid_id_format(url):
    invalid_id = "prueba-de-api-en-docs"

    r = requests.get(f"{url}/get_single_doc/{invalid_id}")

    assert r.status_code in (400, 422)

def test_04_get_single_doc_id_matches_request(url):
    doc_id = "123e4567-e89b-12d3-a456-426614174000"

    r = requests.get(f"{url}/get_single_doc/{doc_id}")
    assert r.status_code == 200

    body = r.json()
    assert body["id"] == doc_id

def test_05_get_single_doc_body_not_empty(url):
    doc_id = "123e4567-e89b-12d3-a456-426614174000"

    r = requests.get(f"{url}/get_single_doc/{doc_id}")

    assert r.json() != {}

# TESTS Get PDF 

# TESTS Create doc

def test_06_post_create_doc_ok(url):
    files = {
        "content": ("test.pdf", b"%PDF-1.4 pdf content", "application/pdf")
    }
    data = {
        "filename": "test.pdf"
    }

    r = requests.post(f"{url}/create_doc/", data=data, files=files)

    assert r.status_code == 200

    body = r.json()

    required_fields = ["id", "filename", "minio_path", "uploaded_at", "result"]
    for field in required_fields:
        assert field in body

    assert body["result"] is True
    assert body["filename"] == "test.pdf"

def test_07_post_create_doc_invalid_file_type(url): 
    files = {
        "content": ("test.txt", b"not a pdf", "text/plain")
    }
    data = {
        "filename": "test.txt"
    }   

    r = requests.post(f"{url}/create_doc/", data=data, files=files)

    assert r.status_code in (400, 415)

def test_08_post_create_doc_missing_file(url):
    data = {
        "filename": "test.pdf"
    }

    r = requests.post(f"{url}/create_doc/", data=data)

tests/DocsAPI/test_doc.py
    assert r.status_code in (400, 422)

def test_09_post_create_doc_missing_filename(url):
    files = {
        "content": ("test.pdf", b"%PDF-1.4 pdf", "application/pdf")
    }

    r = requests.post(f"{url}/create_doc/", files=files)

    assert r.status_code in (400, 422)

def test_10_post_create_doc_filename_consistency(url):
    files = {
        "content": ("doc.pdf", b"%PDF-1.4 pdf", "application/pdf")
    }
    data = {
        "filename": "doc.pdf"
    }

    r = requests.post(f"{url}/create_doc/", data=data, files=files)

    body = r.json()
    assert body["filename"] == "doc.pdf"
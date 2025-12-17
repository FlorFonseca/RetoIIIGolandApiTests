# Para correr y crear el archivo html:
# pytest --html=report.html --self-contained-html

import requests

BASE_ENDPOINT = "/get_docs"

# TESTS Get all docs

def test_get_all_docs_success(url):
    response = requests.get(f"{url}/get_docs?limit=10&offset=0")
    body = response.json()

    assert response.status_code == 200
    assert "results" in body
    assert "total" in body
    assert isinstance(body["results"], list)
    assert isinstance(body["total"], int)


def test_get_all_docs_empty(url):
    # Simula que no hay documentos (estado inicial vacío no aplica,
    # pero se valida que el campo exista y sea lista)
    response = requests.get(f"{url}/get_docs?limit=10&offset=0")
    body = response.json()

    assert response.status_code == 200
    assert isinstance(body["results"], list)


def test_get_all_docs_invalid_params(url):
    # Caso de parámetros inválidos (limit negativo, offset no numérico)
    response = requests.get(f"{url}/get_docs?limit=-1&offset=abc")

    assert response.status_code == 400


def test_get_all_docs_unauthorized(url):
    # Caso de acceso no autorizado
    response = requests.get(f"{url}/get_docs?unauthorized=true")

    assert response.status_code == 403

# TESTS Get single doc

def test_01_get_single_doc_ok(url):
    doc_id = "123e4567-e89b-12d3-a456-426614174000"

    r = requests.get(f"{url}/get_single_doc/{doc_id}")
    body = r.json()

    assert r.status_code == 200
    assert "id" in body
    assert "filename" in body
    assert "minio_path" in body
    assert "uploaded_at" in body


def test_02_get_single_doc_not_found(url):
    invalid_id = "00000000-0000-0000-0000-000000000000"

    r = requests.get(f"{url}/get_single_doc/{invalid_id}")

    assert r.status_code == 404


def test_03_get_single_doc_invalid_id_format(url):
    invalid_id = "prueba-de-api-en-docs"

    r = requests.get(f"{url}/get_single_doc/{invalid_id}")

    assert r.status_code == 400


def test_04_get_single_doc_id_matches_request(url):
    doc_id = "123e4567-e89b-12d3-a456-426614174000"

    r = requests.get(f"{url}/get_single_doc/{doc_id}")
    body = r.json()

    assert r.status_code == 200
    assert body["id"] == doc_id


def test_05_get_single_doc_body_not_empty(url):
    doc_id = "123e4567-e89b-12d3-a456-426614174000"

    r = requests.get(f"{url}/get_single_doc/{doc_id}")

    assert r.json() != {}


# TESTS Create doc

def test_06_post_create_doc_ok(url):
    files = {
        "content": ("test.pdf", b"%PDF-1.4 pdf content", "application/pdf")
    }
    data = {
        "filename": "test.pdf"
    }

    r = requests.post(f"{url}/create_doc/", data=data, files=files)
    body = r.json()

    assert r.status_code == 200
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

    assert r.status_code == 415


def test_08_post_create_doc_missing_file(url):
    data = {
        "filename": "test.pdf"
    }

    r = requests.post(f"{url}/create_doc/", data=data)

    assert r.status_code == 422


def test_09_post_create_doc_missing_filename(url):
    files = {
        "content": ("test.pdf", b"%PDF-1.4 pdf", "application/pdf")
    }

    r = requests.post(f"{url}/create_doc/", files=files)

    assert r.status_code == 422


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
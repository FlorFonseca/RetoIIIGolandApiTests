from unittest.mock import Mock

class MockProcessAPI:
    """
    Mock server que simula la Process API.
    """

    def get(self, url, **kwargs):
        response = Mock()

        # GET /post/{iddoc}
        if "/post/" in url:
            doc_id = url.split("/post/")[1]

            # ID válido
            if doc_id.isdigit():
                response.status_code = 200
                response.json.return_value = {"result": True}
            else:
                response.status_code = 400
                response.json.return_value = {"result": "Error"}

            return response

        # Endpoint inexistente
        response.status_code = 404
        response.json.return_value = {"detail": "Endpoint not found"}
        return response

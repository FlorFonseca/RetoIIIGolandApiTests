from unittest.mock import Mock


class MockChatAPI:
    """
    Mock server que simula la RAG / Chat API.
    """

    def post(self, url, **kwargs):
        response = Mock()

        # POST /chat/:session
        if "/chat/" in url:
            response.status_code = 200

            # Simulación del flujo completo del chatbot
            response.json.return_value = {
                "data": {
                    "type": "RUN_FINISHED",
                    "threadId": "t-123",
                    "runId": "r-456"
                }
            }
            return response

        # Endpoint inexistente
        response.status_code = 404
        response.json.return_value = {"detail": "Endpoint not found"}
        return response
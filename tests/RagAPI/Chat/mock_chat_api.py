from unittest.mock import Mock
import uuid

class MockChatAPI:
    """
    Mock server que simula la RAG / Chat API con eventos.
    """

    def post(self, url, **kwargs):
        response = Mock()

        if "/chat/" not in url:
            response.status_code = 404
            response.json.return_value = {"detail": "Endpoint not found"}
            return response

        body = kwargs.get("json", {})

        # Validaciones básicas del input
        required_fields = [
            "threadId", "runId", "messages",
            "tools", "context", "forwardedProps", "state"
        ]

        for field in required_fields:
            if field not in body:
                response.status_code = 422
                response.json.return_value = {"detail": f"Missing field {field}"}
                return response

        message_id = str(uuid.uuid4())

        # Simulación del flujo completo del chat
        response.status_code = 200
        response.json.return_value = {
            "events": [
                {"data": {"type": "RUN_STARTED", "threadId": body["threadId"], "runId": body["runId"]}},
                {"data": {"type": "TEXT_MESSAGE_START", "messageId": message_id, "role": "assistant"}},
                {"data": {"type": "TEXT_MESSAGE_CONTENT", "messageId": message_id, "delta": "Hola"}},
                {"data": {"type": "TEXT_MESSAGE_END", "messageId": message_id}},
                {"data": {"type": "RUN_FINISHED", "threadId": body["threadId"], "runId": body["runId"]}},
            ]
        }

        return response

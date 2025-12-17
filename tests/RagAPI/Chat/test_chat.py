import unittest
from unittest.mock import patch, Mock
import requests

class TestChatEndpoints(unittest.TestCase):

    @patch('requests.post')
    def test_post_message(self, mock_post_data):
        request = {
            "threadId": "t-123",
            "runId": "r-456",
            "messages": [
                {"role": "user", "content": "Hola"}
            ],
            "tools": [],
            "context": [],
            "forwardedProps": {},
            "state": {}
        }

        mock_post_data = Mock()
        mock_post_data.status_code = 200

        body = {
                    "data": {"type": "RUN_STARTED", "threadId": "t-123", "runId": "r-456"},

                    "data": {
                        "type": "TEXT_MESSAGE_START", "messageId": "m-1", "role": "assistant"},

                    "data": {"type": "TEXT_MESSAGE_CONTENT", "messageId": "m-1", "delta": "Hola"},

                    "data": {"type": "TEXT_MESSAGE_END", "messageId": "m-1"},

                    "data": {"type": "RUN_FINISHED", "threadId": "t-123", "runId": "r-456"},
        }

        mock_post_data.return_value = body
        # llamada al endpoint (mockeada, no nos va a importar)
        response = requests.post("http://fake/chat/session", json=request, stream=True)

        print(response.status_code)

        self.assertEqual(mock_post_data.status_code,200)

        self.assertEqual(mock_post_data.return_value["data"]["type"], "RUN_FINISHED")
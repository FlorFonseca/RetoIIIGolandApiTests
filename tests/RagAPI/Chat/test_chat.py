import unittest
from unittest.mock import patch, Mock
import requests
import json

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

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {
            "Content-Type": "text/event-stream"
        }
        mock_response.iter_lines.return_value = [
            b'data: {"type":"RUN_STARTED","threadId":"t-123","runId":"r-456"}',
            b'data: {"type":"TEXT_MESSAGE_START","messageId":"m-1","role":"assistant"}',
            b'data: {"type":"TEXT_MESSAGE_CONTENT","messageId":"m-1","delta":"Hola"}',
            b'data: {"type":"TEXT_MESSAGE_END","messageId":"m-1"}',
            b'data: {"type":"RUN_FINISHED","threadId":"t-123","runId":"r-456"}',
        ]

        mock_post_data.return_value = mock_response

        # llamada al endpoint (mockeada, no nos va a importar)
        response = requests.post("http://fake/chat/session", json=request, stream=True)

        # consumo del stream
        events = []
        for line in response.iter_lines():
            payload = json.loads(line.replace(b"data:", b"").strip())
            events.append(payload)

        # asserts
        self.assertEqual(response.status_code, 200)
        self.assertEqual(events[0]["type"], "RUN_STARTED")
        self.assertEqual(events[-1]["type"], "RUN_FINISHED")
    
    # endpoint privado
    # @patch('request.get')
    # def test_history(self, mock_get_data):

import unittest
import requests

class ClientTests(unittest.TestCase):
    def test_when_request_sent_to_ping_get_back_pong_and_200(self):
        r = requests.get('http://localhost:19546/ping')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, 'pong')

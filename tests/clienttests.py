import unittest
import requests

class ClientTests(unittest.TestCase):
    def test_when_request_sent_to_ping_get_back_pong_and_200(self):
        r = requests.get('http://localhost:19546/ping')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, 'pong')

    def test_data_store_when_given_valid_data_returns_200(self):
        post_data = {'key': 'key123', 'value': 'value456'}
        r = requests.post('http://localhost:19546/datastore', data=post_data)
        self.assertEqual(r.status_code, 200)

    def test_data_store_when_not_given_key_returns_400(self):
        post_data = {'value': 'value456'}
        r = requests.post('http://localhost:19546/datastore', data=post_data)
        self.assertEqual(r.status_code, 400)

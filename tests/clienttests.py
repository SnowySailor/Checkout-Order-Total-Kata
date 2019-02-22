import unittest
import requests

def MakeClientTests(baseurl):
    class ClientTests(unittest.TestCase):
        # ping
        def test_when_request_sent_to_ping_get_back_pong_and_200(self):
            r = requests.get('http://localhost:19546/ping')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, 'pong')

        # datastore
        def test_post_data_store_when_given_valid_data_returns_200(self):
            post_data = {'key': 'key123', 'value': 'value456'}
            r = requests.post(baseurl + '/datastore', data=post_data)
            self.assertEqual(r.status_code, 200)

        def test_post_data_store_when_not_given_key_returns_400(self):
            post_data = {'value': 'value456'}
            r = requests.post(baseurl + '/datastore', data=post_data)
            self.assertEqual(r.status_code, 400)

        def test_post_data_store_when_not_given_value_returns_400(self):
            post_data = {'key': 'key123'}
            r = requests.post(baseurl + '/datastore', data=post_data)
            self.assertEqual(r.status_code, 400)

        def test_get_data_store_when_endpoint_is_datastore1_returns_404(self):
            r = requests.get(baseurl + '/datastore1/test')
            self.assertEqual(r.status_code, 404)

        def test_get_data_store_when_key_doesnt_exist_returns_null(self):
            r = requests.get(baseurl + '/datastore/doesnotexist')
            self.assertEqual(r.text, 'null')

        def test_get_data_store_when_key_does_exist_returns_value_associated_with_key(self):
            post_data = {'key': 'testingkey', 'value': 'testingvalue'}
            r = requests.post(baseurl + '/datastore', data=post_data)
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/datastore/testingkey')
            self.assertEqual(r.text, '"testingvalue"')

        def test_delete_data_store_when_key_does_not_exist_returns_200(self):
            r = requests.delete(baseurl + '/datastore/doesnotexist')
            self.assertEqual(r.status_code, 200)

        def test_delete_data_store_when_key_exists_it_is_deleted(self):
            post_data = {'key': 'testingkey123', 'value': 'testingvalue123'}
            r = requests.post(baseurl + '/datastore', data=post_data)
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/datastore/testingkey123')
            self.assertEqual(r.text, '"testingvalue123"')
            r = requests.delete(baseurl + '/datastore/testingkey123')
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/datastore/testingkey123')
            self.assertEqual(r.text, 'null')

    return ClientTests
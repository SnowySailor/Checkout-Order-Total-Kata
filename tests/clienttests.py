import unittest
import requests
import json
from src.helpers import get_value

def MakeClientTests(baseurl):
    class ClientTests(unittest.TestCase):
        # Webserver tests
        def test_when_http_get_to_undefined_route_returns_404(self):
            r = requests.get(baseurl + '/doesnotexist/')
            self.assertEqual(r.status_code, 404)

        def test_when_http_post_to_undefined_route_returns_404(self):
            r = requests.post(baseurl + '/doesnotexist/')
            self.assertEqual(r.status_code, 404)

        def test_when_http_delete_to_undefined_route_returns_404(self):
            r = requests.delete(baseurl + '/doesnotexist/')
            self.assertEqual(r.status_code, 404)

        # ping
        def test_when_request_sent_to_ping_get_back_pong_and_200(self):
            r = requests.get('http://localhost:19546/ping')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, 'pong')

        # datastore (in-memory database)
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

        # createitem
        def test_post_create_item_when_given_valid_data_returns_200(self):
            post_data = {'name': 'cherries', 'price': 1.00, 'billing_method': 'weight'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)

        def test_post_create_item_when_given_no_name_returns_400(self):
            post_data = {'price': 1.00, 'billing_method': 'weight'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 400)

        def test_post_create_item_when_given_no_price_returns_400(self):
            post_data = {'name': 'cherries', 'billing_method': 'weight'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 400)

        def test_post_create_item_when_given_no_billing_method_defaults_to_unit(self):
            post_data = {'name': 'cherries', 'price': 1.00}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/itemdetails?name=cherries')
            item = json.loads(r.text)
            self.assertEqual(get_value(item, 'billing_method'), 'unit')

        def test_post_create_item_when_item_already_exists_it_is_overwritten(self):
            first_item = {'name': 'cherries', 'price': 1.00, 'billing_method': 'weight'}
            second_item = {'name': 'cherries', 'price': 0.05, 'billing_method': 'unit'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(first_item))
            self.assertEqual(r.status_code, 200)
            r = requests.post(baseurl + '/createitem', data=json.dumps(second_item))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/itemdetails?name=cherries')
            item = json.loads(r.text)
            self.assertEqual(item, second_item)

        def test_get_create_item_returns_404(self):
            r = requests.get(baseurl + '/createitem')
            self.assertEqual(r.status_code, 404)

        # itemdetails
        def test_get_item_details_when_given_item_name_returns_200(self):
            post_data = {'name': 'milk', 'price': 1.50, 'billing_method': 'unit'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/itemdetails?name=milk')
            self.assertEqual(r.status_code, 200)

        def test_get_item_details_when_given_item_name_returns_item_details_json(self):
            post_data = {'name': 'milk', 'price': 1.50, 'billing_method': 'unit'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/itemdetails?name=milk')
            self.assertEqual(r.text, json.dumps(post_data))

        def test_get_item_details_when_given_no_name_returns_400(self):
            r = requests.get(baseurl + '/itemdetails')
            self.assertEqual(r.status_code, 400)

        def test_get_item_details_when_item_does_not_exist_return_400(self):
            r = requests.get(baseurl + '/itemdetails?name=doesnotexist')
            self.assertEqual(r.status_code, 400)

    return ClientTests

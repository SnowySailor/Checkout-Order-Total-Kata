import unittest
import requests
import json
import uuid
from src.helpers import get_value

def MakeCreateOrderTests(baseurl):
    class CreateOrderTests(unittest.TestCase):
        def setUp(self):
            self.order_id = str(uuid.uuid4())

        @classmethod
        def setUpClass(self):
            post_data = {'identifier': 'milk', 'price': 1.50, 'billing_method': 'unit'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))
            post_data = {'identifier': 'cheese', 'price': 5.75, 'billing_method': 'weight'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))

        def test_post_create_order_when_given_valid_data_returns_200(self):
            post_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)

        def test_post_create_order_when_not_given_id_returns_400(self):
            post_data = {}
            r = requests.post(baseurl + '/createorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 400)

        def test_post_create_order_when_order_exists_returns_400(self):
            first_order = {'id': self.order_id}
            second_order = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(first_order))
            self.assertEqual(r.status_code, 200)
            r = requests.post(baseurl + '/createorder', data=json.dumps(second_order))
            self.assertEqual(r.status_code, 400)

    return CreateOrderTests
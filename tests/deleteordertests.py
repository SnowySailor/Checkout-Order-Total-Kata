import unittest
import requests
import json
import uuid
from src.helpers import get_value

def MakeDeleteOrderTests(baseurl):
    class DeleteOrderTests(unittest.TestCase):
        def setUp(self):
            self.order_id = str(uuid.uuid4())

        @classmethod
        def setUpClass(self):
            post_data = {'name': 'milk', 'price': 1.50, 'billing_method': 'unit'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))
            post_data = {'name': 'cheese', 'price': 5.75, 'billing_method': 'weight'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))

        def test_delete_order_when_order_does_not_exist_returns_400(self):
            first_order = {'id': 'doesnotexist'}
            r = requests.delete(baseurl + '/deleteorder', data=json.dumps(first_order))
            self.assertEqual(r.status_code, 400)

    return DeleteOrderTests
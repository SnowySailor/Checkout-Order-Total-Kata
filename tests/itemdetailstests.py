import unittest
import requests
import json
import uuid
from src.helpers import get_value

def MakeItemDetailsTests(baseurl):
    class ItemDetailsTests(unittest.TestCase):
        def setUp(self):
            self.order_id = str(uuid.uuid4())

        @classmethod
        def setUpClass(self):
            post_data = {'name': 'milk', 'price': 1.50, 'billing_method': 'unit'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))
            post_data = {'name': 'cheese', 'price': 5.75, 'billing_method': 'weight'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))

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

    return ItemDetailsTests

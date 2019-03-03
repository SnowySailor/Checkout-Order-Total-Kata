import unittest
import requests
import json
import uuid
from src.helpers import get_value

def MakeRemoveItemFromOrderTests(baseurl):
    class RemoveItemFromOrderTests(unittest.TestCase):
        def setUp(self):
            self.order_id = str(uuid.uuid4())

        @classmethod
        def setUpClass(self):
            post_data = {'name': 'milk', 'price': 1.50, 'billing_method': 'unit'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))
            post_data = {'name': 'cheese', 'price': 5.75, 'billing_method': 'weight'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))

        def test_post_remove_item_from_order_when_given_item_and_order_returns_200(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'milk', 'amount': 1}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'milk', 'amount': 1}
            r = requests.post(baseurl + '/removeitemfromorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)

        def test_post_remove_item_from_order_when_missing_order_id_returns_400(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'milk', 'amount': 1}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'item': 'milk', 'amount': 1}
            r = requests.post(baseurl + '/removeitemfromorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 400)

        def test_post_remove_item_from_order_when_missing_name_returns_400(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'milk', 'amount': 1}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'amount': 1}
            r = requests.post(baseurl + '/removeitemfromorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 400)

        def test_post_remove_item_from_order_when_item_does_not_exist_returns_400(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'milk', 'amount': 1}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'doesnotexist', 'amount': 1}
            r = requests.post(baseurl + '/removeitemfromorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 400)

        def test_post_remove_item_from_order_when_item_is_not_in_order_returns_400(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'milk', 'amount': 1}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'cheese', 'amount': 1}
            r = requests.post(baseurl + '/removeitemfromorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 400)

        def test_post_remove_item_from_order_when_order_id_does_not_exist_returns_400(self):
            post_data = {'order_id': 'doesnotexist', 'item': 'cheese', 'amount': 1}
            r = requests.post(baseurl + '/removeitemfromorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 400)

        def test_post_remove_item_from_order_when_given_order_and_item_removes_item(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'milk', 'amount': 1}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)

            expected = dict()
            expected['id'] = self.order_id
            expected['total_without_specials'] = 0.00
            expected['total_with_specials'] = 0.00
            expected['items'] = []

            post_data = {'order_id': self.order_id, 'item': 'milk', 'amount': 1}
            r = requests.post(baseurl + '/removeitemfromorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/getorder?id=' + self.order_id)
            self.assertEqual(r.text, json.dumps(expected))

        def test_post_remove_item_from_order_when_given_order_and_item_removes_some_items(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'milk', 'amount': 5}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)

            expected = dict()
            expected['id'] = self.order_id
            expected['total_without_specials'] = 6.00
            expected['total_with_specials'] = 6.00
            expected['items'] = [{'name': 'milk', 'amount': 4}]

            post_data = {'order_id': self.order_id, 'item': 'milk', 'amount': 1}
            r = requests.post(baseurl + '/removeitemfromorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/getorder?id=' + self.order_id)
            self.assertEqual(r.text, json.dumps(expected))

        def test_post_remove_item_from_order_when_missing_amount_defaults_to_1(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'milk', 'amount': 5}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)

            expected = dict()
            expected['id'] = self.order_id
            expected['total_without_specials'] = 6.00
            expected['total_with_specials'] = 6.00
            expected['items'] = [{'name': 'milk', 'amount': 4}]

            post_data = {'order_id': self.order_id, 'item': 'milk'}
            r = requests.post(baseurl + '/removeitemfromorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/getorder?id=' + self.order_id)
            self.assertEqual(r.text, json.dumps(expected))

    return RemoveItemFromOrderTests
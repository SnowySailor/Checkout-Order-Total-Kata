import unittest
import requests
import json
import uuid
from src.helpers import get_value

def MakeAddItemToOrderTests(baseurl):
    class AddItemToOrderTests(unittest.TestCase):
        def setUp(self):
            self.order_id = str(uuid.uuid4())

        @classmethod
        def setUpClass(self):
            post_data = {'name': 'milk', 'price': 1.50, 'billing_method': 'unit'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))
            post_data = {'name': 'cheese', 'price': 5.75, 'billing_method': 'weight'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))

        def test_post_add_item_to_order_when_given_item_and_order_returns_200(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'milk', 'quantity': 1}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)

        def test_post_add_item_to_order_when_missing_order_id_returns_400(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'item': 'cherries', 'quantity': 1.56}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 400)

        def test_post_add_item_to_order_when_missing_item_returns_400(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'quantity': 1.56}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 400)

        def test_post_add_item_to_order_when_order_does_not_exist_returns_400(self):
            post_data = {'order_id': 'doesnotexist', 'item': 'milk', 'quantity': 1.56}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 400)

        def test_post_add_item_to_order_when_item_does_not_exist_returns_400(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'doesnotexist', 'quantity': 1.56}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 400)

        def test_post_add_item_to_order_when_missing_amount_defaults_to_1(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'cheese'}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)

            expected = dict()
            expected['id'] = self.order_id
            expected['total_without_specials'] = 5.75
            expected['total_with_specials'] = 5.75
            expected['items'] = [{'name': 'cheese', 'quantity': 1.0}]
            r = requests.get(baseurl + '/getorder?id=' + self.order_id)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, json.dumps(expected))

        def test_post_add_item_to_order_when_item_added_multiple_times_amounts_add(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'cheese', 'quantity': 1.0}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'cheese', 'quantity': 5.6}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)

            expected = dict()
            expected['id'] = self.order_id
            expected['total_without_specials'] = 37.95
            expected['total_with_specials'] = 37.95
            expected['items'] = [{'name': 'cheese', 'quantity': 6.6}]
            r = requests.get(baseurl + '/getorder?id=' + self.order_id)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, json.dumps(expected))

    return AddItemToOrderTests
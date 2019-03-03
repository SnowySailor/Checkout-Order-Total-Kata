import unittest
import requests
import json
import uuid
from src.helpers import get_value

def MakeGetOrderTests(baseurl):
    class GetOrderTests(unittest.TestCase):
        def setUp(self):
            self.order_id = str(uuid.uuid4())

        @classmethod
        def setUpClass(self):
            post_data = {'name': 'milk', 'price': 1.50, 'billing_method': 'unit'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))
            post_data = {'name': 'cheese', 'price': 5.75, 'billing_method': 'weight'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))

        def test_get_get_order_when_given_valid_order_id_returns_200(self):
            post_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/getorder?id=' + self.order_id)
            self.assertEqual(r.status_code, 200)

        def test_get_get_order_when_given_valid_order_id_with_items_returns_200(self):
            post_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)

            post_data = {'order_id': self.order_id, 'item': 'milk', 'amount': 1}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)

            expected = dict()
            expected['id'] = self.order_id
            expected['total_without_specials'] = 1.50
            expected['total_with_specials'] = 1.50
            expected['items'] = [{'name': 'milk', 'amount': 1}]
            r = requests.get(baseurl + '/getorder?id=' + self.order_id)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, json.dumps(expected))

        def test_get_get_order_when_given_valid_order_id_with_weighted_items_returns_200(self):
            post_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)

            post_data = {'order_id': self.order_id, 'item': 'cheese', 'amount': 1}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)

            expected = dict()
            expected['id'] = self.order_id
            expected['total_without_specials'] = 5.75
            expected['total_with_specials'] = 5.75
            expected['items'] = [{'name': 'cheese', 'amount': 1.0}]
            r = requests.get(baseurl + '/getorder?id=' + self.order_id)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, json.dumps(expected))

        def test_get_get_order_when_given_valid_order_id_with_specials_returns_correct_totals(self):
            special1 = {'type': 'getEOLforAoff', 'off': 25}
            special2 = {'type': 'markdown', 'percentage': 50}
            item  = {'name': 'soup', 'price': 2.00, 'billing_method': 'unit', 'special': special2}
            item2 = {'name': 'peas', 'price': 1.78, 'billing_method': 'unit'}
            item3 = {'name': 'chicken', 'price': 2.37, 'billing_method': 'weight'}
            item4 = {'name': 'beef', 'price': 9.99, 'billing_method': 'weight', 'special': special1}

            r = requests.post(baseurl + '/createitem', data=json.dumps(item))
            r = requests.post(baseurl + '/createitem', data=json.dumps(item2))
            r = requests.post(baseurl + '/createitem', data=json.dumps(item3))
            r = requests.post(baseurl + '/createitem', data=json.dumps(item4))

            post_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)

            post_data = {'order_id': self.order_id, 'item': 'soup', 'amount': 4}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            post_data = {'order_id': self.order_id, 'item': 'peas', 'amount': 1}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            post_data = {'order_id': self.order_id, 'item': 'chicken', 'amount': 4.32}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            post_data = {'order_id': self.order_id, 'item': 'beef', 'amount': 9.34}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))

            expected = dict()
            expected['id'] = self.order_id
            expected['total_without_specials'] = 113.33
            expected['total_with_specials'] = 106.77
            expected['items'] = [
                {'name': 'soup', 'amount': 4},
                {'name': 'peas', 'amount': 1},
                {'name': 'chicken', 'amount': 4.32},
                {'name': 'beef', 'amount': 9.34}
            ]
            r = requests.get(baseurl + '/getorder?id=' + self.order_id)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, json.dumps(expected))

        def test_get_get_order_when_order_id_does_not_exist_returns_400(self):
            r = requests.get(baseurl + '/getorder?id=doesnotexist')
            self.assertEqual(r.status_code, 400)

        def test_get_get_order_when_not_given_order_id_returns_400(self):
            r = requests.get(baseurl + '/getorder')
            self.assertEqual(r.status_code, 400)

    return GetOrderTests

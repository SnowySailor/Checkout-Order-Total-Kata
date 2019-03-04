import unittest
import requests
import json
import uuid
from src.helpers import get_value

def MakeCreateItemTests(baseurl):
    class CreateItemTests(unittest.TestCase):
        def setUp(self):
            self.order_id = str(uuid.uuid4())

        @classmethod
        def setUpClass(self):
            post_data = {'name': 'milk', 'price': 1.50, 'billing_method': 'unit'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))
            post_data = {'name': 'cheese', 'price': 5.75, 'billing_method': 'weight'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))

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
            self.assertEqual(r.text, json.dumps(second_item))

        def test_post_create_item_with_AforB_special_saves_special(self):
            item = {'name': 'pasta', 'price': 2.99, 'billing_method': 'unit', 'special': {'type': 'AforB', 'buy': 5, 'for': 3.00}}
            r = requests.post(baseurl + '/createitem', data=json.dumps(item))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/itemdetails?name=pasta')
            self.assertEqual(r.text, json.dumps(item))

        def test_post_create_item_with_invalid_special_returns_400(self):
            item = {'name': 'pasta', 'price': 2.99, 'billing_method': 'unit', 'special': {'type': 'invalidspecial', 'buy': 5, 'for': 3.00}}
            r = requests.post(baseurl + '/createitem', data=json.dumps(item))
            self.assertEqual(r.status_code, 400)

        def test_post_create_item_with_AforB_special_missing_buy_returns_400(self):
            item = {'name': 'pasta', 'price': 2.99, 'billing_method': 'unit', 'special': {'type': 'AforB', 'for': 3.00}}
            r = requests.post(baseurl + '/createitem', data=json.dumps(item))
            self.assertEqual(r.status_code, 400)

        def test_post_create_item_with_AforB_special_missing_for_returns_400(self):
            item = {'name': 'pasta', 'price': 2.99, 'billing_method': 'unit', 'special': {'type': 'AforB', 'buy': 5}}
            r = requests.post(baseurl + '/createitem', data=json.dumps(item))
            self.assertEqual(r.status_code, 400)

        def test_post_create_item_with_AforB_with_limit_special_saves_special(self):
            item = {'name': 'pasta', 'price': 2.99, 'billing_method': 'unit', 'special': {'type': 'AforB', 'buy': 5, 'for': 3.00, 'limit': 10}}
            r = requests.post(baseurl + '/createitem', data=json.dumps(item))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/itemdetails?name=pasta')
            self.assertEqual(r.text, json.dumps(item))

        def test_post_create_item_with_buyAgetBforCoff_special_saves_special(self):
            item = {'name': 'chicken', 'price': 2.99, 'billing_method': 'unit', 'special': {'type': 'buyAgetBforCoff', 'buy': 1, 'get': 2, 'off': 50.0}}
            r = requests.post(baseurl + '/createitem', data=json.dumps(item))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/itemdetails?name=chicken')
            self.assertEqual(r.text, json.dumps(item))

        def test_post_create_item_with_buyAgetBforCoff_special_missing_buy_returns_400(self):
            item = {'name': 'chicken', 'price': 2.99, 'billing_method': 'unit', 'special': {'type': 'buyAgetBforCoff', 'get': 2, 'off': 50.0}}
            r = requests.post(baseurl + '/createitem', data=json.dumps(item))
            self.assertEqual(r.status_code, 400)

        def test_post_create_item_with_buyAgetBforCoff_special_missing_get_returns_400(self):
            item = {'name': 'chicken', 'price': 2.99, 'billing_method': 'unit', 'special': {'type': 'buyAgetBforCoff', 'buy': 2, 'off': 50.0}}
            r = requests.post(baseurl + '/createitem', data=json.dumps(item))
            self.assertEqual(r.status_code, 400)

        def test_post_create_item_with_buyAgetBforCoff_special_missing_off_returns_400(self):
            item = {'name': 'chicken', 'price': 2.99, 'billing_method': 'unit', 'special': {'type': 'buyAgetBforCoff', 'buy': 2, 'get': 1}}
            r = requests.post(baseurl + '/createitem', data=json.dumps(item))
            self.assertEqual(r.status_code, 400)

        def test_post_create_item_with_buyAgetBforCoff_special_with_limit_saves_special(self):
            item = {'name': 'chicken', 'price': 2.99, 'billing_method': 'unit', 'special': {'type': 'buyAgetBforCoff', 'buy': 1, 'get': 2, 'off': 50.0, 'limit': 5}}
            r = requests.post(baseurl + '/createitem', data=json.dumps(item))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/itemdetails?name=chicken')
            self.assertEqual(r.text, json.dumps(item))

        def test_post_create_item_with_getEOLforAoff_special_saves_special(self):
            item = {'name': 'rice', 'price': 2.99, 'billing_method': 'weight', 'special': {'type': 'getEOLforAoff', 'off': 50.0}}
            r = requests.post(baseurl + '/createitem', data=json.dumps(item))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/itemdetails?name=rice')
            self.assertEqual(r.text, json.dumps(item))

        def test_post_create_item_with_getEOLforAoff_special_missing_off_returns_400(self):
            item = {'name': 'rice', 'price': 2.99, 'billing_method': 'weight', 'special': {'type': 'getEOLforAoff'}}
            r = requests.post(baseurl + '/createitem', data=json.dumps(item))
            self.assertEqual(r.status_code, 400)

        def test_post_create_item_with_markdown_special_saves_special(self):
            item = {'name': 'beans', 'price': 2.99, 'billing_method': 'unit', 'special': {'type': 'markdown', 'percentage': 50.0}}
            r = requests.post(baseurl + '/createitem', data=json.dumps(item))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/itemdetails?name=beans')
            self.assertEqual(r.text, json.dumps(item))

        def test_post_create_item_with_markdown_special_missing_percentage_returns_400(self):
            item = {'name': 'beans', 'price': 2.99, 'billing_method': 'unit', 'special': {'type': 'markdown'}}
            r = requests.post(baseurl + '/createitem', data=json.dumps(item))
            self.assertEqual(r.status_code, 400)

        def test_post_create_item_with_markdown_special_with_limit_saves_special(self):
            item = {'name': 'beans', 'price': 2.99, 'billing_method': 'unit', 'special': {'type': 'markdown', 'percentage': 50.0, 'limit': 10}}
            r = requests.post(baseurl + '/createitem', data=json.dumps(item))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/itemdetails?name=beans')
            self.assertEqual(r.text, json.dumps(item))

        def test_post_create_item_with_markdown_special_with_negative_limit_returns_400(self):
            item = {'name': 'beans', 'price': 2.99, 'billing_method': 'unit', 'special': {'type': 'markdown', 'percentage': 50.0, 'limit': -4}}
            r = requests.post(baseurl + '/createitem', data=json.dumps(item))
            self.assertEqual(r.status_code, 400)

        def test_post_create_item_when_item_already_exists_it_is_overwritten_and_orders_totals_update(self):
            first_item = {'name': 'pie', 'price': 5.00, 'billing_method': 'unit'}
            second_item = {'name': 'pie', 'price': 4.05, 'billing_method': 'unit'}
            order = {'id': self.order_id}
            order_item = {'order_id': self.order_id, 'item': 'pie', 'quantity': 3}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order))
            self.assertEqual(r.status_code, 200)
            r = requests.post(baseurl + '/createitem', data=json.dumps(first_item))
            self.assertEqual(r.status_code, 200)
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(order_item))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/getorder?id=' + self.order_id)
            self.assertEqual(r.status_code, 200)

            expected = dict()
            expected['id'] = self.order_id
            expected['total_without_specials'] = 15.00
            expected['total_with_specials'] = 15.00
            expected['items'] = [{'name': 'pie', 'quantity': 3}]

            self.assertEqual(r.text, json.dumps(expected))

            r = requests.post(baseurl + '/createitem', data=json.dumps(second_item))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/getorder?id=' + self.order_id)
            self.assertEqual(r.status_code, 200)

            expected = dict()
            expected['id'] = self.order_id
            expected['total_without_specials'] = 12.15
            expected['total_with_specials'] = 12.15
            expected['items'] = [{'name': 'pie', 'quantity': 3}]

            self.assertEqual(r.text, json.dumps(expected))

        def test_get_create_item_returns_404(self):
            r = requests.get(baseurl + '/createitem')
            self.assertEqual(r.status_code, 404)

    return CreateItemTests

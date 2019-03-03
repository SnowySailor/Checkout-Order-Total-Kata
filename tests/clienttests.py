import unittest
import requests
import json
import uuid
from src.helpers import get_value

def MakeClientTests(baseurl):
    class ClientTests(unittest.TestCase):
        def setUp(self):
            self.order_id = str(uuid.uuid4())

        @classmethod
        def setUpClass(self):
            post_data = {'name': 'milk', 'price': 1.50, 'billing_method': 'unit'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))
            post_data = {'name': 'cheese', 'price': 5.75, 'billing_method': 'weight'}
            r = requests.post(baseurl + '/createitem', data=json.dumps(post_data))

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
            r = requests.post(baseurl + '/datastore', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)

        def test_post_data_store_when_not_given_key_returns_400(self):
            post_data = {'value': 'value456'}
            r = requests.post(baseurl + '/datastore', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 400)

        def test_post_data_store_when_not_given_value_returns_400(self):
            post_data = {'key': 'key123'}
            r = requests.post(baseurl + '/datastore', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 400)

        def test_get_data_store_when_endpoint_is_datastore1_returns_404(self):
            r = requests.get(baseurl + '/datastore1/test')
            self.assertEqual(r.status_code, 404)

        def test_get_data_store_when_key_doesnt_exist_returns_null(self):
            r = requests.get(baseurl + '/datastore/doesnotexist')
            self.assertEqual(r.text, 'null')

        def test_get_data_store_when_key_does_exist_returns_value_associated_with_key(self):
            post_data = {'key': 'testingkey', 'value': 'testingvalue'}
            r = requests.post(baseurl + '/datastore', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/datastore/testingkey')
            self.assertEqual(r.text, '"testingvalue"')

        def test_delete_data_store_when_key_does_not_exist_returns_200(self):
            r = requests.delete(baseurl + '/datastore/doesnotexist')
            self.assertEqual(r.status_code, 200)

        def test_delete_data_store_when_key_exists_it_is_deleted(self):
            post_data = {'key': 'testingkey123', 'value': 'testingvalue123'}
            r = requests.post(baseurl + '/datastore', data=json.dumps(post_data))
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
            self.assertEqual(r.text, json.dumps(second_item))

        def test_post_create_item_with_AforB_special_saves_special(self):
            item = {'name': 'pasta', 'price': 2.99, 'billing_method': 'unit', 'special': {'type': 'AforB', 'buy': 5, 'for': 3.00}}
            r = requests.post(baseurl + '/createitem', data=json.dumps(item))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/itemdetails?name=pasta')
            self.assertEqual(r.text, json.dumps(item))

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
            order_item = {'order_id': self.order_id, 'item': 'pie', 'amount': 3}
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
            expected['total'] = 15.00
            expected['items'] = [{'name': 'pie', 'amount': 3}]

            self.assertEqual(r.text, json.dumps(expected))

            r = requests.post(baseurl + '/createitem', data=json.dumps(second_item))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/getorder?id=' + self.order_id)
            self.assertEqual(r.status_code, 200)

            expected = dict()
            expected['id'] = self.order_id
            expected['total'] = 12.15
            expected['items'] = [{'name': 'pie', 'amount': 3}]

            self.assertEqual(r.text, json.dumps(expected))

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


        # createorder
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

        # additemtoorder
        def test_post_add_item_to_order_when_given_item_and_order_returns_200(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'milk', 'amount': 1}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)

        def test_post_add_item_to_order_when_missing_order_id_returns_400(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'item': 'cherries', 'amount': 1.56}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 400)

        def test_post_add_item_to_order_when_missing_item_returns_400(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'amount': 1.56}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 400)

        def test_post_add_item_to_order_when_order_does_not_exist_returns_400(self):
            post_data = {'order_id': 'doesnotexist', 'item': 'milk', 'amount': 1.56}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 400)

        def test_post_add_item_to_order_when_item_does_not_exist_returns_400(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'doesnotexist', 'amount': 1.56}
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
            expected['total'] = 5.75
            expected['items'] = [{'name': 'cheese', 'amount': 1.0}]
            r = requests.get(baseurl + '/getorder?id=' + self.order_id)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, json.dumps(expected))

        def test_post_add_item_to_order_when_item_added_multiple_times_amounts_add(self):
            order_data = {'id': self.order_id}
            r = requests.post(baseurl + '/createorder', data=json.dumps(order_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'cheese', 'amount': 1.0}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)
            post_data = {'order_id': self.order_id, 'item': 'cheese', 'amount': 5.6}
            r = requests.post(baseurl + '/additemtoorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)

            expected = dict()
            expected['id'] = self.order_id
            expected['total'] = 37.95
            expected['items'] = [{'name': 'cheese', 'amount': 6.6}]
            r = requests.get(baseurl + '/getorder?id=' + self.order_id)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, json.dumps(expected))

        # removeitemfromorder
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
            expected['total'] = 0.00
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
            expected['total'] = 6.00
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
            expected['total'] = 6.00
            expected['items'] = [{'name': 'milk', 'amount': 4}]

            post_data = {'order_id': self.order_id, 'item': 'milk'}
            r = requests.post(baseurl + '/removeitemfromorder', data=json.dumps(post_data))
            self.assertEqual(r.status_code, 200)
            r = requests.get(baseurl + '/getorder?id=' + self.order_id)
            self.assertEqual(r.text, json.dumps(expected))

        # getorder
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
            expected['total'] = 1.50
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
            expected['total'] = 5.75
            expected['items'] = [{'name': 'cheese', 'amount': 1.0}]
            r = requests.get(baseurl + '/getorder?id=' + self.order_id)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, json.dumps(expected))

        def test_get_get_order_when_order_id_does_not_exist_returns_400(self):
            r = requests.get(baseurl + '/getorder?id=doesnotexist')
            self.assertEqual(r.status_code, 400)

        def test_get_get_order_when_not_given_order_id_returns_400(self):
            r = requests.get(baseurl + '/getorder')
            self.assertEqual(r.status_code, 400)

    return ClientTests

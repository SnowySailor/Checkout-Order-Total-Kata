import unittest
from src.models.item import Item
from src.models.order import MakeOrder
from src.database import DataStore
import src.helpers as H
import uuid

def MakeServerTests(baseurl):
    class ServerTests(unittest.TestCase):
        def setUp(self):
            self.order_id = str(uuid.uuid4())

        # Calculating the savings from specials
        def test_calculate_best_savings_for_BuyAgetBforCoff_for_item_with_1_amount_returns_0(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 1,
                'get': 2,
                'off': 50
            }
            
            datastore = DataStore()
            item = self.create_item('test', 5.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'test', 'amount': 1}, [], datastore)
            self.assertEqual(savings, 0)

        def test_calculate_best_savings_for_BuyAgetBforCoff_for_item_with_5_amount_returns_correct_savings(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 1,
                'get': 2,
                'off': 50
            }
            
            datastore = DataStore()
            item = self.create_item('test', 5.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'test', 'amount': 5}, [], datastore)
            self.assertEqual(savings, 5.0)

        def test_calculate_best_savings_for_BuyAgetBforCoff_for_item_with_buy_1_get_2_50_off(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 1,
                'get': 2,
                'off': 50
            }

            datastore = DataStore()
            item = self.create_item('test', 5.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'test', 'amount': 6}, [], datastore)
            self.assertEqual(savings, 10.0)

        def test_calculate_best_savings_for_BuyAgetBforCoff_for_item_with_buy_2_get_1_free(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 2,
                'get': 1,
                'off': 100
            }

            datastore = DataStore()
            item = self.create_item('test', 6.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'test', 'amount': 2}, [], datastore)
            self.assertEqual(savings, 0)

        def test_calculate_best_savings_for_BuyAgetBforCoff_for_item_with_buy_2_get_1_free_1_occurrence(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 2,
                'get': 1,
                'off': 100
            }

            datastore = DataStore()
            item = self.create_item('test', 6.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'test', 'amount': 3}, [], datastore)
            self.assertEqual(savings, 6.0)

        def test_calculate_best_savings_for_BuyAgetBforCoff_for_item_with_buy_2_get_1_free_2_occurrences(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 2,
                'get': 1,
                'off': 100
            }

            datastore = DataStore()
            item = self.create_item('test', 6.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'test', 'amount': 7}, [], datastore)
            self.assertEqual(savings, 12.0)

        def test_calculate_best_savings_for_BuyAgetBforCoff_for_buy_1_get_1_free_limit_2_with_10_items(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 1,
                'get': 1,
                'off': 100,
                'limit': 2
            }

            datastore = DataStore()
            item = self.create_item('test', 5.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'test', 'amount': 10}, [], datastore)
            self.assertEqual(savings, 5.0)

        def test_calculate_best_savings_for_BuyAgetBforCoff_for_buy_1_get_1_free_limit_3_with_10_items(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 1,
                'get': 1,
                'off': 100,
                'limit': 3
            }

            datastore = DataStore()
            item = self.create_item('test', 5.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'test', 'amount': 10}, [], datastore)
            self.assertEqual(savings, 5.0)

        def test_calculate_best_savings_for_GetEOLforAoff_with_10_dollar_meat_and_9_dollar_other_item(self):
            special = {
                'type': 'getEOLforAoff',
                'off': 50
            }

            datastore = DataStore()
            item  = self.create_item('meat', 5.00, 'weight', special, datastore)
            item2 = self.create_item('soup', 4.50, 'unit', None, datastore)
            
            savings = item.special.calculate_best_savings({'name': 'meat', 'amount': 2}, [{'name': 'soup', 'amount': 2}], datastore)
            self.assertEqual(savings, 2.25)

        def test_calculate_best_savings_for_GetEOLforAoff_with_10_dollar_meat_and_15_dollar_other_items(self):
            special = {
                'type': 'getEOLforAoff',
                'off': 50
            }

            datastore = DataStore()
            item  = self.create_item('meat', 5.00, 'weight', special, datastore)
            item2 = self.create_item('soup', 5.00, 'unit', None, datastore)

            savings = item.special.calculate_best_savings({'name': 'meat', 'amount': 2}, [{'name': 'soup', 'amount': 3}], datastore)
            self.assertEqual(savings, 2.50)

        def test_calculate_best_savings_for_GetEOLforAoff_with_10_dollar_meat_and_15_dollar_other_single_item(self):
            special = {
                'type': 'getEOLforAoff',
                'off': 50
            }

            datastore = DataStore()
            item  = self.create_item('meat', 5.00, 'weight', special, datastore)
            item2 = self.create_item('soup', 15.00, 'unit', None, datastore)

            savings = item.special.calculate_best_savings({'name': 'meat', 'amount': 2}, [{'name': 'soup', 'amount': 1}], datastore)
            self.assertEqual(savings, 0.00)

        def test_calculate_best_savings_for_GetEOLforAoff_with_10_dollar_meat_and_15_dollar_two_other_items(self):
            special = {
                'type': 'getEOLforAoff',
                'off': 50
            }

            datastore = DataStore()
            item  = self.create_item('meat', 5.00, 'weight', special, datastore)
            item2 = self.create_item('soup', 10.00, 'unit', None, datastore)
            item3 = self.create_item('pasta', 1.00, 'unit', None, datastore)

            savings = item.special.calculate_best_savings({'name': 'meat', 'amount': 2}, [{'name': 'soup', 'amount': 1}, {'name': 'pasta', 'amount': 15}], datastore)
            self.assertEqual(savings, 5.00)

        def test_calculate_best_savings_for_AforB_with_2_for_5_with_2_items(self):
            special = {
                'type': 'AforB',
                'buy': 2,
                'for': 5.00
            }

            datastore = DataStore()
            item  = self.create_item('soup', 3.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'soup', 'amount': 2}, [], datastore)
            self.assertEqual(savings, 1.00)

        def test_calculate_best_savings_for_AforB_with_5_for_5_with_10_items(self):
            special = {
                'type': 'AforB',
                'buy': 5,
                'for': 5.00
            }

            datastore = DataStore()
            item  = self.create_item('soup', 2.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'soup', 'amount': 10}, [], datastore)
            self.assertEqual(savings, 10.00)

        def test_calculate_best_savings_for_AforB_with_5_for_5_with_15_items_and_limit_10(self):
            special = {
                'type': 'AforB',
                'buy': 5,
                'for': 5.00,
                'limit': 10
            }

            datastore = DataStore()
            item  = self.create_item('soup', 2.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'soup', 'amount': 10}, [], datastore)
            self.assertEqual(savings, 10.00)

        def test_calculate_best_savings_for_AforB_with_5_for_5_with_8_items_and_limit_10(self):
            special = {
                'type': 'AforB',
                'buy': 5,
                'for': 5.00,
                'limit': 10
            }

            datastore = DataStore()
            item  = self.create_item('soup', 2.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'soup', 'amount': 8}, [], datastore)
            self.assertEqual(savings, 5.00)

        def test_calculate_best_savings_for_AforB_with_10_for_5_with_9_items_returns_0(self):
            special = {
                'type': 'AforB',
                'buy': 10,
                'for': 5.00,
            }

            datastore = DataStore()
            item  = self.create_item('soup', 2.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'soup', 'amount': 9}, [], datastore)
            self.assertEqual(savings, 0.00)

        def test_calculate_best_savings_for_markdown_with_50_off_with_2_items(self):
            special = {
                'type': 'markdown',
                'percentage': 50
            }

            datastore = DataStore()
            item  = self.create_item('soup', 2.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'soup', 'amount': 2}, [], datastore)
            self.assertEqual(savings, 2.00)

        def test_calculate_best_savings_for_markdown_with_50_off_with_4_items_with_limit_2(self):
            special = {
                'type': 'markdown',
                'percentage': 50,
                'limit': 2
            }

            datastore = DataStore()
            item  = self.create_item('soup', 2.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'soup', 'amount': 4}, [], datastore)
            self.assertEqual(savings, 2.00)

        def test_calculate_best_savings_for_markdown_with_100_off_with_5_items_with_limit_5(self):
            special = {
                'type': 'markdown',
                'percentage': 100,
                'limit': 5
            }

            datastore = DataStore()
            item  = self.create_item('soup', 2.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'soup', 'amount': 5}, [], datastore)
            self.assertEqual(savings, 10.00)

        def test_calculate_best_savings_for_markdown_with_0_off_with_5_items_with_limit_5(self):
            special = {
                'type': 'markdown',
                'percentage': 0,
                'limit': 5
            }

            datastore = DataStore()
            item  = self.create_item('soup', 2.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'soup', 'amount': 5}, [], datastore)
            self.assertEqual(savings, 0.00)

        def test_calculate_best_savings_for_markdown_with_25_off_with_5_items_with_limit_1(self):
            special = {
                'type': 'markdown',
                'percentage': 25,
                'limit': 1
            }

            datastore = DataStore()
            item  = self.create_item('soup', 2.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'soup', 'amount': 5}, [], datastore)
            self.assertEqual(savings, 0.50)

        def test_calculate_best_savings_for_markdown_with_25_off_with_5_items_with_limit_6(self):
            special = {
                'type': 'markdown',
                'percentage': 25,
                'limit': 6
            }

            datastore = DataStore()
            item  = self.create_item('soup', 2.00, 'unit', special, datastore)

            savings = item.special.calculate_best_savings({'name': 'soup', 'amount': 5}, [], datastore)
            self.assertEqual(savings, 2.50)

        # calculate_total
        def test_calculate_total_for_order_with_no_specials_and_4_items(self):
            datastore = DataStore()
            item  = self.create_item('soup', 2.00, 'unit', None, datastore)
            item2 = self.create_item('peas', 1.78, 'unit', None, datastore)
            item3 = self.create_item('chicken', 2.37, 'weight', None, datastore)
            item4 = self.create_item('beef', 9.99, 'weight', None, datastore)
            order = self.create_order(datastore)

            order.add_item(item, 3)
            order.add_item(item2, 1)
            order.add_item(item3, 4.32)
            order.add_item(item4, 9.34)

            total = order.calculate_total()
            self.assertEqual(total, 111.33)

        def test_calculate_total_for_order_with_no_specials_and_4_items_2(self):
            datastore = DataStore()
            item  = self.create_item('soup', 2.00, 'unit', None, datastore)
            item2 = self.create_item('peas', 1.78, 'unit', None, datastore)
            item3 = self.create_item('chicken', 2.37, 'weight', None, datastore)
            item4 = self.create_item('beef', 9.99, 'weight', None, datastore)
            order = self.create_order(datastore)

            order.add_item(item, 1)
            order.add_item(item2, 1)
            order.add_item(item3, 5.32)
            order.add_item(item4, 99.34)

            total = order.calculate_total()
            self.assertEqual(total, 1008.80)

        def test_calculate_total_for_order_with_no_specials_and_no_items(self):
            datastore = DataStore()
            item  = self.create_item('soup', 2.00, 'unit', None, datastore)
            item2 = self.create_item('peas', 1.78, 'unit', None, datastore)
            item3 = self.create_item('chicken', 2.37, 'weight', None, datastore)
            item4 = self.create_item('beef', 9.99, 'weight', None, datastore)
            order = self.create_order(datastore)

            total = order.calculate_total()
            self.assertEqual(total, 0.00)

        def create_item(self, name, price, billing_method, special, datastore):
            item = Item(name, price, billing_method, special)
            datastore.set('itemdetails:' + name, item)
            return item

        def create_order(self, datastore):
            order = MakeOrder(self.order_id, datastore)
            datastore.set('orders:' + order.order_id, order)
            return order

    return ServerTests

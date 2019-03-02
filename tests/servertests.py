import unittest
from src.models.item import Item
from src.database import DataStore
import src.helpers as H

def MakeServerTests(baseurl):
    class ServerTests(unittest.TestCase):
        # Calculating the savings from specials
        def test_calculate_best_savings_for_BuyAgetBforCoff_for_item_with_1_amount_returns_0(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 1,
                'get': 2,
                'off': 0.5
            }
            item = Item('test', 5.00, 'unit', special)
            datastore = DataStore()
            datastore.set('itemdetails:' + item.name, item)

            savings = item.special.calculate_best_savings({'name': 'test', 'amount': 1}, [], datastore)
            self.assertEqual(savings, 0)

        def test_calculate_best_savings_for_BuyAgetBforCoff_for_item_with_5_amount_returns_correct_savings(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 1,
                'get': 2,
                'off': 0.5
            }
            item = Item('test', 5.00, 'unit', special)
            datastore = DataStore()
            datastore.set('itemdetails:' + item.name, item)

            savings = item.special.calculate_best_savings({'name': 'test', 'amount': 5}, [], datastore)
            self.assertEqual(savings, 5.0)

        def test_calculate_best_savings_for_BuyAgetBforCoff_for_item_with_buy_1_get_2_50_off(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 1,
                'get': 2,
                'off': 0.5
            }
            item = Item('test', 5.00, 'unit', special)
            datastore = DataStore()
            datastore.set('itemdetails:' + item.name, item)

            savings = item.special.calculate_best_savings({'name': 'test', 'amount': 6}, [], datastore)
            self.assertEqual(savings, 10.0)

        def test_calculate_best_savings_for_BuyAgetBforCoff_for_item_with_buy_2_get_1_free(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 2,
                'get': 1,
                'off': 1.0
            }
            item = Item('test', 6.00, 'unit', special)
            datastore = DataStore()
            datastore.set('itemdetails:' + item.name, item)

            savings = item.special.calculate_best_savings({'name': 'test', 'amount': 2}, [], datastore)
            self.assertEqual(savings, 0)

        def test_calculate_best_savings_for_BuyAgetBforCoff_for_item_with_buy_2_get_1_free_1_occurrence(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 2,
                'get': 1,
                'off': 1.0
            }
            item = Item('test', 6.00, 'unit', special)
            datastore = DataStore()
            datastore.set('itemdetails:' + item.name, item)

            savings = item.special.calculate_best_savings({'name': 'test', 'amount': 3}, [], datastore)
            self.assertEqual(savings, 6.0)

        def test_calculate_best_savings_for_BuyAgetBforCoff_for_item_with_buy_2_get_1_free_2_occurrences(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 2,
                'get': 1,
                'off': 1.0
            }
            item = Item('test', 6.00, 'unit', special)
            datastore = DataStore()
            datastore.set('itemdetails:' + item.name, item)

            savings = item.special.calculate_best_savings({'name': 'test', 'amount': 7}, [], datastore)
            self.assertEqual(savings, 12.0)

        def test_calculate_best_savings_for_BuyAgetBforCoff_for_buy_1_get_1_free_limit_2_with_10_items(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 1,
                'get': 1,
                'off': 1.0,
                'limit': 2
            }
            item = Item('test', 5.00, 'unit', special)
            datastore = DataStore()
            datastore.set('itemdetails:' + item.name, item)

            savings = item.special.calculate_best_savings({'name': 'test', 'amount': 10}, [], datastore)
            self.assertEqual(savings, 5.0)

        def test_calculate_best_savings_for_BuyAgetBforCoff_for_buy_1_get_1_free_limit_3_with_10_items(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 1,
                'get': 1,
                'off': 1.0,
                'limit': 3
            }
            item = Item('test', 5.00, 'unit', special)
            datastore = DataStore()
            datastore.set('itemdetails:' + item.name, item)

            savings = item.special.calculate_best_savings({'name': 'test', 'amount': 10}, [], datastore)
            self.assertEqual(savings, 5.0)

        # Validating specials
        def test_validate_special_AforB_with_weight_item_returns_error(self):
            special = {
                'type': 'AforB',
                'buy': 5,
                'for': 3.00
            }
            self.assertNotEqual(H.validate_special(special, 'weight'), '')

        def test_validate_special_AforB_with_unit_item_returns_ok(self):
            special = {
                'type': 'AforB',
                'buy': 5,
                'for': 3.00
            }
            self.assertEqual(H.validate_special(special, 'unit'), '')

        def test_validate_special_markdown_with_weight_item_returns_ok(self):
            special = {
                'type': 'markdown',
                'percentage': 50
            }
            self.assertEqual(H.validate_special(special, 'weight'), '')

        def test_validate_special_markdown_with_unit_item_returns_ok(self):
            special = {
                'type': 'markdown',
                'percentage': 50
            }
            self.assertEqual(H.validate_special(special, 'unit'), '')

        def test_validate_special_buyAgetBforCoff_with_weight_item_returns_error(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 1,
                'get': 4,
                'off': 25
            }
            self.assertNotEqual(H.validate_special(special, 'weight'), '')

        def test_validate_special_buyAgetBforCoff_with_unit_item_returns_ok(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 1,
                'get': 4,
                'off': 25
            }
            self.assertEqual(H.validate_special(special, 'unit'), '')


    return ServerTests

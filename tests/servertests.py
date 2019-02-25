import unittest
from src.models.item import Item
from src.database import DataStore

def MakeServerTests(baseurl):
    class ServerTests(unittest.TestCase):
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

    return ServerTests
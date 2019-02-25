import unittest
from src.models.item import Item

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

            savings = item.special.calculate_best_savings({'name': 'test', 'amount': 1}, [], None)
            self.assertEqual(savings, 0)

    return ServerTests
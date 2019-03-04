import unittest
from src.models.item import Item
from src.models.order import MakeOrder
from src.database import DataStore
import src.helpers as H
import uuid

def MakeCalculateTotalTests(baseurl):
    class CalculateTotalTests(unittest.TestCase):
        def setUp(self):
            self.order_id = str(uuid.uuid4())

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

        def test_calculate_total_for_order_with_one_markdown_special_and_4_items(self):
            datastore = DataStore()
            special = {
                'type': 'markdown',
                'price': 0.50,
                'limit': 6
            }
            item  = self.create_item('soup', 2.00, 'unit', special, datastore)
            item2 = self.create_item('peas', 1.78, 'unit', None, datastore)
            item3 = self.create_item('chicken', 2.37, 'weight', None, datastore)
            item4 = self.create_item('beef', 9.99, 'weight', None, datastore)
            order = self.create_order(datastore)

            order.add_item(item, 3)
            order.add_item(item2, 1)
            order.add_item(item3, 4.32)
            order.add_item(item4, 9.34)

            total = order.calculate_total()
            self.assertEqual(total, 109.83)

        def test_calculate_total_for_order_with_two_markdown_specials_and_4_items(self):
            datastore = DataStore()
            special1 = {'type': 'markdown','price': 0.50,'limit': 6}
            special2 = {'type': 'markdown','price': 0.89}
            item  = self.create_item('soup', 2.00, 'unit', special1, datastore)
            item2 = self.create_item('peas', 1.78, 'unit', special2, datastore)
            item3 = self.create_item('chicken', 2.37, 'weight', None, datastore)
            item4 = self.create_item('beef', 9.99, 'weight', None, datastore)
            order = self.create_order(datastore)

            order.add_item(item, 3)
            order.add_item(item2, 1)
            order.add_item(item3, 4.32)
            order.add_item(item4, 9.34)

            total = order.calculate_total()
            self.assertEqual(total, 108.94)

        def test_calculate_total_for_order_with_one_AforB_special_and_4_items(self):
            datastore = DataStore()
            special1 = {'type': 'AforB', 'buy': 2, 'for': 2.00}
            item  = self.create_item('soup', 2.00, 'unit', special1, datastore)
            item2 = self.create_item('peas', 1.78, 'unit', None, datastore)
            item3 = self.create_item('chicken', 2.37, 'weight', None, datastore)
            item4 = self.create_item('beef', 9.99, 'weight', None, datastore)
            order = self.create_order(datastore)

            order.add_item(item, 4)
            order.add_item(item2, 1)
            order.add_item(item3, 4.32)
            order.add_item(item4, 9.34)

            total = order.calculate_total()
            self.assertEqual(total, 109.33)

        def test_calculate_total_for_order_with_one_AforB_special_and_markdown_and_4_items(self):
            datastore = DataStore()
            special1 = {'type': 'AforB', 'buy': 2, 'for': 2.00}
            special2 = {'type': 'markdown','price': 0.89}
            item  = self.create_item('soup', 2.00, 'unit', special1, datastore)
            item2 = self.create_item('peas', 1.78, 'unit', special2, datastore)
            item3 = self.create_item('chicken', 2.37, 'weight', None, datastore)
            item4 = self.create_item('beef', 9.99, 'weight', None, datastore)
            order = self.create_order(datastore)

            order.add_item(item, 4)
            order.add_item(item2, 1)
            order.add_item(item3, 4.32)
            order.add_item(item4, 9.34)

            total = order.calculate_total()
            self.assertEqual(total, 108.44)

        def test_calculate_total_for_order_with_one_getEOLforAoff_special_and_markdown_and_4_items(self):
            datastore = DataStore()
            special1 = {'type': 'getEOLforAoff', 'off': 75}
            special2 = {'type': 'markdown', 'price': 0.89}
            item  = self.create_item('soup', 2.00, 'unit', None, datastore)
            item2 = self.create_item('peas', 1.78, 'unit', special2, datastore)
            item3 = self.create_item('chicken', 2.37, 'weight', None, datastore)
            item4 = self.create_item('beef', 9.99, 'weight', special1, datastore)
            order = self.create_order(datastore)

            order.add_item(item, 4)
            order.add_item(item2, 1)
            order.add_item(item3, 4.32)
            order.add_item(item4, 9.34)

            total = order.calculate_total()
            self.assertEqual(total, 104.76)

        def test_calculate_total_for_order_with_one_getEOLforAoff_special_and_markdown_and_4_items_2(self):
            datastore = DataStore()
            special1 = {'type': 'getEOLforAoff', 'off': 25}
            special2 = {'type': 'markdown', 'price': 1.00}
            item  = self.create_item('soup', 2.00, 'unit', special2, datastore)
            item2 = self.create_item('peas', 1.78, 'unit', None, datastore)
            item3 = self.create_item('chicken', 2.37, 'weight', None, datastore)
            item4 = self.create_item('beef', 9.99, 'weight', special1, datastore)
            order = self.create_order(datastore)

            order.add_item(item, 4)
            order.add_item(item2, 1)
            order.add_item(item3, 4.32)
            order.add_item(item4, 9.34)

            total = order.calculate_total()
            self.assertEqual(total, 106.77)

        def test_calculate_total_for_order_with_one_getEOLforAoff_and_markdown_and_AforB_5_items(self):
            datastore = DataStore()
            special1 = {'type': 'getEOLforAoff', 'off': 25}
            special2 = {'type': 'markdown', 'price': 4.00}
            special3 = {'type': 'AforB', 'buy': 3, 'for': 5.00}

            item  = self.create_item('soup'   , 2.00, 'unit', special3, datastore)
            item2 = self.create_item('peas'   , 1.78, 'unit', None, datastore)
            item3 = self.create_item('chicken', 2.37, 'weight', None, datastore)
            item4 = self.create_item('beef'   , 9.99, 'weight', special1, datastore)
            item5 = self.create_item('cheese' , 8.00, 'unit', special2, datastore)
            order = self.create_order(datastore)

            order.add_item(item , 4)
            order.add_item(item2, 1)
            order.add_item(item3, 1.32)
            order.add_item(item4, 9.34)
            order.add_item(item5, 2)

            total = order.calculate_total()
            self.assertEqual(total, 112.44)

        def test_calculate_total_for_order_with_6_specials_and_10_items(self):
            datastore = DataStore()
            special1 = {'type': 'getEOLforAoff', 'off': 25}
            special2 = {'type': 'markdown', 'price': 4.00}
            special3 = {'type': 'AforB', 'buy': 3, 'for': 5.00}
            special4 = {'type': 'buyAgetBforCoff', 'buy': 1, 'get': 1, 'off': 50}
            special5 = {'type': 'markdown', 'price': 0.50}
            special6 = {'type': 'getEOLforAoff', 'off': 35}

            item  = self.create_item('soup'    , 2.00, 'unit'  , special3, datastore)
            item2 = self.create_item('peas'    , 1.78, 'unit'  , None, datastore)
            item3 = self.create_item('chicken' , 2.37, 'weight', None, datastore)
            item4 = self.create_item('beef'    , 9.99, 'weight', special1, datastore)
            item5 = self.create_item('cheese'  , 8.00, 'unit'  , special2, datastore)
            item6 = self.create_item('corn'    , 3.27, 'weight', special6, datastore)
            item7 = self.create_item('chips'   , 4.99, 'unit'  , None, datastore)
            item8 = self.create_item('crackers', 2.68, 'unit'  , special4, datastore)
            item9 = self.create_item('butter'  , 1.99, 'unit'  , special5, datastore)
            item10= self.create_item('eggs'    , 0.89, 'unit'  , None, datastore)
            order = self.create_order(datastore)

            order.add_item(item ,  4)
            order.add_item(item2,  1)
            order.add_item(item3,  1.32)
            order.add_item(item4,  9.34)
            order.add_item(item5,  2)
            order.add_item(item6,  3.56)
            order.add_item(item7,  3)
            order.add_item(item8,  4)
            order.add_item(item9,  1)
            order.add_item(item10, 1)

            total = order.calculate_total()
            self.assertEqual(total, 147.25)

        def test_calculate_total_for_order_with_6_specials_and_10_items_with_limits(self):
            datastore = DataStore()
            special1 = {'type': 'getEOLforAoff', 'off': 25}
            special2 = {'type': 'markdown', 'price': 4.00}
            special3 = {'type': 'AforB', 'buy': 3, 'for': 5.00}
            special4 = {'type': 'buyAgetBforCoff', 'buy': 1, 'get': 1, 'off': 50}
            special5 = {'type': 'markdown', 'price': 0.72, 'limit': 5}
            special6 = {'type': 'getEOLforAoff', 'off': 35}

            item  = self.create_item('soup'    , 2.00, 'unit'  , special3, datastore)
            item2 = self.create_item('peas'    , 1.78, 'unit'  , None, datastore)
            item3 = self.create_item('chicken' , 2.37, 'weight', None, datastore)
            item4 = self.create_item('beef'    , 9.99, 'weight', special1, datastore)
            item5 = self.create_item('cheese'  , 8.00, 'unit'  , special2, datastore)
            item6 = self.create_item('corn'    , 3.27, 'weight', special6, datastore)
            item7 = self.create_item('chips'   , 4.99, 'unit'  , None, datastore)
            item8 = self.create_item('crackers', 2.68, 'unit'  , special4, datastore)
            item9 = self.create_item('butter'  , 1.99, 'unit'  , None, datastore)
            item10= self.create_item('eggs'    , 2.89, 'unit'  , special5, datastore)
            order = self.create_order(datastore)

            order.add_item(item ,  4)
            order.add_item(item2,  1)
            order.add_item(item3,  1.32)
            order.add_item(item4,  9.34)
            order.add_item(item5,  2)
            order.add_item(item6,  3.56)
            order.add_item(item7,  3)
            order.add_item(item8,  4)
            order.add_item(item9,  1)
            order.add_item(item10, 10)

            total = order.calculate_total()
            self.assertEqual(total, 172.16)

        def test_calculate_total_greedy_for_order_with_9_specials_and_10_items(self):
            datastore = DataStore()
            special1 = {'type': 'getEOLforAoff', 'off': 25}
            special2 = {'type': 'markdown', 'price': 4.00}
            special3 = {'type': 'AforB', 'buy': 3, 'for': 5.00}
            special4 = {'type': 'buyAgetBforCoff', 'buy': 1, 'get': 1, 'off': 50}
            special5 = {'type': 'markdown', 'price': 0.50}
            special6 = {'type': 'buyAgetBforCoff', 'buy': 1, 'get': 1, 'off': 100}
            special7 = {'type': 'markdown', 'price': 0.62}
            special8 = {'type': 'getEOLforAoff', 'off': 35}
            special9 = {'type': 'AforB', 'buy': 2, 'for': 3.00}


            item  = self.create_item('soup'    , 2.00, 'unit'  , special3, datastore)
            item2 = self.create_item('peas'    , 1.78, 'unit'  , special7, datastore)
            item3 = self.create_item('chicken' , 2.37, 'weight', special8, datastore)
            item4 = self.create_item('beef'    , 9.99, 'weight', special1, datastore)
            item5 = self.create_item('cheese'  , 8.00, 'unit'  , special2, datastore)
            item6 = self.create_item('corn'    , 3.27, 'unit'  , special6, datastore)
            item7 = self.create_item('chips'   , 4.99, 'unit'  , special9, datastore)
            item8 = self.create_item('crackers', 2.68, 'unit'  , special4, datastore)
            item9 = self.create_item('butter'  , 1.99, 'unit'  , special5, datastore)
            item10= self.create_item('eggs'    , 0.89, 'unit'  , None, datastore)
            order = self.create_order(datastore)

            order.add_item(item ,  4)
            order.add_item(item2,  1)
            order.add_item(item3,  1.32)
            order.add_item(item4,  9.34)
            order.add_item(item5,  2)
            order.add_item(item6,  4)
            order.add_item(item7,  3)
            order.add_item(item8,  4)
            order.add_item(item9,  1)
            order.add_item(item10, 1)

            total = order.calculate_total()
            self.assertEqual(total, 162.87)

        def test_calculate_total_greedy_for_order_with_9_specials_and_9_items(self):
            datastore = DataStore()
            special1 = {'type': 'getEOLforAoff', 'off': 25}
            special2 = {'type': 'markdown', 'price': 4.00}
            special3 = {'type': 'AforB', 'buy': 3, 'for': 5.00}
            special4 = {'type': 'buyAgetBforCoff', 'buy': 1, 'get': 1, 'off': 50, 'limit': 2}
            special5 = {'type': 'markdown', 'price': 0.22}
            special6 = {'type': 'buyAgetBforCoff', 'buy': 1, 'get': 1, 'off': 100}
            special7 = {'type': 'markdown', 'price': 0.62}
            special8 = {'type': 'getEOLforAoff', 'off': 35}
            special9 = {'type': 'AforB', 'buy': 2, 'for': 3.00}


            item  = self.create_item('soup'    , 2.00, 'unit'  , special3, datastore)
            item2 = self.create_item('peas'    , 1.78, 'unit'  , special7, datastore)
            item3 = self.create_item('chicken' , 2.37, 'weight', special1, datastore)
            item4 = self.create_item('beef'    , 9.99, 'weight', special8, datastore)
            item5 = self.create_item('cheese'  , 8.00, 'unit'  , special2, datastore)
            item6 = self.create_item('corn'    , 3.27, 'unit'  , special6, datastore)
            item7 = self.create_item('chips'   , 4.99, 'unit'  , special9, datastore)
            item8 = self.create_item('crackers', 2.68, 'unit'  , special4, datastore)
            item10= self.create_item('eggs'    , 0.89, 'unit'  , special5, datastore)
            order = self.create_order(datastore)

            order.add_item(item ,  4)
            order.add_item(item2,  1)
            order.add_item(item3,  6.32)
            order.add_item(item4,  2.34)
            order.add_item(item5,  2)
            order.add_item(item6,  4)
            order.add_item(item7,  3)
            order.add_item(item8,  4)
            order.add_item(item10, 8)

            total = order.calculate_total()
            self.assertEqual(total, 110.03)

        def create_item(self, name, price, billing_method, special, datastore):
            item = Item(name, price, billing_method, special)
            datastore.set('itemdetails:' + name, item)
            return item

        def create_order(self, datastore):
            order = MakeOrder(self.order_id, datastore)
            datastore.set('orders:' + order.order_id, order)
            return order

    return CalculateTotalTests
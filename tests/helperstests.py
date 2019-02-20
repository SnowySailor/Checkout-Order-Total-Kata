import unittest
import src.helpers as H

class HelpersTests(unittest.TestCase):
    def test_is_in_list_when_in_list_return_true(self):
        l = [1]
        self.assertTrue(H.is_in_list(l, 1))

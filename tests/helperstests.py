import unittest
import src.helpers as H

class HelpersTests(unittest.TestCase):
    def test_is_in_list_when_in_list_return_true(self):
        l = [1]
        self.assertTrue(H.is_in_list(l, 1))

    def test_is_in_list_when_not_in_list_return_false(self):
        l = [1]
        self.assertFalse(H.is_in_list(l, 2))

    def test_is_in_list_when_list_is_none_return_false(self):
        l = None
        self.assertFalse(H.is_in_list(l, 1))

    def test_is_in_list_when_list_is_empty_return_false(self):
        l = []
        self.assertFalse(H.is_in_list(l, 'test'))

    def test_is_in_list_when_list_contains_string_and_value_is_integer_no_exception_occurrs(self):
        l = ['this', 'list', 'of', 'strings']
        self.assertFalse(H.is_in_list(l, 123))

    def test_is_in_list_when_first_argument_is_not_like_a_list_exception_is_thrown(self):
        l = 123
        self.assertRaises(TypeError, H.is_in_list, l, 123)

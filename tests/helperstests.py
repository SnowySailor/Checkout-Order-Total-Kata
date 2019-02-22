import unittest
import src.helpers as H
import requests
import json

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

    def test_parse_post_vars_when_post_to_ping_with_no_data_get_back_no_data(self):
        r = requests.post('http://localhost:19546/ping')
        self.assertEqual(r.text, '{}')

    def test_parse_post_vars_when_post_to_ping_with_data_get_back_same_data(self):
        post_data = {'test': 'ing'}
        r = requests.post('http://localhost:19546/ping', data=post_data)
        self.assertEqual(r.text, json.dumps(post_data))

    def test_parse_post_vars_when_post_to_ping_with_empty_data_get_back_empty_data(self):
        post_data = {}
        r = requests.post('http://localhost:19546/ping', data=post_data)
        self.assertEqual(r.text, json.dumps(post_data))

    def test_parse_post_vars_when_post_to_ping_with_multiple_value_for_same_key_get_back_last_value(self):
        post_data = {'test': 'ing', 'test': '123'}
        r = requests.post('http://localhost:19546/ping', data=post_data)
        self.assertEqual(r.text, json.dumps({'test': '123'}))

    def test_parse_post_vars_when_post_to_ping_with_multiple_keys_and_values_get_back_same_data(self):
        post_data = {'test': 'ing', 'ing': 'test'}
        r = requests.post('http://localhost:19546/ping', data=post_data)
        self.assertEqual(r.text, json.dumps(post_data))

    def test_get_value_when_dict_is_empty_return_none(self):
        d = {}
        self.assertEqual(H.get_value(d, 'key'), None)

    def test_get_value_when_key_not_in_dict_return_none(self):
        d = {'test': 'value'}
        self.assertEqual(H.get_value(d, 'key'), None)

    def test_get_value_when_key_in_dict_return_value(self):
        d = {'test': 'value'}
        self.assertEqual(H.get_value(d, 'test'), 'value')

    def test_get_value_when_key_not_in_dict_return_default(self):
        d = {'test': 'value'}
        self.assertEqual(H.get_value(d, 'key', 'test_default'), 'test_default')

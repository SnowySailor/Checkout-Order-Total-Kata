import unittest
import src.helpers as H
import requests
import json

def MakeHelpersTests(baseurl):
    class HelpersTests(unittest.TestCase):
        # is_in_list
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

        # get_raw_post_data
        def test_get_raw_post_data_when_post_to_ping_with_no_data_get_back_no_data(self):
            r = requests.post(baseurl + '/ping')
            self.assertEqual(r.text, '{}')

        def test_get_raw_post_data_when_post_to_ping_with_data_get_back_same_data(self):
            post_data = {'test': 'ing'}
            r = requests.post(baseurl + '/ping', data=json.dumps(post_data))
            self.assertEqual(r.text, json.dumps(post_data))

        def test_get_raw_post_data_when_post_to_ping_with_empty_data_get_back_empty_data(self):
            post_data = {}
            r = requests.post(baseurl + '/ping', data=json.dumps(post_data))
            self.assertEqual(r.text, json.dumps(post_data))

        def test_get_raw_post_data_when_post_to_ping_with_multiple_value_for_same_key_get_back_last_value(self):
            post_data = {'test': 'ing', 'test': '123'}
            r = requests.post(baseurl + '/ping', data=json.dumps(post_data))
            self.assertEqual(r.text, json.dumps({'test': '123'}))

        def test_get_raw_post_data_when_post_to_ping_with_multiple_keys_and_values_get_back_same_data(self):
            post_data = {'test': 'ing', 'ing': 'test'}
            r = requests.post(baseurl + '/ping', data=json.dumps(post_data))
            self.assertEqual(r.text, json.dumps(post_data))

        # get_value
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

        def test_get_value_when_value_is_list_returns_the_list(self):
            d = {'test': ['value', 'list', 123]}
            self.assertEqual(H.get_value(d, 'test'), ['value', 'list', 123])

        def test_get_value_when_key_is_in_dict_dont_return_default_if_set(self):
            d = {'test': 'entry'}
            self.assertNotEqual(H.get_value(d, 'test', 123), 123)

        # get_path_id
        def test_get_path_id_when_path_is_empty_return_empty_string(self):
            p = ''
            self.assertEqual(H.get_path_id(p), '')

        def test_get_path_id_when_id_is_single_word_return_word(self):
            p = '/test'
            self.assertEqual(H.get_path_id(p), 'test')

        def test_get_path_id_when_path_has_multiple_words_return_last(self):
            p = '/test/1/2'
            self.assertEqual(H.get_path_id(p), '2')

        def test_get_path_id_when_path_ends_in_slash_return_empty_string(self):
            p = '/test/1/2/'
            self.assertEqual(H.get_path_id(p), '')

        def test_get_path_id_when_path_is_none_empty_string(self):
            p = None
            self.assertEqual(H.get_path_id(p), '')

        # parse_int
        def test_parse_int_when_given_string_123_returns_123(self):
            self.assertEqual(H.parse_int('123'), 123)

        def test_parse_int_when_given_none_returns_default(self):
            self.assertEqual(H.parse_int(None, 'test'), 'test')

        def test_parse_int_when_given_string_aaa_returns_default(self):
            self.assertEqual(H.parse_int('aaa'), -1)

        # parse_float
        def test_parse_float_when_given_string_123_returns_123(self):
            self.assertEqual(H.parse_float('123'), 123.0)

        def test_parse_float_when_given_none_returns_default(self):
            self.assertEqual(H.parse_float(None, 123.0), 123.0)

        def test_parse_float_when_given_string_aaa_returns_default(self):
            self.assertEqual(H.parse_float('aaa'), -1)

        # parse_json
        def test_parse_json_when_given_json_returns_same_json_as_dict(self):
            json_str = "{}"
            self.assertEqual(H.parse_json(json_str), dict())

        def test_parse_json_when_given_json_with_data_returns_json_as_dict(self):
            json_str = '{"test":123}'
            self.assertEqual(H.parse_json(json_str), {"test":123})

        def test_parse_json_when_given_invalid_json_with_data_returns_default(self):
            json_str = '{"test":123'
            self.assertEqual(H.parse_json(json_str), None)

        def test_parse_json_when_given_empty_string_returns_default(self):
            json_str = ''
            self.assertEqual(H.parse_json(json_str), None)


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

        def test_validate_special_AforB_when_buy_for_not_numbers_returns_error(self):
            special = {
                'type': 'AforB',
                'buy': 'aaa',
                'for': 'bbb'
            }
            self.assertNotEqual(H.validate_special(special, 'unit'), '')

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

        def test_validate_special_markdown_when_percentage_not_number_returns_error(self):
            special = {
                'type': 'markdown',
                'percentage': 'aaa'
            }
            self.assertNotEqual(H.validate_special(special, 'unit'), '')

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

        def test_validate_special_buyAgetBforCoff_when_buy_get_off_not_numbers_returns_error(self):
            special = {
                'type': 'buyAgetBforCoff',
                'buy': 'aaa',
                'get': 'bbb',
                'off': 'ccc'
            }
            self.assertNotEqual(H.validate_special(special, 'unit'), '')

        def test_validate_special_getEOLforAoff_with_unit_item_returns_error(self):
            special = {
                'type': 'getEOLforAoff',
                'off': 50
            }
            self.assertNotEqual(H.validate_special(special, 'unit'), '')

        def test_validate_special_getEOLforAoff_when_off_is_not_number_returns_error(self):
            special = {
                'type': 'getEOLforAoff',
                'off': 'notanumber'
            }
            self.assertNotEqual(H.validate_special(special, 'weight'), '')

        def test_validate_special_getEOLforAoff_when_off_negative_returns_error(self):
            special = {
                'type': 'getEOLforAoff',
                'off': -1
            }
            self.assertNotEqual(H.validate_special(special, 'weight'), '')

        def test_validate_integer_with_higher_value_than_expected_returns_error(self):
            self.assertNotEqual(H.validate_integer(101, 0, 100), '')

        def test_validate_float_with_higher_value_than_expected_returns_error(self):
            self.assertNotEqual(H.validate_float(101, 0, 100), '')

        def test_validate_float_with_lower_value_than_expected_returns_error(self):
            self.assertNotEqual(H.validate_float(-100, 0, 100), '')

    return HelpersTests

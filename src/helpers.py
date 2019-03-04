from cgi import parse_header, parse_multipart
from urllib.parse import parse_qsl, urlparse
import json
import sys

def is_in_list(l, v):
    if l is None:
        return False
    return v in l

def get_value(d, key, default = None):
    if d is None or key not in d:
        return default
    return d[key]

def parse_int(val, default = -1):
    try:
        return int(val)
    except TypeError:
        return default
    except ValueError:
        return default

def parse_float(val, default = -1.0):
    try:
        return float(val)
    except TypeError:
        return default
    except ValueError:
        return default

def set_response(handler, status_code, content, content_type = 'application/json'):
    handler.send_response(status_code)
    handler.send_header('Content-Type', content_type)
    handler.end_headers()
    handler.wfile.write(content.encode('utf-8'))

def get_raw_post_data(self):
    length = int(self.headers['content-length'])
    return self.rfile.read(length)

def parse_json(json_str, default = None):
    try:
        return json.loads(json_str)
    except ValueError:
        return default

def parse_url_query(path):
    query = urlparse(path).query
    return dict(parse_qsl(query))

def get_path_id(path):
    if path is None:
        return ''
    # Want to get the last value in the path
    # We want 'three' if the path is /one/two/three
    path_list = path.split('/')
    return path_list[-1]

def validate_special(special, billing_method):
    special_type = get_value(special, 'type')
    billing_method = billing_method.lower()
    msg = ''
    if special_type == 'AforB':
        if billing_method != 'unit':
            msg += 'Special can only apply to items billed by the unit. '
        buy = get_value(special, 'buy')
        f = get_value(special, 'for')
        if buy is None:
            msg += 'Must provide buy. '
        else:
            msg += validate_integer(buy, 0)
        if f is None:
            msg += 'Must provide for. '
        else:
            msg += validate_float(f, 0)
    elif special_type == 'buyAgetBforCoff':
        if billing_method != 'unit':
            msg += 'Special can only apply to items billed by the unit. '
        buy = get_value(special, 'buy')
        get = get_value(special, 'get')
        off = get_value(special, 'off')
        if buy is None:
            msg += 'Must provide buy. '
        else:
            msg += validate_integer(buy, 0)
        if get is None:
            msg += 'Must provide get. '
        else:
            msg += validate_integer(get, 0)
        if off is None:
            msg += 'Must provide off. '
        else:
            msg += validate_integer(off, 0, 100)
    elif special_type == 'getEOLforAoff':
        if billing_method != 'weight':
            msg += 'Special can only apply to items billed by weight. '
        off = get_value(special, 'off')
        if get_value(special, 'off') is None:
            msg += 'Must provide off. '
        else:
            msg += validate_integer(off, 0, 100)
    elif special_type == 'markdown':
        price = get_value(special, 'price')
        if price is None:
            msg += 'Must provide price. '
        else:
            msg += validate_float(price, 0)
    else:
        msg += 'Invalid special type. '

    # Limit validation
    limit = parse_int(get_value(special, 'limit'), None)
    if limit is not None and limit <= 0:
        msg += 'Limit must be greater than 0. '

    return msg

def validate_integer(i, low = None, high = None):
    i = parse_int(i, None)
    if i is None:
        return 'Unable to parse value to integer. '
    elif low is not None and i < low:
        return 'Value must be greater than or equal to {low}. '
    elif high is not None and i > high:
        return 'Value must be less than or equal to {high}. '
    return ''

def validate_float(i, low = None, high = None):
    i = parse_int(i, None)
    if i is None:
        return 'Unable to parse value to float. '
    elif low is not None and i < low:
        return 'Value must be greater than or equal to {low}. '
    elif high is not None and i > high:
        return 'Value must be less than or equal to {high}. '
    return ''

def flatten(*lists):
    ret = list()
    # Iterate over the lists in the arguments
    for l in lists:
        # Iterate over the items in the list
        for item in l:
            ret.append(item)
    return ret

def merge_item_dict_lists_to_dict(*lists):
    d = dict()
    # Iterate over all lists in the arguments
    for l in lists:
        # Iterate over the dicts in the list and add
        # each item to the master dict
        for item in l:
            identifier = get_value(item, 'identifier')
            quantity   = get_value(item, 'quantity')
            d[identifier] = quantity  
    return d

def has_specials(item_dict, datastore):
    for item, _ in item_dict.items():
        item_def = datastore.get('itemdetails:' + item)
        if item_def.special is not None:
            return True
    return False

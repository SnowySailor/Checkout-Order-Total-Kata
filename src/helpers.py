from cgi import parse_header, parse_multipart
from urllib.parse import parse_qsl, urlparse
import json

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
        if get_value(special, 'buy') is None:
            msg += 'Must provide buy. '
        if get_value(special, 'for') is None:
            msg += 'Must provide for. '
    elif special_type == 'buyAgetBforCoff':
        if billing_method != 'unit':
            msg += 'Special can only apply to items billed by the unit. '
        if get_value(special, 'buy') is None:
            msg += 'Must provide buy. '
        if get_value(special, 'get') is None:
            msg += 'Must provide get. '
        if get_value(special, 'off') is None:
            msg += 'Must provide off. '
    elif special_type == 'getEOLforAoff':
        if billing_method != 'weight':
            msg += 'Special can only apply to items billed by weight. '
        if get_value(special, 'off') is None:
            msg += 'Must provide off. '
    elif special_type == 'markdown':
        if get_value(special, 'percentage') is None:
            msg += 'Must provide percentage. '
    else:
        msg += 'Invalid special type. '
    return msg

from cgi import parse_header, parse_multipart
from urllib.parse import parse_qsl

def is_in_list(l, v):
    if l is None:
        return False
    return v in l

def get_value(d, key, default = None):
    if key not in d:
        return default
    return d[key]

def set_response(handler, status_code, content, content_type = 'application/json'):
    handler.send_response(status_code)
    handler.send_header('Content-Type', content_type)
    handler.end_headers()
    handler.wfile.write(content.encode('utf-8'))

def parse_post_vars(self):
    if self.headers['content-type'] is None:
        return dict()

    content_type, param_dict = parse_header(self.headers['content-type'])
    if content_type == 'application/x-www-form-urlencoded':
        # Parse url-encoded params
        length = int(self.headers['content-length'])
        encoded_vars = dict(parse_qsl(self.rfile.read(length), keep_blank_values=1, encoding='utf-8'))
    else:
        encoded_vars = dict()

    # Decode each key-value pair
    post_vars = dict()
    for key, value in encoded_vars.items():
        post_vars[key.decode('utf-8')] = value.decode('utf-8')

    return post_vars

def get_path_id(path):
    if path is None:
        return ''
    path_list = path.split('/')
    return path_list[-1]

from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json

from src.helpers import set_response, parse_post_vars, get_value, get_path_id, get_raw_post_data, parse_url_query
from src.database import DataStore
from src.models.item import Item, Methods

def MakeRequestHandler(is_testing_mode, datastore):
    class RequestHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            # Just return so the http server doesn't dump logs for each request
            return

        def do_GET(self):
            if self.path == '/ping':
                self.do_get_ping()
            elif self.path.startswith('/datastore/') and is_testing_mode:
                self.do_get_data_store()
            elif self.path.startswith('/itemdetails'):
                self.do_get_item_details()
            else:
                set_response(self, 404, '404', 'text/html')

        def do_POST(self):
            if self.path == '/ping':
                self.do_post_ping()
            elif self.path == '/datastore' and is_testing_mode: # Route only available for testing mode
                self.do_post_data_store()
            elif self.path == '/createitem':
                self.do_post_create_item()
            else:
                set_response(self, 404, '404', 'text/html')

        def do_DELETE(self):
            if self.path.startswith('/datastore/') and is_testing_mode: # Route only available for testing mode
                self.do_delete_data_store()
            else:
                set_response(self, 404, '404', 'text/html')

        # HTTP GET handlers
        def do_get_ping(self):
            set_response(self, 200, 'pong', 'text/text')

        def do_get_data_store(self):
            data_id = get_path_id(self.path)
            value = datastore.get(data_id)
            set_response(self, 200, json.dumps(value))

        def do_get_item_details(self):
            url_query = parse_url_query(self.path)
            name = get_value(url_query, 'name')
            if name is None or name == '':
                set_response(self, 400, 'Must provide name.', 'text/text')
            else:
                item = datastore.get('itemdetails:' + name, None)
                set_response(self, 200, item.to_json())


        # HTTP POST handlers
        def do_post_ping(self):
            # Read the post variables and return them to the client
            post_vars = parse_post_vars(self)
            json_resp = json.dumps(post_vars)
            set_response(self, 200, json_resp)

        def do_post_data_store(self):
            post_vars = parse_post_vars(self)
            key       = get_value(post_vars, 'key')
            value     = get_value(post_vars, 'value')

            if key is None:
                set_response(self, 400, 'Must provide key', 'text/text')
            elif value is None:
                set_response(self, 400, 'Must provide value', 'text/text')
            else:
                datastore.set(key, value)
                set_response(self, 200, '')

        def do_post_create_item(self):
            item_json = get_raw_post_data(self)
            item_dict = json.loads(item_json)

            name           = get_value(item_dict, 'name')
            price          = get_value(item_dict, 'price', 0)
            billing_method = get_value(item_dict, 'billing_method', '')
            if billing_method.lower() == 'weight':
                billing_method = Methods.WEIGHT
            else:
                billing_method = Methods.UNIT

            msg = ''
            if name is None or name == '':
                msg += 'Must provide name. '
            if price <= 0:
                msg += 'Must provide price. '

            if msg != '':
                set_response(self, 400, msg, 'text/text')
            else:
                item = Item(name, price, billing_method)
                datastore.set('itemdetails:' + item.name, item)
                set_response(self, 200, '')


        # HTTP DELETE handlers
        def do_delete_data_store(self):
            data_id = get_path_id(self.path)
            datastore.delete(data_id)
            set_response(self, 200, '')

    return RequestHandler

def run_server(is_testing_mode):
    datastore = DataStore()
    server = HTTPServer(('', 19546), MakeRequestHandler(is_testing_mode, datastore))
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    print('Started server. Listening at http://localhost:19546')

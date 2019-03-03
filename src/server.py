from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json
from urllib.parse import urlparse

from src.helpers import set_response, get_value, get_path_id,\
    get_raw_post_data, parse_url_query, parse_int, parse_float,\
    parse_json, validate_special
from src.database import DataStore
from src.models.item import Item, Methods
from src.models.order import MakeOrder

def MakeRequestHandler(is_testing_mode, datastore):
    class RequestHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            # Just return so the http server doesn't dump logs for each request
            return

        def do_GET(self):
            path = urlparse(self.path).path
            if path == '/ping':
                self.do_get_ping()
            elif path.startswith('/datastore/') and is_testing_mode:
                self.do_get_data_store()
            elif path == '/itemdetails':
                self.do_get_item_details()
            elif path == '/getorder':
                self.do_get_order()
            else:
                set_response(self, 404, '404', 'text/html')

        def do_POST(self):
            path = urlparse(self.path).path
            if path == '/ping':
                self.do_post_ping()
            elif path == '/datastore' and is_testing_mode: # Route only available for testing mode
                self.do_post_data_store()
            elif path == '/createitem':
                self.do_post_create_item()
            elif path == '/createorder':
                self.do_post_create_order()
            elif path == '/additemtoorder':
                self.do_post_add_item_to_order()
            elif path == '/removeitemfromorder':
                self.do_post_remove_item_from_order()
            else:
                set_response(self, 404, '404', 'text/html')

        def do_DELETE(self):
            path = urlparse(self.path).path
            if path.startswith('/datastore/') and is_testing_mode: # Route only available for testing mode
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
            # Ensure that the client provided a name to look up
            if name is None or name == '':
                set_response(self, 400, 'Must provide name.', 'text/text')
            else:
                item = datastore.get('itemdetails:' + name, None)
                if item is not None:
                    # Return the item to the user as json
                    set_response(self, 200, item.to_json())
                else:
                    # If the name isn't a name from an item, tell the client there
                    # was a problem
                    set_response(self, 400, 'Item does not exist.', 'text/text')

        def do_get_order(self):
            url_query = parse_url_query(self.path)
            order_id = get_value(url_query, 'id')
            if order_id is None or order_id == '':
                set_response(self, 400, 'Must provide order id')
            else:
                order = datastore.get('orders:' + order_id)
                if order is None:
                    set_response(self, 400, 'Order does not exist.')
                else:
                    set_response(self, 200, order.to_json())


        # HTTP POST handlers
        def do_post_ping(self):
            # Read the post variables and return them to the client
            post_data = get_raw_post_data(self)
            post_dict = parse_json(post_data, dict())
            json_resp = json.dumps(post_dict)
            set_response(self, 200, json_resp)

        def do_post_data_store(self):
            post_data = get_raw_post_data(self)
            post_dict = parse_json(post_data)
            key       = get_value(post_dict, 'key')
            value     = get_value(post_dict, 'value')

            if key is None:
                set_response(self, 400, 'Must provide key', 'text/text')
            elif value is None:
                set_response(self, 400, 'Must provide value', 'text/text')
            else:
                datastore.set(key, value)
                set_response(self, 200, '')

        def do_post_create_item(self):
            post_data = get_raw_post_data(self)
            item_dict = parse_json(post_data)

            # Pull out all of the fields we need
            name           = get_value(item_dict, 'name')
            price          = parse_float(get_value(item_dict, 'price', 0))
            billing_method = get_value(item_dict, 'billing_method', '')
            special        = get_value(item_dict, 'special')

            # Ensure that all necessary data is present
            msg = ''
            if name is None or name == '':
                msg += 'Must provide name. '
            if price is None or price <= 0:
                msg += 'Must provide price and must be positive. '

            if msg != '':
                set_response(self, 400, msg, 'text/text')
            else:
                # Check to see if the provided special is valid
                if special is not None:
                    msg = validate_special(special, billing_method)
                if msg != '':
                    set_response(self, 400, msg, 'text/text')
                else:
                    # Create and store the item and tell the user everything is fine
                    item = Item(name, price, billing_method, special)
                    datastore.set('itemdetails:' + item.name, item)
                    set_response(self, 200, '')

        def do_post_create_order(self):
            post_data = get_raw_post_data(self)
            post_dict = parse_json(post_data)
            order_id  = get_value(post_dict, 'id')
            # Ensure the client provided an id to create
            if order_id is None or order_id == '':
                set_response(self, 400, 'Must provide id.', 'text/text')
            else:
                # If the order already exists, we don't want to overwrite it
                # Instead, tell the user that there was a problem
                if datastore.get('orders:' + order_id) is None:
                    order = MakeOrder(order_id, datastore)
                    datastore.set('orders:' + order_id, order)
                    set_response(self, 200, '')
                else:
                    set_response(self, 400, 'Order with that id already exists.', 'text/text')

        def do_post_add_item_to_order(self):
            post_data = get_raw_post_data(self)
            post_dict = parse_json(post_data)
            order_id  = get_value(post_dict, 'order_id')
            item_name = get_value(post_dict, 'item')

            msg = ''
            if order_id is None or order_id == '':
                msg += 'Must provide order_id. '
            if item_name is None:
                msg += 'Must provide item. '

            if msg != '':
                set_response(self, 400, msg, 'text/text')
            else:
                order = datastore.get('orders:' + order_id)
                item  = datastore.get('itemdetails:' + item_name)

                if order is None:
                    set_response(self, 400, 'Order does not exist.', 'text/text')
                elif item is None:
                    set_response(self, 400, 'Item does not exist.', 'text/text')
                else:
                    # If the item is a UNIT type, we only want to allow integers
                    # for the amount since it doesn't make sense to have something
                    # like 1.25 cans of soup
                    amount = parse_float(get_value(post_dict, 'amount'), 1.0)
                    if item.billing_method == Methods.UNIT:
                        amount = parse_int(amount)

                    order.add_item(item, amount)
                    set_response(self, 200, '')

        def do_post_remove_item_from_order(self):
            post_data = get_raw_post_data(self)
            post_dict = parse_json(post_data)
            order_id  = get_value(post_dict, 'order_id')
            item_name = get_value(post_dict, 'item')

            msg = ''
            if order_id is None or order_id == '':
                msg += 'Must provide order_id. '
            if item_name is None or item_name == '':
                msg += 'Must provide item. '

            if msg != '':
                set_response(self, 400, msg, 'text/text')
            else:
                item  = datastore.get('itemdetails:' + item_name)
                order = datastore.get('orders:' + order_id)
                if order is None:
                    set_response(self, 400, 'Order does not exist.', 'text/text')
                elif item is None:
                    set_response(self, 400, 'Item does not exist.', 'text/text')
                elif get_value(order.items, item_name) is None:
                    set_response(self, 400, 'Order does not contain provided item.', 'text/text')
                else:
                    # If the item is a UNIT type, we only want to allow integers
                    # for the amount since it doesn't make sense to have something
                    # like 1.25 cans of soup
                    amount = parse_float(get_value(post_dict, 'amount'), 1.0)
                    if item.billing_method == Methods.UNIT:
                        amount = parse_int(amount)

                    order.remove_item(item, amount)
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

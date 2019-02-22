from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json

from src.helpers import set_response, parse_post_vars, get_value

def MakeRequestHandler(is_testing_mode):
    class RequestHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            # Just return so the http server doesn't dump logs for each request
            return

        def do_GET(self):
            if self.path == '/ping':
                self.do_get_ping()
            elif self.path.startswith('/datastore'):
                self.do_get_data_store()
            else:
                set_response(self, 404, '404', 'text/html')

        def do_POST(self):
            if self.path == '/ping':
                self.do_post_ping()
            elif self.path == '/datastore' and is_testing_mode: # Route only available for testing mode
                self.do_post_data_store()
            else:
                set_response(self, 404, '404', 'text/html')

        # HTTP GET handlers
        def do_get_ping(self):
            set_response(self, 200, 'pong', 'text/text')

        def do_get_data_store(self):
            set_response(self, 200, 'null', 'application/json')


        # HTTP POST handlers
        def do_post_ping(self):
            # Read the post variables and return them to the client
            post_vars = parse_post_vars(self)
            json_resp = json.dumps(post_vars)
            set_response(self, 200, json_resp, 'application/json')

        def do_post_data_store(self):
            post_vars = parse_post_vars(self)
            if get_value(post_vars, 'key') is None:
                set_response(self, 400, 'Must provide "key"', 'text/text')
            elif get_value(post_vars, 'value') is None:
                set_response(self, 400, 'Must provide "value"', 'text/text')
            else:
                set_response(self, 200, '', 'application/json')

    return RequestHandler

def run_server(is_testing_mode):
    server = HTTPServer(('', 19546), MakeRequestHandler(is_testing_mode))
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    print('Started server. Listening at http://localhost:19546')

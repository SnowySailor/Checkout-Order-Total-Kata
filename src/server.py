from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

from src.helpers import set_response

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/ping':
            self.do_get_ping()
        else:
            set_response(self, 404, '404', 'text/html')

    def do_get_ping(self):
        set_response(self, 200, 'pong', 'text/text')

def run_server():
    server = HTTPServer(('', 19546), RequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    print('Started server. Listening at http://localhost:19546')

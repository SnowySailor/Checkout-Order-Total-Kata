from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/ping':
            self.do_get_ping()
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.wfile.write('404'.encode('utf-8'))
            self.end_headers()

    def do_get_ping(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/text')
        self.end_headers()
        self.wfile.write('pong'.encode('utf-8'))

def run_server():
    server = HTTPServer(('', 19546), RequestHandler)
    threading.Thread(target=server.serve_forever).start()

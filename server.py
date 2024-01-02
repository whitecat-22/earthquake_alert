from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import sendslack
import sendx

address = ('0.0.0.0', 8000)

class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        parsed_path = urlparse(self.path)
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'Hello from do_GET')

    def do_POST(self):

        parsed_path = urlparse(self.path)
        content_length = int(self.headers['content-length'])

        json_data = '{}'.format((self.rfile.read(content_length).decode('utf-8')))
        sendslack.format_text(json_data)
        sendx.format_text(json_data)

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'Hello from do_POST')

with HTTPServer(address, MyHTTPRequestHandler) as server:
    server.serve_forever()

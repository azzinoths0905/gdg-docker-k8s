from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
# import sys


class CORSRequestHandler (SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


if __name__ == '__main__':
    server = ThreadedHTTPServer(('localhost', 8088), CORSRequestHandler)
    server.serve_forever()

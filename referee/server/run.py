import http.server

def run(server_class=http.server.HTTPServer, handler_class=http.server.BaseHTTPRequestHandler):
    port = 8000
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('now listening on localhost:{}'.format(port))
    httpd.serve_forever()

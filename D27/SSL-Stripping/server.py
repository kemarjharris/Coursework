from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import HTTPSConnection
from urllib import parse
import sys

class Server(BaseHTTPRequestHandler):

    def __init__(self, filepath, *args, **kwargs):
            self.filepath = filepath
            super().__init__(*args, **kwargs)

# =============================================
# ========= write your code below  ============
# =============================================

    # GET request handler 
    def do_GET(self):

        # retrieve the path from the HTTP request
        path = self.path

        # retrieve the headers from the HTTP request
        headers = self.headers
        # retrieve the body from the HTTP request
        body = None
        if (self.headers.get('content-length') != None):
            body = self.rfile.read(int(self.headers.get('content-length')))

        # send an HTTP request to another server and get the response
        conn = HTTPSConnection(headers.get("Host"))
        method = 'GET'
        conn.request(method, path, body, headers)
        # and get the response back 
        res = conn.getresponse()
        resBody = res.read(int(res.headers.get('content-length')))
        conn.close()

        # flag extraction
        if (path == "/check"):
            flag = resBody.decode("utf-8")
            with open(self.filepath, "w") as fp:
                fp.write(flag)
                sys.exit(0)

        # set HTTP response status code and body
        self.send_response(res.status, res.reason)
        # set HTTP reponse headers
        for x in res.headers.keys():
            self.send_header(x, res.headers.get(x))
        self.end_headers()

        self.wfile.write(resBody)

    # POST request handler 
    def do_POST(self):
        # retrieve the path from the HTTP request
        path = self.path
        # retrieve the headers from the HTTP request
        headers = self.headers
        # retrieve the body from the HTTP request
        params = None
        if (self.headers.get('content-length') != None):
            body = self.rfile.read(int(self.headers.get('content-length')))
            params = parse.parse_qs(body.decode("utf-8"))
            params = parse.urlencode({x : params[x][0] for x in params})

        # send an HTTP request to another server and get the response
        conn = HTTPSConnection(headers.get("Host"))
        method = 'POST'
        
        conn.request(method, path, params, headers)
        res = conn.getresponse()
        resBody = res.read(int(res.headers.get('content-length')))
        conn.close()
        # set HTTP response status code and body
        self.send_response(res.status, res.reason)
        # set HTTP reponse headers
        for x in res.headers.keys():
            self.send_header(x, res.headers.get(x))
        self.end_headers()
        self.wfile.write(resBody)

      
    # PUT request handler     
    def do_PUT(self):
        # retrieve the path from the HTTP request
        path = self.path
        # retrieve the headers from the HTTP request
        headers = self.headers
        # retrieve the body from the HTTP request
        params = None
        if (self.headers.get('content-length') != None):
            body = self.rfile.read(int(self.headers.get('content-length')))
            params = parse.parse_qs(body.decode("utf-8"))
            params = parse.urlencode({x : params[x][0] for x in params})

        # send an HTTP request to another server and get the response
        conn = HTTPSConnection(headers.get("Host"))
        method = 'PUT'
        
        conn.request(method, path, params, headers)
        res = conn.getresponse()
        resBody = res.read(int(res.headers.get('content-length')))
        conn.close()
        # set HTTP response status code and body
        self.send_response(res.status, res.reason)
        # set HTTP reponse headers
        for x in res.headers.keys():
            self.send_header(x, res.headers.get(x))
        self.end_headers()
        self.wfile.write(resBody)
        

# =============================================
# ===== do not modify the code below ==========
# =============================================
        
def run_server(filepath):
    handler = partial(Server, filepath)
    httpd = HTTPServer(('', 8080), handler)
    httpd.serve_forever()
    
if __name__ == "__main__":
    import os, sys, getopt
    def usage():
       print ('Usage:    ' + os.path.basename(__file__) + ' filepath ')
       sys.exit(2)
    # extract parameters
    try:
         opts, args = getopt.getopt(sys.argv[1:],"h",["help"])
    except getopt.GetoptError as err:
         print(err)
         usage()
         sys.exit(2)
    filepath = args[0] if len(args) > 0 else None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
           usage()
    if (filepath is None):
        print('filepath is missing\n')
        usage()
    # run the command
    run_server(filepath)
import http.server
import socketserver
import urllib
import cgi
from threading import Thread
from txn2 import test_send_algo_txn

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("do_GET(): path=", self.path)
        if self.path == '/':
            self.path = '/htdocs/'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    def do_POST(self):
        print("do_POST(): path=", self.path)
        if self.path == '/send':
            form = cgi.FieldStorage(
                fp = self.rfile,
                headers = self.headers,
                environ = {
                    "REQUEST_METHOD" : "POST",
                    "CONTENT_TYPE" : self.headers["Content-Type"]
                }
            )

            post_dict = {}
            for key in form:
                post_dict[key] = form[key].value

            print(post_dict['amount'])
            thr = Thread(
                target = test_send_algo_txn, 
                args = (
                    post_dict['senderKey'], 
                    post_dict['sender'], 
                    post_dict['receiver'], 
                    float(post_dict['amount'])
                )
            )
            thr.start()
            # test_send_algo_txn(
            #     post_dict['senderKey'], 
            #     post_dict['sender'], 
            #     post_dict['receiver'], 
            #     float(post_dict['amount'])
            # )
            return post_dict['sender']

# Create an object of the above class
handler_object = MyHttpRequestHandler

PORT = 9000
my_server = socketserver.TCPServer(("", PORT), handler_object)
print("Server object created.")
# Star the server
my_server.serve_forever()

import http.server
import socketserver
import urllib
import cgi
from threading import Thread
from main_module import *
global algod_client, creator_private_key, app_id

STAKE_CREATOR="IXY7TNLQ75CBIB3UKLHK5GQBLITR5FFWD3MYJOOCXAILJ36VM344YVQAS4"

def create_stake(stakeholder_address, stakeholder_mnemonic, amount):
    print("--------------------------------------------")
    print("Calling Counter application......")
    app_args = ["Add"]
    amountInMicroAlgo = int(float(amount) * 1000000)
    call_app(algod_client, stakeholder_address, stakeholder_mnemonic, amountInMicroAlgo, app_id, app_args)
    # read global state of application
    global_state = read_global_state(algod_client, account.address_from_private_key(creator_private_key), app_id)
    global_counter = global_state['Count']
    print("Global state:", global_counter)

    return global_counter

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
            """
            thr = Thread(
                target = change_global_counter, 
                args = (
                    post_dict['stakeholder'], 
                    post_dict['stakeholderKey'], 
                    float(post_dict['amount'])
                )
            )
            thr.start()
            """
            return create_stake(
                post_dict['stakeholder'], 
                post_dict['stakeholderMnemonic'], 
                float(post_dict['amount'])
            )
 
# Create an object of the above class
handler_object = MyHttpRequestHandler

PORT = 9000
my_server = socketserver.TCPServer(("", PORT), handler_object)
print("Server object created.")

algod_client, app_id, creator_private_key = main_func()
print("Algorand Client Initialized: ",app_id, creator_private_key)

# Star the server
my_server.serve_forever()

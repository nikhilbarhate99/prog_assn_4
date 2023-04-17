import argparse
import json
import grpc
from grpc_files import buyer_pb2
from grpc_files import buyer_pb2_grpc
from google.protobuf.json_format import Parse, ParseDict, MessageToDict, MessageToJson
from suds.client import Client
from http.server import BaseHTTPRequestHandler, HTTPServer

from global_variables import *

import random


"""
generate stubs:

python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. buyer.proto


"""

class BuyerServer:

    def create_buyer(self, request_json, customer_db_stub_list, product_db_stub_list):

        customer_db_stub = random.choice(customer_db_stub_list)
        product_db_stub = random.choice(product_db_stub_list)

        user = ParseDict(request_json, buyer_pb2.BuyerUser())
        response = customer_db_stub.create_buyer(user)
        response = MessageToDict(response, including_default_value_fields=True)
        return response

    def login_buyer(self, request_json, customer_db_stub_list, product_db_stub_list):

        customer_db_stub = random.choice(customer_db_stub_list)
        product_db_stub = random.choice(product_db_stub_list)

        user = ParseDict(request_json, buyer_pb2.BuyerUser())
        response = customer_db_stub.login_buyer(user)
        response = MessageToDict(response, including_default_value_fields=True)
        return response
        
    def logout_buyer(self, request_json, customer_db_stub_list, product_db_stub_list):

        customer_db_stub = random.choice(customer_db_stub_list)
        product_db_stub = random.choice(product_db_stub_list)

        user = ParseDict(request_json, buyer_pb2.BuyerUser())
        response = customer_db_stub.logout_buyer(user)
        response = MessageToDict(response, including_default_value_fields=True)
        return response

    def add_cart(self, request_json, customer_db_stub_list, product_db_stub_list):

        customer_db_stub = random.choice(customer_db_stub_list)
        product_db_stub = random.choice(product_db_stub_list)

        login_status = self.check_buyer_login_status({'username' : request_json['username']}, 
                            customer_db_stub_list, product_db_stub_list)['success']        
        if login_status:
            user = ParseDict(request_json, buyer_pb2.CartItem())
            response = customer_db_stub.add_cart(user)
            response = MessageToDict(response, including_default_value_fields=True)
        else:
            response = {"success": False, "message": "user not logged in"}

        return response

    def display_cart(self, request_json, customer_db_stub_list, product_db_stub_list):

        customer_db_stub = random.choice(customer_db_stub_list)
        product_db_stub = random.choice(product_db_stub_list)

        login_status = self.check_buyer_login_status({'username' : request_json['username']}, 
                            customer_db_stub_list, product_db_stub_list)['success']        
        if login_status:
            user = ParseDict(request_json, buyer_pb2.BuyerUser())
            response = customer_db_stub.display_cart(user)
            response = MessageToDict(response, including_default_value_fields=True)
        else:
            response = {"success": False, "message": "user not logged in"}

        return response

    def clear_cart(self, request_json, customer_db_stub_list, product_db_stub_list):

        customer_db_stub = random.choice(customer_db_stub_list)
        product_db_stub = random.choice(product_db_stub_list)

        login_status = self.check_buyer_login_status({'username' : request_json['username']}, 
                            customer_db_stub_list, product_db_stub_list)['success']        
        if login_status:
            user = ParseDict(request_json, buyer_pb2.BuyerUser())
            response = customer_db_stub.clear_cart(user)
            response = MessageToDict(response, including_default_value_fields=True)
        else:
            response = {"success": False, "message": "user not logged in"}
        
        return response

    def remove_cart(self, request_json, customer_db_stub_list, product_db_stub_list):
        
        customer_db_stub = random.choice(customer_db_stub_list)
        product_db_stub = random.choice(product_db_stub_list)

        login_status = self.check_buyer_login_status({'username' : request_json['username']}, 
                            customer_db_stub_list, product_db_stub_list)['success']  
        if login_status:
            user = ParseDict(request_json, buyer_pb2.CartItem())
            response = customer_db_stub.remove_cart(user)
            response = MessageToDict(response, including_default_value_fields=True)
        else:
            response = {"success": False, "message": "user not logged in"}

        return response
        
    def search(self, request_json, customer_db_stub_list, product_db_stub_list):
        
        customer_db_stub = random.choice(customer_db_stub_list)
        product_db_stub = random.choice(product_db_stub_list)

        login_status = self.check_buyer_login_status({'username' : request_json['username']}, 
                            customer_db_stub_list, product_db_stub_list)['success']  
        if login_status:
            
            user = ParseDict(request_json, buyer_pb2.BuyerSearchQuery())

            response = product_db_stub.search(user)
            response = MessageToDict(response, including_default_value_fields=True)
        else:
            response = {"success": False, "message": "user not logged in"}

        return response
    
    def get_purchase_history(self, request_json, customer_db_stub_list, product_db_stub_list):

        customer_db_stub = random.choice(customer_db_stub_list)
        product_db_stub = random.choice(product_db_stub_list)

        login_status = self.check_buyer_login_status({'username' : request_json['username']}, 
                            customer_db_stub_list, product_db_stub_list)['success']  
        if login_status:
            user = ParseDict(request_json, buyer_pb2.BuyerUser())
            response = customer_db_stub.get_purchase_history(user)
            response = MessageToDict(response, including_default_value_fields=True)
        else:
            response = {"success": False, "message": "user not logged in"}

        return response
    
    def get_seller_rating(self, request_json, customer_db_stub_list, product_db_stub_list):

        customer_db_stub = random.choice(customer_db_stub_list)
        product_db_stub = random.choice(product_db_stub_list)

        user = ParseDict(request_json, buyer_pb2.BuyerUser())
        response = customer_db_stub.get_seller_rating(user)
        response = MessageToDict(response, including_default_value_fields=True)
        return response

    def check_buyer_login_status(self, request_json, customer_db_stub_list, product_db_stub_list):

        customer_db_stub = random.choice(customer_db_stub_list)
        product_db_stub = random.choice(product_db_stub_list)

        user = ParseDict(request_json, buyer_pb2.BuyerUser())
        response = customer_db_stub.check_buyer_login_status(user)
        response = MessageToDict(response, including_default_value_fields=True)
        return response



    def make_purchase(self, request_json, customer_db_stub_list, product_db_stub_list):

        customer_db_stub = random.choice(customer_db_stub_list)
        product_db_stub = random.choice(product_db_stub_list)

        login_status = self.check_buyer_login_status({'username' : request_json['username']}, 
                            customer_db_stub_list, product_db_stub_list)['success']  
        if not login_status:
         return {"success": False, "message": "user not logged in"}
        
        url = 'http://' + FINANCIAL_TRANSACTION_HOST + ':' + FINANCIAL_TRANSACTION_PORT + '/?wsdl'
        client = Client(url)
        
        username=request_json['username']
        creditcard=request_json['creditcard']

        transaction_success = client.service.get_yes_or_no(creditcard, username)

        ### transaction_success = random.random() < 0.9

        if transaction_success:
            cart_request = {'username': request_json['username']}
            
            cart_response = self.display_cart(cart_request, customer_db_stub_list, product_db_stub_list)
            self.clear_cart(cart_request, customer_db_stub_list, product_db_stub_list)

            for prod_id, quantity in cart_response['cart'].items():
                purchase_request = {'username': request_json['username'], 'prod_id': prod_id, 'quantity' : quantity}
                
                cart_item = ParseDict(purchase_request, buyer_pb2.CartItem())
                response = customer_db_stub.add_purchase(cart_item)
                response = MessageToDict(response, including_default_value_fields=True)

                cart_item = ParseDict(purchase_request, buyer_pb2.CartItem())
                response = product_db_stub.remove_purchase_item(cart_item)
                response = MessageToDict(response, including_default_value_fields=True)
            
            return {"success": True, "message": "purchase completed"}


        return {"success": False, "message": "purchase failed"}
    
    

class BuyerRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):

        server = BuyerServer()      

        customer_db_channel_list = []
        customer_db_stub_list = []
        for host, port in CUSTOMER_DB_LIST[:CUSTOMER_DB_N]:
            customer_db_channel_list.append(grpc.insecure_channel(host + ':' + port))
            customer_db_stub_list.append(buyer_pb2_grpc.BuyerStub(customer_db_channel_list[-1]))


        product_db_channel_list = []
        product_db_stub_list = []
        for host, port in PRODUCT_DB_LIST[:PRODUCT_DB_N]:
            product_db_channel_list.append(grpc.insecure_channel(host + ':' + port))
            product_db_stub_list.append(buyer_pb2_grpc.BuyerStub(product_db_channel_list[-1]))



        content_length = int(self.headers['Content-Length'])
        request_str = self.rfile.read(content_length).decode('utf-8')
        
        request = json.loads(request_str)
        action = request.get("action")
        request.pop("action")

        #print(action)

        if action == "create_buyer":
            response = server.create_buyer(request, customer_db_stub_list, product_db_stub_list)
        elif action == "login_buyer":
            response = server.login_buyer(request, customer_db_stub_list, product_db_stub_list)
        elif action == "logout_buyer":
            response = server.logout_buyer(request, customer_db_stub_list, product_db_stub_list)
        elif action == "add_to_cart":
            response = server.add_cart(request, customer_db_stub_list, product_db_stub_list)
        elif action == "remove_cart":
            response = server.remove_cart(request, customer_db_stub_list, product_db_stub_list)
        elif action == "display_cart":
            response = server.display_cart(request, customer_db_stub_list, product_db_stub_list)
        elif action == "clear_cart":
            response = server.clear_cart(request, customer_db_stub_list, product_db_stub_list)    
        elif action == "search":
            response = server.search(request, customer_db_stub_list, product_db_stub_list)
        elif action == "get_purchase_history":
            response = server.get_purchase_history(request, customer_db_stub_list, product_db_stub_list)
        elif action == "get_seller_rating":
            response = server.get_seller_rating(request, customer_db_stub_list, product_db_stub_list)
        elif action == "make_purchase":
            response = server.make_purchase(request, customer_db_stub_list, product_db_stub_list)
        else:
            response = {"success": False, "message": "Invalid action"}

        self.send_json_response(response)

    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())



def start_server(args):

    node_id = args.node_id

    assert node_id < BUYER_SERVER_N, 'max node id BUYER_SERVER_N - 1'

    host, port = BUYER_SERVER_LIST[node_id]
    port = int(port)

    httpd = HTTPServer((host, port), BuyerRequestHandler)
    print("=============================")
    print("Server running")
    print("Server type: BUYER SERVER")
    print("node id:", node_id)
    print(host, port)
    print("=============================")

    httpd.serve_forever()
    
    print("=============================")
    print("Server shutdown")
    print("=============================")



    # server = BuyerServer()
    
    # customer_db_channel_list = []
    # customer_db_stub_list = []
    # for host, port in CUSTOMER_DB_LIST[:CUSTOMER_DB_N]:
    #     customer_db_channel_list.append(grpc.insecure_channel(host + ':' + port))
    #     customer_db_stub_list.append(buyer_pb2_grpc.BuyerStub(customer_db_channel_list[-1]))

    # product_db_channel_list = []
    # product_db_stub_list = []
    # for host, port in PRODUCT_DB_LIST[:PRODUCT_DB_N]:
    #     product_db_channel_list.append(grpc.insecure_channel(host + ':' + port))
    #     product_db_stub_list.append(buyer_pb2_grpc.BuyerStub(product_db_channel_list[-1]))
        

    # add_dummy_data(server, customer_db_stub_list, product_db_stub_list)





#########################################################################
#### Testing functions
#########################################################################


#########################################################################

def add_dummy_data(server, customer_db_stub, product_db_stub):

    print("=============================")

    request = {"action": "create_buyer", 
               "username": "usr1",
               "password": "pw1",
               "name" : "name1",
               }


    action = request.get("action")
    print(action)
    response = handle_request(server, request, customer_db_stub, product_db_stub)
    print(type(response))
    print(response)

    print("=============================")

    request = {"action": "create_buyer", 
               "username": "usr2",
               "password": "pw2",
               "name" : "name2",
               }


    action = request.get("action")
    print(action)
    response = handle_request(server, request, customer_db_stub, product_db_stub)
    print(type(response))
    print(response)

    print("=============================")

    request = {"action": "create_buyer", 
               "username": "usr2",
               "password": "pw2",
               "name" : "name2",
               }

    action = request.get("action")
    print(action)
    response = handle_request(server, request, customer_db_stub, product_db_stub)
    print(type(response))
    print(response)



    print("=============================")

    request = {"action": "login_buyer", 
               "username": "usr1",
               "password": "pw1",
               "name" : "name2",
               }

    action = request.get("action")
    print(action)
    response = handle_request(server, request, customer_db_stub, product_db_stub)
    print(type(response))
    print(response)



    print("=============================")

    request = {"action": "login_buyer", 
               "username": "usr2",
               "password": "pw2",
               "name" : "name2",
               }

    action = request.get("action")
    print(action)
    response = handle_request(server, request, customer_db_stub, product_db_stub)
    print(type(response))
    print(response)



    print("=============================")

    request = {"action": "add_to_cart",
               "username": "usr2", 
               "prod_id": 1,
               "quantity": 2,
               }

    action = request.get("action")
    print(action)
    response = handle_request(server, request, customer_db_stub, product_db_stub)
    print(type(response))
    print(response)



    print("=============================")

    request = {"action": "add_to_cart",
               "username": "usr2", 
               "prod_id": 2,
               "quantity": 2,
               }


    action = request.get("action")
    print(action)
    response = handle_request(server, request, customer_db_stub, product_db_stub)
    print(type(response))
    print(response)



    print("=============================")

    request = {"action": "make_purchase", 
               "username": "usr2",
               "creditcard": "123456789",
               }

 
    action = request.get("action")
    print(action)
    response = handle_request(server, request, customer_db_stub, product_db_stub)
    print(type(response))
    print(response)



    print("=============================")

    request = {"action": "get_purchase_history", 
               "username": "usr2",
               }

 
    action = request.get("action")
    print(action)
    response = handle_request(server, request, customer_db_stub, product_db_stub)
    print(type(response))
    print(response)


## FOR TESTING ONLY
def handle_request(server, request, customer_db_stub, product_db_stub):

    action = request.get("action")
    request.pop("action")
    if action == "create_buyer":
        response = server.create_buyer(request, customer_db_stub, product_db_stub)
    elif action == "login_buyer":
        response = server.login_buyer(request, customer_db_stub, product_db_stub)
    elif action == "logout_buyer":
        response = server.logout_buyer(request, customer_db_stub, product_db_stub)
    elif action == "add_to_cart":
        response = server.add_cart(request, customer_db_stub, product_db_stub)
    elif action == "remove_cart":
        response = server.remove_cart(request, customer_db_stub, product_db_stub)
    elif action == "display_cart":
        response = server.display_cart(request, customer_db_stub, product_db_stub)
    elif action == "clear_cart":
        response = server.clear_cart(request, customer_db_stub, product_db_stub)    
    elif action == "search":
        response = server.search(request, customer_db_stub, product_db_stub)
    elif action == "get_purchase_history":
        response = server.get_purchase_history(request, customer_db_stub, product_db_stub)
    elif action == "get_seller_rating":
        response = server.get_seller_rating(request, customer_db_stub, product_db_stub)
    elif action == "make_purchase":
        response = server.make_purchase(request, customer_db_stub, product_db_stub)
    else:
        response = {"success": False, "message": "Invalid action"}
        
    return response







##########################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--node_id', type=int, default=0)
    args = parser.parse_args()

    start_server(args)




import json
import grpc
from grpc_files import seller_pb2
from grpc_files import seller_pb2_grpc
from google.protobuf.json_format import Parse, ParseDict, MessageToDict, MessageToJson
from http.server import BaseHTTPRequestHandler, HTTPServer


# Global Variables

BUYER_SERVER_HOST = '127.0.0.1'
BUYER_SERVER_PORT = 10000

SELLER_SERVER_HOST = '127.0.0.1'
SELLER_SERVER_PORT = 10001

PRODUCT_DB_HOST = '127.0.0.1'
PRODUCT_DB_PORT = '10002'

CUSTOMER_DB_HOST = '127.0.0.1'
CUSTOMER_DB_PORT = '10003'

FINANCIAL_TRANSACTION_HOST = '127.0.0.1'
FINANCIAL_TRANSACTION_PORT = '10005'


"""
generate stubs:

python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. seller.proto


"""

class SellerServer:

    def create_seller(self, request_json, customer_db_stub, product_db_stub):        
        user = ParseDict(request_json, seller_pb2.SellerUser())
        response = customer_db_stub.create_seller(user)
        response = MessageToDict(response, including_default_value_fields=True)
        return response


    def login_seller(self, request_json, customer_db_stub, product_db_stub):
        user = ParseDict(request_json, seller_pb2.SellerUser())
        response = customer_db_stub.login_seller(user)
        response = MessageToDict(response, including_default_value_fields=True)
        return response 


    def logout_seller(self, request_json, customer_db_stub, product_db_stub):
        user = ParseDict(request_json, seller_pb2.SellerUser())
        response = customer_db_stub.logout_seller(user)
        response = MessageToDict(response, including_default_value_fields=True)
        return response
    

    def get_seller_rating(self, request_json, customer_db_stub, product_db_stub):
        user = ParseDict(request_json, seller_pb2.SellerUser())
        response = customer_db_stub.get_seller_rating(user)
        response = MessageToDict(response, including_default_value_fields=True)
        return response


    def add_item(self, request_json, customer_db_stub, product_db_stub):

        login_status = self.check_seller_login_status({'username' : request_json['username']}, 
                            customer_db_stub, product_db_stub)['success']        
        if login_status:
            query = ParseDict(request_json, seller_pb2.SellerQuery())
            response = product_db_stub.add_item(query)
            response = MessageToDict(response, including_default_value_fields=True)
        else:
            response = {"success": False, "message": "user not logged in"}

        return response 


    def remove_item(self, request_json, customer_db_stub, product_db_stub):

        login_status = self.check_seller_login_status({'username' : request_json['username']}, 
                            customer_db_stub, product_db_stub)['success']        
        if login_status:
            query = ParseDict(request_json, seller_pb2.SellerQuery())
            response = product_db_stub.remove_item(query)
            response = MessageToDict(response, including_default_value_fields=True)
        else:
            response = {"success": False, "message": "user not logged in"}
        
        return response 


    def change_price(self, request_json, customer_db_stub, product_db_stub):

        login_status = self.check_seller_login_status({'username' : request_json['username']}, 
                            customer_db_stub, product_db_stub)['success']        
        if login_status:
            query = ParseDict(request_json, seller_pb2.SellerQuery())
            response = product_db_stub.change_price(query)
            response = MessageToDict(response, including_default_value_fields=True)
        else:
            response = {"success": False, "message": "user not logged in"}
        
        return response


    def all_items_by_seller(self, request_json, customer_db_stub, product_db_stub):

        login_status = self.check_seller_login_status({'username' : request_json['username']}, 
                            customer_db_stub, product_db_stub)['success']        
        if login_status:
            user = ParseDict(request_json, seller_pb2.SellerUser())
            response = product_db_stub.all_items_by_seller(user)
            response = MessageToDict(response, including_default_value_fields=True)
        else:
            response = {"success": False, "message": "user not logged in"}

        return response

    def check_seller_login_status(self, request_json, customer_db_stub, product_db_stub):
        user = ParseDict(request_json, seller_pb2.SellerUser())
        response = customer_db_stub.check_seller_login_status(user)
        response = MessageToDict(response, including_default_value_fields=True)
        return response


class SellerRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        server=SellerServer()
        
        customer_db_channel = grpc.insecure_channel(CUSTOMER_DB_HOST + ':' + CUSTOMER_DB_PORT)
        customer_db_stub = seller_pb2_grpc.SellerStub(customer_db_channel)

        product_db_channel = grpc.insecure_channel(PRODUCT_DB_HOST + ':' + PRODUCT_DB_PORT)
        product_db_stub = seller_pb2_grpc.SellerStub(product_db_channel)
        
        content_length = int(self.headers['Content-Length'])
        request_str = self.rfile.read(content_length).decode('utf-8')
        
        request = json.loads(request_str)
        action = request.get("action")
        request.pop("action")


        if action == "create_seller":
            response = server.create_seller(request, customer_db_stub, product_db_stub)
        elif action == "login_seller":
            response = server.login_seller(request, customer_db_stub, product_db_stub)
        elif action == "logout_seller":
            response = server.logout_seller(request, customer_db_stub, product_db_stub)
        elif action == "get_seller_rating":
            response = server.get_seller_rating(request, customer_db_stub, product_db_stub)
        elif action == "add_item":
            response = server.add_item(request, customer_db_stub, product_db_stub)
        elif action == "remove_item":
            response = server.remove_item(request, customer_db_stub, product_db_stub)
        elif action == "change_price":
            response = server.change_price(request, customer_db_stub, product_db_stub)
        elif action == "all_items_by_seller":
            response = server.all_items_by_seller(request, customer_db_stub, product_db_stub)
        else:
            response = {"success": False, "message": "Invalid action"}

        
        self.send_json_response(response)

    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())





def start_server():
    
    server = SellerServer()
    httpd = HTTPServer((SELLER_SERVER_HOST, SELLER_SERVER_PORT), SellerRequestHandler)
    print("=============================")
    print("Server running")
    print("=============================")

    httpd.serve_forever()
    
    print("=============================")
    print("Server shutdown")
    print("=============================")



    # server = SellerServer()
    # customer_db_channel = grpc.insecure_channel(CUSTOMER_DB_HOST + ':' + CUSTOMER_DB_PORT)
    # customer_db_stub = seller_pb2_grpc.SellerStub(customer_db_channel)
    # product_db_channel = grpc.insecure_channel(PRODUCT_DB_HOST + ':' + PRODUCT_DB_PORT)
    # product_db_stub = seller_pb2_grpc.SellerStub(product_db_channel)

    # ## Add DUMMY DATA and print FOR TESTING ONLY

    # add_dummy_data(server, customer_db_stub, product_db_stub)

    # test_db(server, customer_db_stub, product_db_stub)







##########################################################################
# Testing functions
##########################################################################


##########################################################################


# def add_dummy_data(server, customer_db_stub, product_db_stub):

#     print("=============================")

#     request = {"action": "create_seller", 
#                "username": "usr1",
#                "password": "pw1",
#                "name" : "name1",
#                }

#     # emulate conversion on network
#     request = json.loads(json.dumps(request).encode())
    
#     action = request.get("action")
#     print(action)
#     response = handle_request(server, request, customer_db_stub, product_db_stub)
#     print(type(response))
#     print(response)

#     print("=============================")

#     request = {"action": "create_seller", 
#                "username": "usr2",
#                "password": "pw2",
#                "name" : "name2",
#                }

#     # emulate conversion on network
#     request = json.loads(json.dumps(request).encode())
    
#     action = request.get("action")
#     print(action)
#     response = handle_request(server, request, customer_db_stub, product_db_stub)
#     print(type(response))
#     print(response)

#     print("=============================")

#     request = {"action": "create_seller", 
#                "username": "usr2",
#                "password": "pw2",
#                "name" : "name2",
#                }

#     # emulate conversion on network
#     request = json.loads(json.dumps(request).encode())
    
#     action = request.get("action")
#     print(action)
#     response = handle_request(server, request, customer_db_stub, product_db_stub)
#     print(type(response))
#     print(response)



#     print("=============================")

#     request = {"action": "login_seller", 
#                "username": "usr1",
#                "password": "pw1",
#                "name" : "name2",
#                }

#     # emulate conversion on network
#     request = json.loads(json.dumps(request).encode())
    
#     action = request.get("action")
#     print(action)
#     response = handle_request(server, request, customer_db_stub, product_db_stub)
#     print(type(response))
#     print(response)



#     print("=============================")

#     request = {"action": "login_seller", 
#                "username": "usr2",
#                "password": "pw2",
#                "name" : "name2",
#                }

#     # emulate conversion on network
#     request = json.loads(json.dumps(request).encode())
    
#     action = request.get("action")
#     print(action)
#     response = handle_request(server, request, customer_db_stub, product_db_stub)
#     print(type(response))
#     print(response)






#     print("=============================")
#     item = {"name": "item1", 
#             "category" : 0, 
#             "condition" : "new", 
#             "keywords" : ("k1", "k2", "k3"), 
#             "price" : 100
#             }

#     request = {"action": "add_item", 
#                "username": "usr1",
#                "item" : item,
#                "quantity" : 2
#                }

#     # emulate conversion on network
#     request = json.loads(json.dumps(request).encode())
    
#     action = request.get("action")
#     print(action)
#     response = handle_request(server, request, customer_db_stub, product_db_stub)
#     print(response)



#     print("=============================")
#     item = {"name": "item2", 
#             "category" : 0, 
#             "condition" : "new", 
#             "keywords" : ("k3", "k4", "k5"), 
#             "price" : 100
#             }

#     request = {"action": "add_item", 
#                "username": "usr2",
#                "item" : item,
#                "quantity" : 2
#                }


#     # emulate conversion on network
#     request = json.loads(json.dumps(request).encode())
    
#     action = request.get("action")
#     print(action)
#     response = handle_request(server, request, customer_db_stub, product_db_stub)
#     print(response)



# ##########################################################################

# def test_db(server, customer_db_stub, product_db_stub):

#     print("=============================")

#     request = {"action": "remove_item", 
#                "prod_id": 0,
#                "quantity" : 2, 
#                "username": "usr2",
#                }
    
#     # emulate conversion on network
#     request = json.loads(json.dumps(request).encode())
    
#     action = request.get("action")
#     print(action)
#     response = handle_request(server, request, customer_db_stub, product_db_stub)
#     print(response)



#     print("=============================")

#     request = {"action": "remove_item", 
#                "prod_id": 1,
#                "quantity" : 1, 
#                "username": "usr2",
#                }
    
#     # emulate conversion on network
#     request = json.loads(json.dumps(request).encode())
    
#     action = request.get("action")
#     print(action)
#     response = handle_request(server, request, customer_db_stub, product_db_stub)
#     print(response)




#     print("=============================")

#     request = {"action": "change_price", 
#                "prod_id": 2,
#                "new_price" : 50, 
#                "username": "usr2",
#                }
    
#     # emulate conversion on network
#     request = json.loads(json.dumps(request).encode())
    
#     action = request.get("action")
#     print(action)
#     response = handle_request(server, request, customer_db_stub, product_db_stub)
#     print(response)


## for TESTING ONLY
# def handle_request(server, request, customer_db_stub, product_db_stub):
#         action = request.get("action")
#         request.pop("action")

#         if action == "create_seller":
#             response = server.create_seller(request, customer_db_stub, product_db_stub)
#         elif action == "login_seller":
#             response = server.login_seller(request, customer_db_stub, product_db_stub)
#         elif action == "logout_seller":
#             response = server.logout_seller(request, customer_db_stub, product_db_stub)
#         elif action == "get_seller_rating":
#             response = server.get_seller_rating(request, customer_db_stub, product_db_stub)
#         elif action == "add_item":
#             response = server.add_item(request, customer_db_stub, product_db_stub)
#         elif action == "remove_item":
#             response = server.remove_item(request, customer_db_stub, product_db_stub)
#         elif action == "change_price":
#             response = server.change_price(request, customer_db_stub, product_db_stub)
#         elif action == "all_items_by_seller":
#             response = server.all_items_by_seller(request, customer_db_stub, product_db_stub)
#         else:
#             response = {"success": False, "message": "Invalid action"}
        
#         return response







##########################################################################

if __name__ == '__main__':
    start_server()







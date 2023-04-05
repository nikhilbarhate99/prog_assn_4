import argparse
import sys
import json
import grpc
from concurrent import futures 
import time
import socket
import pickle

from grpc_files import seller_pb2
from grpc_files import seller_pb2_grpc
from grpc_files import buyer_pb2
from grpc_files import buyer_pb2_grpc

from google.protobuf.json_format import Parse, ParseDict, MessageToDict, MessageToJson

from global_variables import *


sys.path.append('./grpc_files')


class DBServer:

    def __init__(self):
        self.seller_id_count = 0
        self.seller_data  = dict()

        self.buyer_id_count = 0
        self.buyer_data = dict()

        self.cart_data = dict()

        self.logged_sellers = dict()
        self.logged_buyers = dict()

        self.purchase_history = dict()
        self.order_id = 0

    def create_seller(self, usr_name, password, name):

        if usr_name in self.seller_data:
            return {"success": False, "message": "username not available"}
        
        self.seller_data.update({usr_name : 
                                 {"password" : password, 
                                  "id" :  self.seller_id_count, 
                                  "name" : name,
                                  "feedback_pos" : 0,
                                  "feedback_neg" : 0,
                                  "num_items_sold" : 0
                                  }})
        self.seller_id_count += 1
        return {"success": True, "message": "Account created successfully"}
    
    
    def login_seller(self, usr_name, password):
        if usr_name in self.seller_data and self.seller_data.get(usr_name).get("password") == password:
            self.logged_sellers[usr_name] = time.time()
            return {"success": True, "message": "credentials verified"}
        
        return {"success": False, "message": "wrong username or password"}
    
    def logout_seller(self, usr_name):
        if usr_name in self.logged_sellers:
            self.logged_sellers.pop(usr_name)
        
        return {"success": True, "message": "user logged out"}
            

    def get_seller_rating(self, usr_name):
        if usr_name in self.seller_data:
            return {"success": True, 
                    "rating_pos" : self.seller_data.get("feedback_pos"), 
                    "rating_neg" : self.seller_data.get("feedback_neg")}
        
        return {"success": False, "rating_pos": -1, "rating_neg": -1}

    def create_buyer(self, usr_name, password, name):
        if usr_name in self.buyer_data:
            return {"success": False, "message": "username not available"}
        
        self.buyer_data.update({usr_name : 
                                 {"password" : password, 
                                  "id" :  self.buyer_id_count, 
                                  "name" : name,
                                  "num_items_purchased" : 0
                                  }})
        self.buyer_id_count += 1
        return {"success": True, "message": "Account created successfully"}
    
    
    def login_buyer(self, usr_name, password):
        if usr_name in self.buyer_data and self.buyer_data.get(usr_name).get("password") == password:
            self.logged_buyers[usr_name] = time.time()
            return {"success": True, "message": "credentials verified"}
        
        return {"success": False, "message": "wrong username or password"}

    def logout_buyer(self, usr_name):
        if usr_name in self.logged_buyers:
            self.logged_buyers.pop(usr_name)
        
        return {"success": True, "message": "user logged out"}

    def add_cart(self, usr_name, prod_id, quantity):
        prod_id = int(prod_id)
        quantity = int(quantity)
        if usr_name in self.cart_data:
            self.cart_data[usr_name].update({prod_id : quantity})
        else:
            self.cart_data[usr_name] = dict({prod_id : quantity})

        return {"success": True, "message": "item added to cart"}
    
    def remove_cart(self, usr_name, prod_id, quantity):
        prod_id = int(prod_id)
        quantity = int(quantity)
        if usr_name in self.cart_data and prod_id in self.cart_data.get(usr_name):
            new_quantity = self.cart_data.get(usr_name).get(prod_id) - quantity

            if new_quantity > 0:
                self.cart_data[usr_name].update({prod_id : new_quantity})
            else:
                self.cart_data[usr_name].pop(prod_id)
                if len(self.cart_data[usr_name]) == 0:
                    self.clear_cart(usr_name)

            return {"success": True, "message": "item removed from cart"}
        
        return {"success": False, "message": "invalid product id / username"}

    def clear_cart(self, usr_name):
        if usr_name in self.cart_data:
            self.cart_data.pop(usr_name)
        return {"success": True, "message": "cart cleared"}

    def display_cart(self, usr_name):
        if usr_name in self.cart_data:
            return {"success": True, "cart": self.cart_data.get(usr_name)}
        return {"success": False, "cart": None}
    

    def add_purchase(self, usr_name, prod_id, quantity):
        prod_id = int(prod_id)
        quantity = int(quantity)
        if usr_name not in self.purchase_history:
            self.purchase_history[usr_name] = []

        order = dict({'prod_id' : prod_id, 'quantity': quantity})
        self.purchase_history[usr_name].append(order)

        return {"success": True, "message": "purchase added"}

    def get_purchase_history(self, usr_name):
        result = []
        if usr_name in self.purchase_history:
            result = self.purchase_history[usr_name]
        return {"success": True, "purchase_history": result}
    

    def check_seller_login_status(self, usr_name):
        if usr_name in self.logged_sellers:
            return {"success": True, "message": "login session active"}
        return {"success": False, "message": "user not logged in"}
    
    def check_buyer_login_status(self, usr_name):
        if usr_name in self.logged_buyers:
            return {"success": True, "message": "login session active"}
        return {"success": False, "message": "user not logged in"}



class RequestMessage:
    def __init__(self, msg_id, data, meta_data):
        self.msg_id = msg_id
        self.data = data
        self.meta_data = meta_data

class SequenceMessage:
    def __init__(self, server_id, msg_id, global_seq_num, meta_data):
        self.server_id = server_id
        self.msg_id = msg_id
        self.global_seq_num = global_seq_num
        self.meta_data = meta_data

class AtomicBroadcaster:
    def __init__(self, id, node_list):

        self.server_id = id
        self.local_seq_num = -1

        self.node_list = node_list
        self.num_nodes = len(node_list)
        
        self.request_msg_buffer = dict()
        self.sequence_msg_buffer = dict()

        host, port = node_list[id]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, int(port)))
        self.sock.settimeout(UDP_SOCKET_TIMEOUT)


    def send_request_message(self, req_data, meta_data):
        msg_id = (self.server_id, self.local_seq_num)
        req_msg = RequestMessage(msg_id, req_data, meta_data)
        self.request_msg_buffer[msg_id] = req_msg
        for (host, port) in self.node_list:
            self.sock.sendto(pickle.dumps(req_msg), (host, int(port)))

    def recv_request_message(self):
        req_msg, addr = self.sock.recvfrom(UDP_PACKET_SIZE)
        req_msg = pickle.loads(req_msg)
        return req_msg, addr


    def send_sequence_message(self, msg_id, global_seq_num, meta_data):
        
        seq_msg = SequenceMessage(self.server_id, msg_id, global_seq_num, meta_data)
        self.sequence_msg_buffer[msg_id] = global_seq_num


        pass

    def consensus(self, request):

        self.send_request_message(request, "meta_data")

        return 0

    
    def apply_requests(self, request_list, db):
        for req in request_list:
            if req.meta_data == 'create_seller':
                request = req.data
                response_dict = self.db.create_seller(request.username, request.password, request.name)
        
        # return last response
        return response_dict









class SellerServicer(seller_pb2_grpc.SellerServicer):
    def __init__(self, db, atomic_broadcaster):
        self.db = db
        self.atomic_broadcaster = atomic_broadcaster
    
    def create_seller(self, request, context):

        ## communicate and figure out all the sequences 
        ## apply them
        ## apply this request

        request_list = self.atomic_broadcaster.consensus(request)

        # response_dict = self.atomic_broadcaster.apply_all_req(request_list, self.db)





        response_dict = self.db.create_seller(request.username, request.password, request.name)
        response = ParseDict(response_dict, seller_pb2.SellerResponse())
        return response

    def login_seller(self, request, context):
        response_dict = self.db.login_seller(request.username, request.password)
        response = ParseDict(response_dict, seller_pb2.SellerResponse())
        return response
    
    def logout_seller(self, request, context):
        response_dict = self.db.logout_seller(request.username)
        response = ParseDict(response_dict, seller_pb2.SellerResponse())
        return response
    
    def get_seller_rating(self, request, context):
        response_dict = self.db.get_seller_rating(request.username)
        response = ParseDict(response_dict, seller_pb2.SellerRating())
        return response

    def check_seller_login_status(self, request, context):
        response_dict = self.db.check_seller_login_status(request.username)
        response = ParseDict(response_dict, seller_pb2.SellerResponse())
        return response


class BuyerServicer(buyer_pb2_grpc.BuyerServicer):
    def __init__(self, db, atomic_broadcaster):
        self.db = db
        self.atomic_broadcaster = atomic_broadcaster
    
    def create_buyer(self, request, context):
        response_json = self.db.create_buyer(request.username, request.password, request.name)
        response = ParseDict(response_json, buyer_pb2.BuyerResponse())
        return response
    
    def login_buyer(self, request, context):
        response_json = self.db.login_buyer(request.username, request.password)
        response = ParseDict(response_json, buyer_pb2.BuyerResponse())
        return response
    
    def logout_buyer(self, request, context):
        response_json = self.db.logout_buyer(request.username)
        response = ParseDict(response_json, buyer_pb2.BuyerResponse())
        return response

    def add_cart(self, request, context):
        response_json = self.db.add_cart(request.username, request.prod_id, request.quantity)
        response = ParseDict(response_json, buyer_pb2.BuyerResponse())
        return response
    
    def remove_cart(self, request, context):
        response_json = self.db.remove_cart(request.username, request.prod_id, request.quantity)
        response = ParseDict(response_json, buyer_pb2.BuyerResponse())
        return response

    def clear_cart(self, request, context):
        response_json = self.db.clear_cart(request.username)
        response = ParseDict(response_json, buyer_pb2.BuyerResponse())
        return response
    
    def display_cart(self, request, context):
        response_json = self.db.display_cart(request.username)
        response = ParseDict(response_json, buyer_pb2.CartResponse())
        return response
    
    def add_purchase(self, request, context):
        response_json = self.db.add_purchase(request.username, request.prod_id, request.quantity)
        response = ParseDict(response_json, buyer_pb2.BuyerResponse())
        return response
    
    def get_purchase_history(self, request, context):
        response_json = self.db.get_purchase_history(request.username)
        response = ParseDict(response_json, buyer_pb2.BuyerHistory())
        return response

    def get_seller_rating(self, request, context):
        response_dict = self.db.get_seller_rating(request.username)
        response = ParseDict(response_dict, buyer_pb2.BuyerSellerRating())
        return response
    
    def check_buyer_login_status(self, request, context):
        response_json = self.db.check_buyer_login_status(request.username)
        response = ParseDict(response_json, buyer_pb2.BuyerResponse())
        return response
    


def start_server(args):

    node_id = args.node_id
    host, port = CUSTOMER_DB_LIST[node_id]

    print("=============================")
    print("Server running")
    print("Server type: CUSTOMER DB")
    print("node id:", node_id)
    print(host, port)
    print("=============================")

    

    # initialize db and server
    db = DBServer()
    atomic_broadcaster = AtomicBroadcaster(node_id, CUSTOMER_DB_LIST)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))

    # add services to server
    seller_pb2_grpc.add_SellerServicer_to_server(SellerServicer(db, atomic_broadcaster), server)
    buyer_pb2_grpc.add_BuyerServicer_to_server(BuyerServicer(db, atomic_broadcaster), server)

    # add port and start server
    server.add_insecure_port(host + ':' + port)
    server.start()
    
    while True:
        try:
            req_msg, addr = atomic_broadcaster.recv_request_message()

            print('>' * 30)
            print("recv msg from: ", addr)
            print(req_msg.msg_id)
            print(req_msg.data)
            print(req_msg.meta_data)
            print('>' * 30)

        except:
            continue

        pass


    server.wait_for_termination()


    print("=============================")
    print("Server shutdown")
    print("=============================")










##########################################################################
# Testing functions
##########################################################################

def print_db_state(db):
    print("=============================")
    print(db.seller_id_count)
    print("=============================")
    for k, v in db.seller_data.items():
        print(k, v)

    print("=============================")
    print(db.buyer_id_count)

    print("=============================")
    for k, v in db.buyer_data.items():
        print(k, v)

    print("=============================")
    for k, v in db.cart_data.items():
        print(k, v)



##########################################################################


def add_dummy_data(db):

    print("=============================")

    request = {"action": "create_seller", 
               "username": "usr1",
               "password": "pw1",
               "name" : "name1",
               }

    # emulate conversion on network
    request = json.loads(json.dumps(request).encode())
    
    action = request.get("action")
    print(action)
    response = db.create_seller(request.get("username"), request.get("password"), request.get("name"))
    print(response)

    print("=============================")

    request = {"action": "create_seller", 
               "username": "usr2",
               "password": "pw2",
               "name" : "name2",
               }

    # emulate conversion on network
    request = json.loads(json.dumps(request).encode())
    
    action = request.get("action")
    print(action)
    response = db.create_seller(request.get("username"), request.get("password"), request.get("name"))
    print(response)

    print("=============================")

    request = {"action": "create_seller", 
               "username": "usr2",
               "password": "pw2",
               "name" : "name2",
               }

    # emulate conversion on network
    request = json.loads(json.dumps(request).encode())
    
    action = request.get("action")
    print(action)
    response = db.create_seller(request.get("username"), request.get("password"), request.get("name"))
    print(response)




    print("=============================")

    request = {"action": "create_buyer", 
               "username": "usr4",
               "password": "pw4",
               "name" : "name4",
               }

    # emulate conversion on network
    request = json.loads(json.dumps(request).encode())
    
    action = request.get("action")
    print(action)
    response = db.create_buyer(request.get("username"), request.get("password"), request.get("name"))
    print(response)


    print("=============================")

    request = {"action": "create_buyer", 
               "username": "usr5",
               "password": "pw5",
               "name" : "name5",
               }

    # emulate conversion on network
    request = json.loads(json.dumps(request).encode())
    
    action = request.get("action")
    print(action)
    response = db.create_buyer(request.get("username"), request.get("password"), request.get("name"))
    print(response)


    print("=============================")

    request = {"action": "create_buyer", 
               "username": "usr5",
               "password": "pw5",
               "name" : "name5",
               }

    # emulate conversion on network
    request = json.loads(json.dumps(request).encode())
    
    action = request.get("action")
    print(action)
    response = db.create_buyer(request.get("username"), request.get("password"), request.get("name"))
    print(response)


##########################################################################


def test_db(db):
    

    print("=============================")

    request = {"action": "add_cart", 
               "username": "usr5",
               "prod_id": 1,
               "quantity" : 3,
               }

    # emulate conversion on network
    request = json.loads(json.dumps(request).encode())
    
    action = request.get("action")
    print(action)
    response = db.add_cart(request.get("username"), request.get("prod_id"), request.get("quantity"))
    print(response)


    print("=============================")

    request = {"action": "add_cart", 
               "username": "usr5",
               "prod_id": 2,
               "quantity" : 1,
               }

    # emulate conversion on network
    request = json.loads(json.dumps(request).encode())
    
    action = request.get("action")
    print(action)
    response = db.add_cart(request.get("username"), request.get("prod_id"), request.get("quantity"))
    print(response)


    print("=============================")

    request = {"action": "add_cart", 
               "username": "usr5",
               "prod_id": 3,
               "quantity" : 1,
               }

    # emulate conversion on network
    request = json.loads(json.dumps(request).encode())
    
    action = request.get("action")
    print(action)
    response = db.add_cart(request.get("username"), request.get("prod_id"), request.get("quantity"))
    print(response)


    print("=============================")

    request = {"action": "remove_cart", 
               "username": "usr5",
               "prod_id": 3,
               "quantity" : 1,
               }

    # emulate conversion on network
    request = json.loads(json.dumps(request).encode())
    
    action = request.get("action")
    print(action)
    response = db.remove_cart(request.get("username"), request.get("prod_id"), request.get("quantity"))
    print(response)



    print("=============================")

    request = {"action": "remove_cart", 
               "username": "usr5",
               "prod_id": 1,
               "quantity" : 1,
               }

    # emulate conversion on network
    request = json.loads(json.dumps(request).encode())
    
    action = request.get("action")
    print(action)
    response = db.remove_cart(request.get("username"), request.get("prod_id"), request.get("quantity"))
    print(response)




    print("=============================")

    request = {"action": "display_cart", 
               "username": "usr5",
               "prod_id": 1,
               "quantity" : 1,
               }

    # emulate conversion on network
    request = json.loads(json.dumps(request).encode())
    
    action = request.get("action")
    print(action)
    response = db.display_cart(request.get("username"))
    print(response)




    print("=============================")

    request = {"action": "clear_cart", 
               "username": "usr5",
               "prod_id": 1,
               "quantity" : 1,
               }

    # emulate conversion on network
    request = json.loads(json.dumps(request).encode())
    
    action = request.get("action")
    print(action)
    response = db.clear_cart(request.get("username"))
    print(response)



    print("=============================")

    request = {"action": "display_cart", 
               "username": "usr5",
               "prod_id": 1,
               "quantity" : 1,
               }

    # emulate conversion on network
    request = json.loads(json.dumps(request).encode())
    
    action = request.get("action")
    print(action)
    response = db.display_cart(request.get("username"))
    print(response)








##########################################################################

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--node_id', type=int, default=0)
    args = parser.parse_args()

    start_server(args)







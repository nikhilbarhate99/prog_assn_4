import argparse
import sys
import json
import grpc
from concurrent import futures 
import time
import socket
import pickle

import threading
import random

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


class MetaData:
    def __init__(self, max_global_seq_num=None, local_seq_num=None, seq_num_iter=None, node_wise_msgs=[]):
        self.max_global_seq_num = max_global_seq_num
        self.local_seq_num = local_seq_num
        self.seq_num_iter = seq_num_iter
        self.node_wise_msgs = node_wise_msgs
        
class RequestMessage:
    def __init__(self, sender_id, msg_id, data, func_name, meta_data=None):
        self.sender_id = sender_id
        self.msg_id = msg_id
        self.func_name = func_name
        self.data = data
        self.meta_data = meta_data

class SequenceMessage:
    def __init__(self, sender_id, msg_id, global_seq_num, meta_data=None):
        self.sender_id = sender_id
        self.msg_id = msg_id
        self.global_seq_num = global_seq_num
        self.meta_data = meta_data

class RetransmissionMessage:
    def __init__(self, sender_id, ret_msg_id, ret_msg_seq_num, ret_msg_type, meta_data=None):
        self.sender_id = sender_id
        self.ret_msg_id = ret_msg_id
        self.ret_msg_seq_num = ret_msg_seq_num
        self.ret_msg_type = ret_msg_type # 'request_msg' or 'sequence_msg' or 'sequence_msg_via_num'
        assert ret_msg_type in {'request_msg', 'sequence_msg', 'sequence_msg_via_num'}, 'unknown ret_msg_type in Retransmission msg'
        self.meta_data = meta_data

class AtomicBroadcaster:
    def __init__(self, id, node_list):

        self.server_id = id
        self.node_list = node_list
        self.num_nodes = len(self.node_list)
        
        self.prev_server_id = self.server_id - 1 if self.server_id > 0 else self.num_nodes - 1
        self.next_server_id = self.server_id + 1 if self.server_id < self.num_nodes - 1 else 0

        # last global seq num that is delivered on this node
        self.local_seq_num = -1

        # the max global seq num node have seen
        self.max_global_seq_num = -1

        # goes from local_seq_num to max_global_seq_num
        # tracks seq_num for which we have both req msg and seq msg wiht s <= seq_num
        self.seq_num_iter = -1 


        # maps node -> local_seq_num -> req_msg 
        self.request_msg_buffer = dict()

        # maps node -> local_seq_num -> seq_msg
        self.sequence_msg_buffer = dict()

        # maps global_seq -> msg_id (node_id, local_seq_num)
        self.global_seq_buffer = dict()

        # stores current msg ids that have not been deilvered 
        self.curr_req_msg = set()
        self.curr_seq_msg = set()

        # maintain a list of all delivered requests
        self.list_of_delivered_requests = []

        host, port = node_list[id]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, int(port)))
        self.sock.settimeout(UDP_SOCKET_TIMEOUT)

        # condition variable for mutual exclusion
        self.lock = threading.Lock()

    def add_meta_data_to_msg(self, msg):
        # set meta data 
        meta_data = MetaData(max_global_seq_num=self.max_global_seq_num, 
                             local_seq_num=self.local_seq_num,
                             seq_num_iter=self.seq_num_iter)
        msg.meta_data = meta_data
        return msg

    def send_message(self, msg, node_id):
        # set meta data
        msg = self.add_meta_data_to_msg(msg)

        host, port = self.node_list[node_id]
        self.sock.sendto(pickle.dumps(msg), (host, int(port)))

    def recv_message(self):
        msg, addr = self.sock.recvfrom(UDP_PACKET_SIZE)


        ### simulate packet loss ###
        loss_ratio = 0.2
        if random.random() < loss_ratio:
            print("+!" * 30)
            print("DISCARDING PACKET")
            print("+!" * 30)
            raise TimeoutError


        msg = pickle.loads(msg)
        # get node id from address
        node_id = self.node_list.index((addr[0], str(addr[1])))
        return msg, node_id
    

    def broadcast_message(self, msg):
        # set meta data
        msg = self.add_meta_data_to_msg(msg)

        for (host, port) in self.node_list:
            self.sock.sendto(pickle.dumps(msg), (host, int(port)))


    def broadcast_request_message(self, msg_id, req_data, func_name):
        
        req_msg = RequestMessage(self.server_id, msg_id, req_data, func_name)

        # add to request msg buffer
        node, local_seq_num = req_msg.msg_id
        if node not in self.request_msg_buffer:
            self.request_msg_buffer[node] = dict()
        if local_seq_num not in self.request_msg_buffer[node]:
            self.request_msg_buffer[node][local_seq_num] = req_msg
            # add to list of current unapplied msgs
            self.curr_req_msg.add(req_msg.msg_id)

        self.broadcast_message(req_msg)


    def broadcast_sequence_message(self, msg_id, global_seq_num):
        seq_msg = SequenceMessage(self.server_id, msg_id, global_seq_num)
        
        # add to sequence msg buffer
        node, local_seq_num = msg_id
        if node not in self.sequence_msg_buffer:
                self.sequence_msg_buffer[node] = dict()
        if local_seq_num not in self.sequence_msg_buffer[node]:
            self.sequence_msg_buffer[node][local_seq_num] = seq_msg
            # also add to global_seq_buffer
            self.global_seq_buffer[seq_msg.global_seq_num] = seq_msg.msg_id
            # add to list of current unapplied msgs
            self.curr_seq_msg.add(seq_msg.msg_id)
            self.max_global_seq_num = max(self.max_global_seq_num, seq_msg.global_seq_num)

        self.broadcast_message(seq_msg)
    

    def send_retransmission_msg(self, recv_node_id, msg_id, ret_msg_seq_num, ret_msg_type):
        retransmit_msg = RetransmissionMessage(self.server_id, 
                                               msg_id,
                                               ret_msg_seq_num,
                                               ret_msg_type)
        self.send_message(retransmit_msg, recv_node_id)


    def broadcast_retransmission_msg(self, msg_id, ret_msg_seq_num, ret_msg_type):
        retransmit_msg = RetransmissionMessage(self.server_id, 
                                               msg_id,
                                               ret_msg_seq_num,
                                               ret_msg_type)
        self.broadcast_message(retransmit_msg)


    def get_seq_num_assigner_id(self, id):
        return id % self.num_nodes


    def propose_new_req(self, request, func_name):
        msg_id = (self.server_id, self.local_seq_num)
        self.broadcast_request_message(msg_id, request, func_name)
        return msg_id


    def process_message(self, msg, node_id):
        
        if type(msg) == RequestMessage:
            # add to request msg buffer
            node, local_seq_num = msg.msg_id
            if node not in self.request_msg_buffer:
                self.request_msg_buffer[node] = dict()
            if local_seq_num not in self.request_msg_buffer[node]:
                self.request_msg_buffer[node][local_seq_num] = msg

                # add to list of current unapplied msgs
                self.curr_req_msg.add(msg.msg_id)

            print('>' * 30)
            print(type(msg))
            print("recv msg from: ", node_id)
            print("msg_id: ", msg.msg_id)
            print("func_name: ", msg.func_name)
            print("max_global_seq_num: ", msg.meta_data.max_global_seq_num)
            print("data: ", msg.data)
            print('>' * 30)

        elif type(msg) == SequenceMessage:
            # add to sequence msg buffer
            node, local_seq_num = msg.msg_id
            if node not in self.sequence_msg_buffer:
                self.sequence_msg_buffer[node] = dict()
            if local_seq_num not in self.sequence_msg_buffer[node]:
                self.sequence_msg_buffer[node][local_seq_num] = msg

                # also add to global_seq_buffer
                self.global_seq_buffer[msg.global_seq_num] = msg.msg_id

                # add to list of current unapplied msgs
                self.curr_seq_msg.add(msg.msg_id)


            print('>' * 30)
            print(type(msg))
            print("recv msg from: ", node_id)
            print("msg_id: ", msg.msg_id)
            print("max_global_seq_num: ", msg.meta_data.max_global_seq_num)
            print("global_seq_num: ", msg.global_seq_num)
            print('>' * 30)

        elif type(msg) == RetransmissionMessage:
            
            if msg.ret_msg_type == 'request_msg':
                # get msg from buffer
                node, local_seq_num = msg.ret_msg_id
                if node in self.request_msg_buffer and local_seq_num in self.request_msg_buffer[node]:
                    ret_msg = self.request_msg_buffer[node][local_seq_num]
                    # send the msg to sender
                    self.send_message(ret_msg, msg.sender_id)

            elif msg.ret_msg_type == 'sequence_msg':
                # get msg from buffer
                node, local_seq_num = msg.ret_msg_id
                if node in self.sequence_msg_buffer and local_seq_num in self.sequence_msg_buffer[node]:
                    ret_msg = self.sequence_msg_buffer[node][local_seq_num]
                    # send the msg to sender
                    self.send_message(ret_msg, msg.sender_id)

            elif msg.ret_msg_type == 'sequence_msg_via_num':
                
                s = msg.ret_msg_seq_num
                assert s in self.global_seq_buffer, 'sequence_msg_via_num, s has to be assigned before call'

                node, local_seq_num = self.global_seq_buffer[s]
                ret_msg = self.sequence_msg_buffer[node][local_seq_num]
                # send the msg to sender
                self.send_message(ret_msg, msg.sender_id)


                # send all msgs with s from begin_s to end_s

            else:
                NotImplementedError
            
            print('>' * 30)
            print(type(msg))
            print("recv msg from: ", node_id)
            print("ret_msg_id: ", msg.ret_msg_id)
            print("ret_msg_type: ", msg.ret_msg_type)
            print("sender_id: ", msg.sender_id)
            print('>' * 30)

        else:
            raise NotImplementedError

        # update max global seq based on meta data
        if msg.meta_data.max_global_seq_num > self.max_global_seq_num:
            self.max_global_seq_num = msg.meta_data.max_global_seq_num


    def consensus(self):

        consensus_reached = False
        
        while not consensus_reached:

            req_msg_w_no_seq = self.curr_req_msg.difference(self.curr_seq_msg)

            print("@" * 30)

            print("request_msg_buffer ", self.request_msg_buffer)
            print('-' * 10)
            print("sequence_msg_buffer ", self.sequence_msg_buffer)
            print('-' * 10)
            print("global_seq_buffer ", self.global_seq_buffer)
            print('-' * 10)
            print("curr_req_msg ", self.curr_req_msg)
            print('-' * 10)
            print("curr_seq_msg ", self.curr_seq_msg)
            print('-' * 10)
            print("req_msg_w_no_seq ", req_msg_w_no_seq)

            print("local_seq_num ", self.local_seq_num)
            print("seq_num_iter ", self.seq_num_iter)
            print("max_global_seq_num ", self.max_global_seq_num)
            
            print("@" * 30)

            ###### check consensus conditions ######

            if self.seq_num_iter == self.max_global_seq_num and self.curr_req_msg == self.curr_seq_msg:
                
                print("consensus reached ", self.server_id)
                
                print("@" * 30)

                consensus_reached = True
                
                break


            ###### send msgs ######

            assert self.seq_num_iter < self.max_global_seq_num or len(self.curr_req_msg) > 0, 'seq_msg_iter >= max_global_seq_num'

            next_seq_num_iter =  self.seq_num_iter + 1
            next_node_id = self.get_seq_num_assigner_id(next_seq_num_iter)
            req_msg_w_no_seq = self.curr_req_msg.difference(self.curr_seq_msg)
            
            if self.seq_num_iter < self.max_global_seq_num:

                # next node is this server and we still have req msg with no seq msg then assign it
                if next_node_id == self.server_id and len(req_msg_w_no_seq) > 0:
                    global_seq_num = next_seq_num_iter
                    # choose next req_msg without global sequence
                    msg_id = next(iter(req_msg_w_no_seq))
                    self.broadcast_sequence_message(msg_id, global_seq_num)
                    
                    # this seq num has been handled, so move to next seq num
                    self.seq_num_iter = next_seq_num_iter

                    print("ASSIGNING GLOBAL SEQ NUM")
                    print(msg_id)
                    print(global_seq_num)
                
                else:
                    # ask for corresponding seq msg
                    if next_seq_num_iter not in self.global_seq_buffer:
                        self.send_retransmission_msg(next_node_id, None, next_seq_num_iter, 'sequence_msg_via_num')
                    
                    # ask for corresponding req msg
                    else:
                        next_msg_id = self.global_seq_buffer[next_seq_num_iter]
                        node, local_seq_num = next_msg_id
                        if node not in self.request_msg_buffer or local_seq_num not in self.request_msg_buffer[node]:
                            self.send_retransmission_msg(next_node_id, next_msg_id, None, 'request_msg')

                        # if both req and seq msg present in buffer, then move to next seq num
                        else:
                            self.seq_num_iter = next_seq_num_iter

            elif len(self.curr_req_msg) > 0:
                # next node is this server and we still have req msg with no seq msg then assign it
                if next_node_id == self.server_id and len(req_msg_w_no_seq) > 0:
                    global_seq_num = next_seq_num_iter
                    # choose next req_msg without global sequence
                    msg_id = next(iter(req_msg_w_no_seq))
                    self.broadcast_sequence_message(msg_id, global_seq_num)
                    
                    # this seq num has been handled, so move to next seq num
                    self.seq_num_iter = next_seq_num_iter

                    print("ASSIGNING GLOBAL SEQ NUM")
                    print(msg_id)
                    print(global_seq_num)
                
                elif len(req_msg_w_no_seq) > 0:
                    # get msg from buffer
                    next_msg_id = next(iter(req_msg_w_no_seq))
                    node, local_seq_num = next_msg_id
                    
                    # send request msg
                    if random.random() < 0.5:
                        # send the msg to sender
                        ret_msg = self.request_msg_buffer[node][local_seq_num]
                        self.broadcast_message(ret_msg)
                    
                    # ask for seq msg
                    else:
                        # send the msg to sender
                        self.broadcast_retransmission_msg(next_msg_id, None, 'sequence_msg')


            ##### too many msgs and too slow ... fix it
            
            time.sleep(RECEIVE_LOOP_DELAY) #### ++++++++++++++++++++++++++++++++++++++++++++++


            ###### receive and process msgs ######
            for _ in range(3):
                try:
                    msg, node_id = self.recv_message()
                    self.process_message(msg, node_id)

                except Exception as e:
                    print("In Consensus while loop exception occurred: ", e)
                    pass

            

        # clear current not delivered messages buffers
        self.curr_req_msg.clear()
        self.curr_seq_msg.clear()

        return

    
    def deliver_requests(self, db, rpc_return_msg_id):
        
        return_response_dict = None

        # deliver msgs in this range
        begin_seq_num = self.local_seq_num + 1
        end_seq_num = self.max_global_seq_num + 1

        for s in range(begin_seq_num, end_seq_num):
            
            # make sure the msg with global seq num 's' is in buffer
            assert s in self.global_seq_buffer, 'msg to be delivered not in buffer'

            # get request message with global seq num 's'
            msg_id = self.global_seq_buffer[s]
            node, local_seq_num = msg_id
            req_msg = self.request_msg_buffer[node][local_seq_num]            

            # extract request func_name and data (gprc protobuff object)
            func_name = req_msg.func_name
            request = req_msg.data            

            # deliver the msg
            if func_name == 'create_seller':
                response_dict = db.create_seller(request.username, request.password, request.name)

            elif func_name == 'login_seller':
                response_dict = db.login_seller(request.username, request.password)

            elif func_name == 'logout_seller':
                response_dict = db.logout_seller(request.username)

            elif func_name == 'check_seller_login_status':
                response_dict = db.check_seller_login_status(request.username)

            elif func_name == 'get_seller_rating':
                response_dict = db.get_seller_rating(request.username)
            
            elif func_name == 'create_buyer':
                response_dict = db.create_buyer(request.username, request.password, request.name)

            elif func_name == 'login_buyer':
                response_dict = db.login_buyer(request.username, request.password)

            elif func_name == 'logout_buyer':
                response_dict = db.logout_buyer(request.username)

            elif func_name == 'add_cart':
                response_dict = db.add_cart(request.username, request.prod_id, request.quantity)

            elif func_name == 'remove_cart':
                response_dict = db.remove_cart(request.username, request.prod_id, request.quantity)

            elif func_name == 'clear_cart':
                response_dict = db.clear_cart(request.username)

            elif func_name == 'display_cart':
                response_dict = db.display_cart(request.username)

            elif func_name == 'add_purchase':
                response_dict = db.add_purchase(request.username, request.prod_id, request.quantity)

            elif func_name == 'get_purchase_history':
                response_dict = db.get_purchase_history(request.username)
            
            elif func_name == 'get_seller_rating':
                response_dict = db.get_seller_rating(request.username)

            elif func_name == 'check_buyer_login_status':
                response_dict = db.check_buyer_login_status(request.username)
                
            else:
                NotImplementedError


            # update local seq number after applying corresponding request
            self.local_seq_num += 1

            self.list_of_delivered_requests.append([s, msg_id, func_name])

            # keep current response_dict to return 
            if rpc_return_msg_id is not None and rpc_return_msg_id == msg_id:
                return_response_dict = response_dict
        

        print("&" * 45)
        print("list of delivered request")

        for k in self.list_of_delivered_requests:
            print(k)
            
        print("&" * 45)

        # return curr response dict
        return return_response_dict




class SellerServicer(seller_pb2_grpc.SellerServicer):
    def __init__(self, db, atomic_broadcaster):
        self.db = db
        self.atomic_broadcaster = atomic_broadcaster
    
    def create_seller(self, request, context):

        func_name = 'create_seller'
        
        self.atomic_broadcaster.lock.acquire()

        print("+" * 60)

        # broadcast the message and start consensus protocol
        rpc_return_msg_id = self.atomic_broadcaster.propose_new_req(request, func_name)

        self.atomic_broadcaster.consensus()

        response_dict = self.atomic_broadcaster.deliver_requests(self.db, rpc_return_msg_id)

        print("+" * 60)

        self.atomic_broadcaster.lock.release()



        response = ParseDict(response_dict, seller_pb2.SellerResponse())
        return response



    def login_seller(self, request, context):

        func_name = 'login_seller'
        
        self.atomic_broadcaster.lock.acquire()

        print("+" * 60)

        # broadcast the message and start consensus protocol
        rpc_return_msg_id = self.atomic_broadcaster.propose_new_req(request, func_name)

        self.atomic_broadcaster.consensus()

        response_dict = self.atomic_broadcaster.deliver_requests(self.db, rpc_return_msg_id)

        print("+" * 60)

        self.atomic_broadcaster.lock.release()


        response = ParseDict(response_dict, seller_pb2.SellerResponse())

        return response
    
    def logout_seller(self, request, context):

        func_name = 'logout_seller'
        
        self.atomic_broadcaster.lock.acquire()

        print("+" * 60)

        # broadcast the message and start consensus protocol
        rpc_return_msg_id = self.atomic_broadcaster.propose_new_req(request, func_name)

        self.atomic_broadcaster.consensus()

        response_dict = self.atomic_broadcaster.deliver_requests(self.db, rpc_return_msg_id)

        print("+" * 60)

        self.atomic_broadcaster.lock.release()


        response = ParseDict(response_dict, seller_pb2.SellerResponse())
        return response
    

    def get_seller_rating(self, request, context):

        func_name = 'get_seller_rating'
        
        self.atomic_broadcaster.lock.acquire()

        print("+" * 60)

        # broadcast the message and start consensus protocol
        rpc_return_msg_id = self.atomic_broadcaster.propose_new_req(request, func_name)

        self.atomic_broadcaster.consensus()

        response_dict = self.atomic_broadcaster.deliver_requests(self.db, rpc_return_msg_id)

        print("+" * 60)

        self.atomic_broadcaster.lock.release()


        response = ParseDict(response_dict, seller_pb2.SellerRating())
        return response

    def check_seller_login_status(self, request, context):

        func_name = 'check_seller_login_status'

        self.atomic_broadcaster.lock.acquire()

        print("+" * 60)

        # broadcast the message and start consensus protocol
        rpc_return_msg_id = self.atomic_broadcaster.propose_new_req(request, func_name)

        self.atomic_broadcaster.consensus()

        response_dict = self.atomic_broadcaster.deliver_requests(self.db, rpc_return_msg_id)

        print("+" * 60)

        self.atomic_broadcaster.lock.release()


        response = ParseDict(response_dict, seller_pb2.SellerResponse())
        return response


class BuyerServicer(buyer_pb2_grpc.BuyerServicer):
    def __init__(self, db, atomic_broadcaster):
        self.db = db
        self.atomic_broadcaster = atomic_broadcaster
    
    def create_buyer(self, request, context):

        func_name = 'create_buyer'
        
        self.atomic_broadcaster.lock.acquire()

        print("+" * 60)

        # broadcast the message and start consensus protocol
        rpc_return_msg_id = self.atomic_broadcaster.propose_new_req(request, func_name)

        self.atomic_broadcaster.consensus()

        response_dict = self.atomic_broadcaster.deliver_requests(self.db, rpc_return_msg_id)

        print("+" * 60)

        self.atomic_broadcaster.lock.release()


        response = ParseDict(response_dict, buyer_pb2.BuyerResponse())
        return response
    
    def login_buyer(self, request, context):
        
        func_name = 'login_buyer'
        
        self.atomic_broadcaster.lock.acquire()

        print("+" * 60)

        # broadcast the message and start consensus protocol
        rpc_return_msg_id = self.atomic_broadcaster.propose_new_req(request, func_name)

        self.atomic_broadcaster.consensus()

        response_dict = self.atomic_broadcaster.deliver_requests(self.db, rpc_return_msg_id)

        print("+" * 60)

        self.atomic_broadcaster.lock.release()


        response = ParseDict(response_dict, buyer_pb2.BuyerResponse())
        return response
    
    def logout_buyer(self, request, context):

        func_name = 'logout_buyer'
        
        self.atomic_broadcaster.lock.acquire()

        print("+" * 60)

        # broadcast the message and start consensus protocol
        rpc_return_msg_id = self.atomic_broadcaster.propose_new_req(request, func_name)

        self.atomic_broadcaster.consensus()

        response_dict = self.atomic_broadcaster.deliver_requests(self.db, rpc_return_msg_id)

        print("+" * 60)

        self.atomic_broadcaster.lock.release()

        
        response = ParseDict(response_dict, buyer_pb2.BuyerResponse())
        return response

    def add_cart(self, request, context):

        func_name = 'add_cart'
        
        self.atomic_broadcaster.lock.acquire()

        print("+" * 60)

        # broadcast the message and start consensus protocol
        rpc_return_msg_id = self.atomic_broadcaster.propose_new_req(request, func_name)

        self.atomic_broadcaster.consensus()

        response_dict = self.atomic_broadcaster.deliver_requests(self.db, rpc_return_msg_id)

        print("+" * 60)

        self.atomic_broadcaster.lock.release()


        response = ParseDict(response_dict, buyer_pb2.BuyerResponse())
        return response
    
    def remove_cart(self, request, context):

        func_name = 'remove_cart'
        
        self.atomic_broadcaster.lock.acquire()

        print("+" * 60)

        # broadcast the message and start consensus protocol
        rpc_return_msg_id = self.atomic_broadcaster.propose_new_req(request, func_name)

        self.atomic_broadcaster.consensus()

        response_dict = self.atomic_broadcaster.deliver_requests(self.db, rpc_return_msg_id)

        print("+" * 60)

        self.atomic_broadcaster.lock.release()

        response = ParseDict(response_dict, buyer_pb2.BuyerResponse())
        return response

    def clear_cart(self, request, context):

        func_name = 'clear_cart'
        

        self.atomic_broadcaster.lock.acquire()

        print("+" * 60)

        # broadcast the message and start consensus protocol
        rpc_return_msg_id = self.atomic_broadcaster.propose_new_req(request, func_name)

        self.atomic_broadcaster.consensus()

        response_dict = self.atomic_broadcaster.deliver_requests(self.db, rpc_return_msg_id)

        print("+" * 60)

        self.atomic_broadcaster.lock.release()


        response = ParseDict(response_dict, buyer_pb2.BuyerResponse())
        return response
    
    def display_cart(self, request, context):

        func_name = 'display_cart'
        

        self.atomic_broadcaster.lock.acquire()

        print("+" * 60)

        # broadcast the message and start consensus protocol
        rpc_return_msg_id = self.atomic_broadcaster.propose_new_req(request, func_name)

        self.atomic_broadcaster.consensus()

        response_dict = self.atomic_broadcaster.deliver_requests(self.db, rpc_return_msg_id)

        print("+" * 60)

        self.atomic_broadcaster.lock.release()


        response = ParseDict(response_dict, buyer_pb2.CartResponse())
        return response
    
    def add_purchase(self, request, context):

        func_name = 'add_purchase'
        

        self.atomic_broadcaster.lock.acquire()

        print("+" * 60)

        # broadcast the message and start consensus protocol
        rpc_return_msg_id = self.atomic_broadcaster.propose_new_req(request, func_name)

        self.atomic_broadcaster.consensus()

        response_dict = self.atomic_broadcaster.deliver_requests(self.db, rpc_return_msg_id)

        print("+" * 60)

        self.atomic_broadcaster.lock.release()


        response = ParseDict(response_dict, buyer_pb2.BuyerResponse())
        return response
    
    def get_purchase_history(self, request, context):

        func_name = 'get_purchase_history'
        

        self.atomic_broadcaster.lock.acquire()

        print("+" * 60)

        # broadcast the message and start consensus protocol
        rpc_return_msg_id = self.atomic_broadcaster.propose_new_req(request, func_name)

        self.atomic_broadcaster.consensus()

        response_dict = self.atomic_broadcaster.deliver_requests(self.db, rpc_return_msg_id)

        print("+" * 60)

        self.atomic_broadcaster.lock.release()


        response = ParseDict(response_dict, buyer_pb2.BuyerHistory())
        return response

    def get_seller_rating(self, request, context):

        func_name = 'get_seller_rating'
        
        self.atomic_broadcaster.lock.acquire()

        print("+" * 60)

        # broadcast the message and start consensus protocol
        rpc_return_msg_id = self.atomic_broadcaster.propose_new_req(request, func_name)

        self.atomic_broadcaster.consensus()

        response_dict = self.atomic_broadcaster.deliver_requests(self.db, rpc_return_msg_id)

        print("+" * 60)

        self.atomic_broadcaster.lock.release()


        response = ParseDict(response_dict, buyer_pb2.BuyerSellerRating())
        return response
    
    def check_buyer_login_status(self, request, context):

        func_name = 'check_buyer_login_status'
        

        self.atomic_broadcaster.lock.acquire()

        print("+" * 60)

        # broadcast the message and start consensus protocol
        rpc_return_msg_id = self.atomic_broadcaster.propose_new_req(request, func_name)

        self.atomic_broadcaster.consensus()

        response_dict = self.atomic_broadcaster.deliver_requests(self.db, rpc_return_msg_id)

        print("+" * 60)

        self.atomic_broadcaster.lock.release()


        response = ParseDict(response_dict, buyer_pb2.BuyerResponse())
        return response
    


def start_server(args):

    node_id = args.node_id
    
    assert node_id < CUSTOMER_DB_N, 'max node id CUSTOMER_DB_N - 1'

    host, port = CUSTOMER_DB_LIST[node_id]

    # initialize db and server
    db = DBServer()

    atomic_broadcaster = AtomicBroadcaster(node_id, CUSTOMER_DB_PROTOCOL_LIST[:CUSTOMER_DB_N])

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=CUSTOMER_DB_MAX_WORKERS))

    # add services to server
    seller_pb2_grpc.add_SellerServicer_to_server(SellerServicer(db, atomic_broadcaster), server)
    buyer_pb2_grpc.add_BuyerServicer_to_server(BuyerServicer(db, atomic_broadcaster), server)

    # add port and start server
    server.add_insecure_port(host + ':' + port)
    server.start()

    print("=============================")
    print("Server running")
    print("Server type: CUSTOMER DB")
    print("node id:", node_id)
    print(host, port)
    print("=============================")


    while True:
        try:
            atomic_broadcaster.lock.acquire()

            print("+" * 60)

            # try to receive msg
            msg, node_id = atomic_broadcaster.recv_message()
            atomic_broadcaster.process_message(msg, node_id)
            atomic_broadcaster.consensus()
            atomic_broadcaster.deliver_requests(db, None)
            print("+" * 60)

            atomic_broadcaster.lock.release()            

        except Exception as e:
            print("In Main while loop exception occurred: ", e)
            print("+" * 60)

            atomic_broadcaster.lock.release()
            
            time.sleep(RECEIVE_LOOP_DELAY)

            continue



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







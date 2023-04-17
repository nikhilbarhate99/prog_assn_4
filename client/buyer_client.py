import urllib.request
import json
import http.client
import time
import random

from global_variables import *


class BuyerClient:

    def create_account(self, username, password, name):
        request = {"action": "create_buyer", "username": username, "password": password, "name":name}

        host, port = random.choice(BUYER_SERVER_LIST[:BUYER_SERVER_N])
        port = int(port)

        conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)
        headers = {'Content-type': 'application/json'}
        conn.request('POST', '/create_buyer', body=json.dumps(request), headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            response_body = response.read().decode()
            response_data = json.loads(response_body)
            #print(response_data["message"])
        else:
            response_data = {"success": False, "message": "No response from server"}
        conn.close()
        return response_data

    def login(self, username, password):
        request = {"action": "login_buyer", "username": username, "password": password}

        host, port = random.choice(BUYER_SERVER_LIST[:BUYER_SERVER_N])
        port = int(port)

        conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)
        headers = {'Content-type': 'application/json'}
        conn.request('POST', '/login_buyer', body=json.dumps(request), headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            response_body = response.read().decode()
            response_data = json.loads(response_body)
            #print(response_data["message"])
        else:
            response_data = {"success": False, "message": "No response from server"}
        conn.close()
        return response_data


    def display_cart(self, username):
        request = {"action": "display_cart", "username": username}

        host, port = random.choice(BUYER_SERVER_LIST[:BUYER_SERVER_N])
        port = int(port)

        conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)
        headers = {'Content-type': 'application/json'}
        conn.request('POST', '/display_cart', body=json.dumps(request), headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            response_body = response.read().decode()
            response_data = json.loads(response_body)
            #print(response_data["cart"])
        else:
            response_data = {"success": False, "message": "No response from server"}
        conn.close()
        return response_data


    def logout(self, username):
        request = {"action": "logout_buyer", "username": username}

        host, port = random.choice(BUYER_SERVER_LIST[:BUYER_SERVER_N])
        port = int(port)

        conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)
        headers = {'Content-type': 'application/json'}
        conn.request('POST', '/logout_buyer', body=json.dumps(request), headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            response_body = response.read().decode()
            response_data = json.loads(response_body)
            #print(response_data["message"])
        else:
            response_data = {"success": False, "message": "No response from server"}
        conn.close()
        return response_data

    def add_to_cart(self, username, prod_id, quantity):
        request = {"action": "add_to_cart", "username": username, "prod_id": prod_id, "quantity": quantity}

        host, port = random.choice(BUYER_SERVER_LIST[:BUYER_SERVER_N])
        port = int(port)

        conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)
        headers = {'Content-type': 'application/json'}
        conn.request('POST', '/add_to_cart', body=json.dumps(request), headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            response_body = response.read().decode()
            response_data = json.loads(response_body)
            #print(response_data["message"])
        else:
            response_data = {"success": False, "message": "No response from server"}
        conn.close()
        return response_data
          
       
    def remove_cart(self, username, prod_id, quantity):
        request = {"action": "remove_cart", "username": username, "prod_id": prod_id, "quantity": quantity}

        host, port = random.choice(BUYER_SERVER_LIST[:BUYER_SERVER_N])
        port = int(port)

        conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)
        headers = {'Content-type': 'application/json'}
        conn.request('POST', '/remove_cart', body=json.dumps(request), headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            response_body = response.read().decode()
            response_data = json.loads(response_body)
            #print(response_data["message"])
        else:
            response_data = {"success": False, "message": "No response from server"}
        conn.close()
        return response_data
        
    
    def clear_cart(self, username):
        request = {"action": "clear_cart", "username": username}

        host, port = random.choice(BUYER_SERVER_LIST[:BUYER_SERVER_N])
        port = int(port)

        conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)
        headers = {'Content-type': 'application/json'}
        conn.request('POST', '/clear_cart', body=json.dumps(request), headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            response_body = response.read().decode()
            response_data = json.loads(response_body)
            #print(response_data["message"])
        else:
            response_data = {"success": False, "message": "No response from server"}
        conn.close()
        return response_data



    def search_items(self, category, keywords,username):
        request = {"action": "search", "prod_cat": category,"keywords":keywords,"username":username}

        host, port = random.choice(BUYER_SERVER_LIST[:BUYER_SERVER_N])
        port = int(port)

        conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)
        headers = {'Content-type': 'application/json'}
        conn.request('POST', '/search', body=json.dumps(request), headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            response_body = response.read().decode()
            response_data = json.loads(response_body)
            #print(response_data)
        else:
            response_data = {"success": False, "message": "No response from server"}
        conn.close()
        return response_data

    def get_purchase_history(self, username):
        request = {"action": "get_purchase_history", "username": username}

        host, port = random.choice(BUYER_SERVER_LIST[:BUYER_SERVER_N])
        port = int(port)

        conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)
        headers = {'Content-type': 'application/json'}
        conn.request('POST', '/get_purchase_history', body=json.dumps(request), headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            response_body = response.read().decode()
            response_data = json.loads(response_body)
            #print(response_data["message"])
            #print(response_data["purchaseHistory"])
        else:
            response_data = {"success": False, "message": "No response from server"}
        conn.close()
        return response_data


    def make_purchase(self, username, creditcard ):
        request = {"action": "make_purchase", "username": username, "creditcard":creditcard}

        host, port = random.choice(BUYER_SERVER_LIST[:BUYER_SERVER_N])
        port = int(port)

        conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)
        headers = {'Content-type': 'application/json'}
        conn.request('POST', '/make_purchase', body=json.dumps(request), headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            response_body = response.read().decode()
            response_data = json.loads(response_body)
            #print(response_data["message"])
            #print(response_data)
        else:
            response_data = {"success": False, "message": "No response from server"}
        conn.close()
        return response_data

    def get_seller_rating(self, username):
        request = {"action": "get_seller_rating", "username": username}

        host, port = random.choice(BUYER_SERVER_LIST[:BUYER_SERVER_N])
        port = int(port)

        conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)
        headers = {'Content-type': 'application/json'}
        conn.request('POST', '/get_seller_rating', body=json.dumps(request), headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            response_body = response.read().decode()
            response_data = json.loads(response_body)
            #print("positive:"+ str(response_data["ratingPos"]) )
            #print("negative:"+ str(response_data["ratingNeg"]) )
        else:
            response_data = {"success": False, "message": "No response from server"}
        conn.close()
        return response_data




def handle_interface(client):
    cmd = int(input('Enter command:'))

    if cmd == 0:
        request = {"action": "create_buyer", "username": "", "password": "", "name": ""}
        print(request['action'])
        for key in request.keys():
            if key == "action":
                continue
            else:
                request[key] = input('Enter ' + key + ' : ')
        
        # convert input to proper data format string, int, double etc.

        response = client.create_account(request)
        print(response)


    return 0



def start_client():
    
    max_iterations = 10

    client = BuyerClient()
    start_time = time.time()

    for i in range(max_iterations):

        client.create_account("12345","1234","1234")
        
        client.login("12345","1234")

        client.add_to_cart("12345", 123445, 1)

        client.display_cart("12345")

        client.make_purchase("12345", "12345678")

        client.get_purchase_history("12345")

        client.clear_cart("12345")

        keywords = ["k1","k2","k3"]
        
        client.search_items(0, keywords, "12345")

        client.get_seller_rating("123")

        client.logout("12345")

        print(i, time.time() - start_time)



    end_time = time.time()
    total_time = end_time - start_time


    print(total_time)




if __name__ == '__main__':
    
    start_client()







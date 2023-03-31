import urllib.request
import json
import http.client
import time

# Global Variables

BUFFER_SIZE = 4096
TIME_OUT = 10
MAX_WAITING_CONNECTIONS = 50000

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

class BuyerClient:

    def create_account(self, username, password, name):
        request = {"action": "create_buyer", "username": username, "password": password, "name":name}
        conn = http.client.HTTPConnection(BUYER_SERVER_HOST, BUYER_SERVER_PORT, timeout=TIME_OUT)
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
        conn = http.client.HTTPConnection(BUYER_SERVER_HOST, BUYER_SERVER_PORT, timeout=TIME_OUT)
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
        conn = http.client.HTTPConnection(BUYER_SERVER_HOST, BUYER_SERVER_PORT, timeout=TIME_OUT)
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
        conn = http.client.HTTPConnection(BUYER_SERVER_HOST, BUYER_SERVER_PORT, timeout=TIME_OUT)
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
        conn = http.client.HTTPConnection(BUYER_SERVER_HOST, BUYER_SERVER_PORT, timeout=TIME_OUT)
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
        conn = http.client.HTTPConnection(BUYER_SERVER_HOST, BUYER_SERVER_PORT, timeout=TIME_OUT)
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
        conn = http.client.HTTPConnection(BUYER_SERVER_HOST, BUYER_SERVER_PORT, timeout=TIME_OUT)
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
        conn = http.client.HTTPConnection(BUYER_SERVER_HOST, BUYER_SERVER_PORT, timeout=TIME_OUT)
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
        conn = http.client.HTTPConnection(BUYER_SERVER_HOST, BUYER_SERVER_PORT, timeout=TIME_OUT)
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
        conn = http.client.HTTPConnection(BUYER_SERVER_HOST, BUYER_SERVER_PORT, timeout=TIME_OUT)
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
        conn = http.client.HTTPConnection(BUYER_SERVER_HOST, BUYER_SERVER_PORT, timeout=TIME_OUT)
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
    
    client = BuyerClient()

    # handle_interface(client)

    # ###############################call functions################################
    max_iterations=100

    start_time=time.time()
    for i in range(max_iterations):

    #     response = client.create_account("username"+str(i), "password"+str(i), "name"+str(i))
    #     response = client.login("username"+str(i), "password"+str(i))
    #     response = client.add_to_cart("username"+str(i), i, 1)
    #     response = client.view_cart("username"+str(i))
    #     response = client.remove_cart("username"+str(i), i, 1)



        client.create_account("12345","1234","1234")
        client.login("12345","1234")


        client.add_to_cart("12345",123445,1)
        client.display_cart("12345")

        #client.make_purchase("12345","12345678")
        #client.get_purchase_history("12345")

        client.clear_cart("12345")

        keywords=["k1","k2","k3"]
        
        #client.search_items(0,keywords,"12345")

        client.get_seller_rating("123")
        client.logout("12345")




    end_time = time.time()
    time_for_1000_apicalls=end_time - start_time


    print(time_for_1000_apicalls)




if __name__ == '__main__':
    
    start_client()







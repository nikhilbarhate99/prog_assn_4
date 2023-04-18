import urllib.request
import json
import http.client
import time
import random

from global_variables import *



class SellerClient:

    def create_account(self, username, password, name):

        for _ in range(CLIENT_RETRIES_N):
            request = {"action": "create_seller", "username": username, "password": password, "name":name}

            host, port = random.choice(SELLER_SERVER_LIST[:SELLER_SERVER_N])
            port = int(port)

            conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)

            headers = {'Content-type': 'application/json'}

            conn.request('POST', '/create_seller', body=json.dumps(request), headers=headers)

            response = conn.getresponse()
            conn.close()

            if response.status == 200:

                response_body = response.read().decode()

                response_data = json.loads(response_body)

                #print(response_data["message"])
                break
                
            else:

                response_data = {"success": False, "message": "No response from server"}

            

        return response_data



    def login(self, username, password):

        for _ in range(CLIENT_RETRIES_N):
                
            request = {"action": "login_seller", "username": username, "password": password}

            host, port = random.choice(SELLER_SERVER_LIST[:SELLER_SERVER_N])
            port = int(port)

            conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)

            headers = {'Content-type': 'application/json'}

            conn.request('POST', '/login_seller', body=json.dumps(request), headers=headers)

            response = conn.getresponse()
            conn.close()
            

            if response.status == 200:

                response_body = response.read().decode()

                response_data = json.loads(response_body)

                #print(response_data["message"])
                break

            else:

                response_data = {"success": False, "message": "No response from server"}

            

        return response_data



    def logout(self, username):

        for _ in range(CLIENT_RETRIES_N):
                
            request = {"action": "logout_seller", "username": username}

            host, port = random.choice(SELLER_SERVER_LIST[:SELLER_SERVER_N])
            port = int(port)

            conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)

            headers = {'Content-type': 'application/json'}

            conn.request('POST', '/logout_seller', body=json.dumps(request), headers=headers)

            response = conn.getresponse()
            conn.close()
            

            if response.status == 200:

                response_body = response.read().decode()

                response_data = json.loads(response_body)

    #            print(response_data["message"])
                break

            else:

                response_data = {"success": False, "message": "No response from server"}

            

        return response_data



    def get_seller_rating(self, username):

        for _ in range(CLIENT_RETRIES_N):
                
            request = {"action": "get_seller_rating", "username": username}
            
            host, port = random.choice(SELLER_SERVER_LIST[:SELLER_SERVER_N])
            port = int(port)

            conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)

            headers = {'Content-type': 'application/json'}

            conn.request('POST', '/get_seller_rating', body=json.dumps(request), headers=headers)

            response = conn.getresponse()
            conn.close()
            

            if response.status == 200:

                response_body = response.read().decode()

                response_data = json.loads(response_body)

    #            print("positive:"+ str(response_data["ratingPos"]) )

    #           print("negative:"+ str(response_data["ratingNeg"]) )
                break

            else:

                response_data = {"success": False, "message": "No response from server"}

            

        return response_data



    def add_item(self, username, item, quantity):

        for _ in range(CLIENT_RETRIES_N):
                
            request = {"action": "add_item", "item": item, "quantity":quantity,"username":username}

            host, port = random.choice(SELLER_SERVER_LIST[:SELLER_SERVER_N])
            port = int(port)

            conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)

            headers = {'Content-type': 'application/json'}

            conn.request('POST', '/add_item', body=json.dumps(request), headers=headers)

            response = conn.getresponse()
            conn.close()
            

            if response.status == 200:

                response_body = response.read().decode()

                response_data = json.loads(response_body)

    #          print(response_data["message"])
                break

            else:

                response_data = {"success": False, "message": "No response from server"}

            

        return response_data

            

    def remove_item(self,  prod_id, quantity,username):

        for _ in range(CLIENT_RETRIES_N):
                
            request = {"action": "remove_item", "prod_id": prod_id, "quantity": quantity,"username":username}

            host, port = random.choice(SELLER_SERVER_LIST[:SELLER_SERVER_N])
            port = int(port)

            conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)

            headers = {'Content-type': 'application/json'}

            conn.request('POST', '/remove_item', body=json.dumps(request), headers=headers)

            response = conn.getresponse()
            conn.close()
            

            if response.status == 200:

                response_body = response.read().decode()

                response_data = json.loads(response_body)

    #            print(response_data["message"])
                break

            else:

                response_data = {"success": False, "message": "No response from server"}

            

        return response_data



        

    def change_price(self, prod_id, new_price,username):

        for _ in range(CLIENT_RETRIES_N):
                
            request = {"action": "change_price", "prod_id": prod_id,"new_price": new_price,"username":username}

            host, port = random.choice(SELLER_SERVER_LIST[:SELLER_SERVER_N])
            port = int(port)

            conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)

            headers = {'Content-type': 'application/json'}

            conn.request('POST', '/change_price', body=json.dumps(request), headers=headers)

            response = conn.getresponse()
            conn.close()
            

            if response.status == 200:

                response_body = response.read().decode()

                response_data = json.loads(response_body)

    #           print(response_data["message"])
                break

            else:

                response_data = {"success": False, "message": "No response from server"}

            

        return response_data





    def all_items_by_seller(self, username):

        for _ in range(CLIENT_RETRIES_N):
                
            request = {"action": "all_items_by_seller", "username": username}

            host, port = random.choice(SELLER_SERVER_LIST[:SELLER_SERVER_N])
            port = int(port)

            conn = http.client.HTTPConnection(host, port, timeout=HTTP_TIME_OUT)

            headers = {'Content-type': 'application/json'}

            conn.request('POST', '/all_items_by_seller', body=json.dumps(request), headers=headers)

            response = conn.getresponse()
            conn.close()
            

            if response.status == 200:

                response_body = response.read().decode()

                response_data = json.loads(response_body)

    #          print(response_data)
                break

            else:

                response_data = {"success": False, "message": "No response from server"}

            

        return response_data



def start_client():

    max_iterations = 10


    client = SellerClient()
    start_time = time.time()

    for i in range(max_iterations):

        client.create_account("123","123","123")

        client.login("123","123")

        item = {"name": "item2", 
                "category" : 0, 
                "condition" : "new", 
                "keywords" : ("k1", "k2", "k3"), 
                "price" : 100
                }

        client.add_item("123",item,"12")

        client.get_seller_rating("123")

        client.remove_item(0,3,"123")

        client.change_price(123,50,"123")

        client.all_items_by_seller("123")


        print(i, time.time() - start_time)


    end_time = time.time()

    total_time = end_time - start_time

    print(total_time)




if __name__ == '__main__':

    start_client()
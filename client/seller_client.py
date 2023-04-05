import urllib.request
import json
import http.client
import time

from global_variables import *



class SellerClient:

    def create_account(self, username, password, name):

        request = {"action": "create_seller", "username": username, "password": password, "name":name}

        conn = http.client.HTTPConnection(SELLER_SERVER_HOST, SELLER_SERVER_PORT, timeout=HTTP_TIME_OUT)

        headers = {'Content-type': 'application/json'}

        conn.request('POST', '/create_seller', body=json.dumps(request), headers=headers)

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

        request = {"action": "login_seller", "username": username, "password": password}

        conn = http.client.HTTPConnection(SELLER_SERVER_HOST, SELLER_SERVER_PORT, timeout=HTTP_TIME_OUT)

        headers = {'Content-type': 'application/json'}

        conn.request('POST', '/login_seller', body=json.dumps(request), headers=headers)

        response = conn.getresponse()

        if response.status == 200:

            response_body = response.read().decode()

            response_data = json.loads(response_body)

            #print(response_data["message"])

        else:

            response_data = {"success": False, "message": "No response from server"}

        conn.close()

        return response_data



    def logout(self, username):

        request = {"action": "logout_seller", "username": username}

        conn = http.client.HTTPConnection(SELLER_SERVER_HOST, SELLER_SERVER_PORT, timeout=HTTP_TIME_OUT)

        headers = {'Content-type': 'application/json'}

        conn.request('POST', '/logout_seller', body=json.dumps(request), headers=headers)

        response = conn.getresponse()

        if response.status == 200:

            response_body = response.read().decode()

            response_data = json.loads(response_body)

#            print(response_data["message"])

        else:

            response_data = {"success": False, "message": "No response from server"}

        conn.close()

        return response_data



    def get_seller_rating(self, username):

        request = {"action": "get_seller_rating", "username": username}

        conn = http.client.HTTPConnection(SELLER_SERVER_HOST, SELLER_SERVER_PORT, timeout=HTTP_TIME_OUT)

        headers = {'Content-type': 'application/json'}

        conn.request('POST', '/get_seller_rating', body=json.dumps(request), headers=headers)

        response = conn.getresponse()

        if response.status == 200:

            response_body = response.read().decode()

            response_data = json.loads(response_body)

#            print("positive:"+ str(response_data["ratingPos"]) )

 #           print("negative:"+ str(response_data["ratingNeg"]) )

        else:

            response_data = {"success": False, "message": "No response from server"}

        conn.close()

        return response_data



    def add_item(self, username, item, quantity):

        request = {"action": "add_item", "item": item, "quantity":quantity,"username":username}

        conn = http.client.HTTPConnection(SELLER_SERVER_HOST, SELLER_SERVER_PORT, timeout=HTTP_TIME_OUT)

        headers = {'Content-type': 'application/json'}

        conn.request('POST', '/add_item', body=json.dumps(request), headers=headers)

        response = conn.getresponse()

        if response.status == 200:

            response_body = response.read().decode()

            response_data = json.loads(response_body)

  #          print(response_data["message"])

        else:

            response_data = {"success": False, "message": "No response from server"}

        conn.close()

        return response_data

            

    def remove_item(self,  prod_id, quantity,username):

        request = {"action": "remove_item", "prod_id": prod_id, "quantity": quantity,"username":username}

        conn = http.client.HTTPConnection(SELLER_SERVER_HOST, SELLER_SERVER_PORT, timeout=HTTP_TIME_OUT)

        headers = {'Content-type': 'application/json'}

        conn.request('POST', '/remove_item', body=json.dumps(request), headers=headers)

        response = conn.getresponse()

        if response.status == 200:

            response_body = response.read().decode()

            response_data = json.loads(response_body)

#            print(response_data["message"])

        else:

            response_data = {"success": False, "message": "No response from server"}

        conn.close()

        return response_data



        

    def change_price(self, prod_id, new_price,username):

        request = {"action": "change_price", "prod_id": prod_id,"new_price": new_price,"username":username}

        conn = http.client.HTTPConnection(SELLER_SERVER_HOST, SELLER_SERVER_PORT, timeout=HTTP_TIME_OUT)

        headers = {'Content-type': 'application/json'}

        conn.request('POST', '/change_price', body=json.dumps(request), headers=headers)

        response = conn.getresponse()

        if response.status == 200:

            response_body = response.read().decode()

            response_data = json.loads(response_body)

 #           print(response_data["message"])

        else:

            response_data = {"success": False, "message": "No response from server"}

        conn.close()

        return response_data





    def all_items_by_seller(self, username):

        request = {"action": "all_items_by_seller", "username": username}

        conn = http.client.HTTPConnection(SELLER_SERVER_HOST, SELLER_SERVER_PORT, timeout=HTTP_TIME_OUT)

        headers = {'Content-type': 'application/json'}

        conn.request('POST', '/all_items_by_seller', body=json.dumps(request), headers=headers)

        response = conn.getresponse()

        if response.status == 200:

            response_body = response.read().decode()

            response_data = json.loads(response_body)

  #          print(response_data)

        else:

            response_data = {"success": False, "message": "No response from server"}

        conn.close()

        return response_data







def start_client():

    

    client = SellerClient()

    # ###############################call functions################################

    max_iterations=100



    start_time=time.time()

    for i in range(max_iterations):



    # end_time = time.time()

    # time_for_1000_apicalls=end_time - start_time



        client.create_account("123","123","123")

        client.login("123","123")

        # client.logout("123")

        #['name', 'condition', 'category', 'price', 'keywords']

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

    end_time=time.time()
    print(end_time-start_time)

if __name__ == '__main__':

    

    start_client()
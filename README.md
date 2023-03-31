
## CSCI 5673 Distributed Systems programming assignment 2

Nikhil Barhate and Sriranga Kalkunte Ramaswamy


### To Run

```
python3 -m customer_DB.customer_db
python3 -m product_DB.product_db
python3 -m server.buyer_server
python3 -m server.seller_server

```

```
python3 -m client.test_seller
python3 -m client.test_buyer
```




### Design aspects:

    1. Communication between server and DB is acheived using gRPC
    2. Communication between client and server is acheived using REST API via HTTP
    3. All request messages contain a string variable ('action') to determine the requested functionality.
    4. All response messages contain a boolean variable ('success') to determine the status of the request.
    5. The data is stored in memory on these separate services in the form of nested python dictionaries.

### Assumptions:

    - for the search function, the keywords in the database exactly match the keywords in the query
    - while removing an item if updated quantity is less than or equal to 0, then the item is removed from the database
    - while viewing the cart the buyer can see product ids only, rest of the product characterstics 
        can be refered from results of the search query.


### Things that work:

    - seller side:
        - create a new seller account
        - login / logout a seller account
        - get seller rating
        - put an item for sale 
        - change the sale price of an item
        - remove and item from sale 
        - display all items by this seller
    
    - buyer side:
        - create a new buyer account 
        - login / logout a buyer account 
        - search items for sale 
        - add item to cart 
        - remove item from cart 
        - clear cart 
        - display cart 
        - make purchase
        


### Things that do not work:

    - Little to no exception handling






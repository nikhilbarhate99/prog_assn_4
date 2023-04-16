
## CSCI 5673 Distributed Systems programming assignment 2

Nikhil Barhate and Sriranga Kalkunte Ramaswamy


### To Run

```
python3 -m customer_DB.customer_db --node_id 0
python3 -m product_DB.product_db --node_id 0
python3 -m server.buyer_server --node_id 0
python3 -m server.seller_server --node_id 0
python3 -m financial_transaction
```

```
python3 -m client.seller_client
python3 -m client.buyer_client

python3 -m client.test_seller
python3 -m client.test_buyer
```




### Design aspects:

    1. Communication between server and DB is acheived using gRPC
    2. Communication between client and server is acheived using REST API via HTTP
    3. Customer DB is replicated using a custom Atomic Broadcast protocol
    4. This protocol assumes only transient communication failures (i.e. no partition and no process failure)
    5. A global sequence number 's' is assigned by node with id, s % num_nodes.
    6. With these assumptions, a RPC request with assigned global sequence cannot be lost, hence a majority check is not necessary before delivering a msg and is not implemented.


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

    - Atomic Broadcast protocol for Customer DB is slow and not optimized for performance
    - Little to no exception handling






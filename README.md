
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

### Performance Numbers:

#### scenarios

1. Average response time for each client function when all replicas run normally (no failures).
2. Average response time for each client function when one server-side sellers interface replica and one server-side buyers interface to which some of the clients are connected fail.
3. Average response time for each client function when one product database replica (not the leader) fails.
4. Average response time for each client function when the product database replica acting as leader fails.


#### Average Response time (sec)

| seller client function | scenario 1 | scenario 2 | scenario 3 | scenario 4 |
| --- | --- | --- | --- | --- |
| create_seller | 0 | 0 | 0 | 0 |
| login_seller | 0 | 0 | 0 | 0 |
| logout_seller | 0 | 0 | 0 | 0 |
| get_seller_rating | 0 | 0 | 0 | 0 |
| add_item | 0 | 0 | 0 | 0 |
| remove_item | 0 | 0 | 0 | 0 |
| change_price | 0 | 0 | 0 | 0 |
| all_items_by_seller | 0 | 0 | 0 | 0 |


| buyer client function | scenario 1 | scenario 2 | scenario 3 | scenario 4 |
| --- | --- | --- | --- | --- |
| create_buyer | 0 | 0 | 0 | 0 |
| login_buyer | 0 | 0 | 0 | 0 |
| logout_buyer | 0 | 0 | 0 | 0 |
| display_cart | 0 | 0 | 0 | 0 |
| add_to_cart | 0 | 0 | 0 | 0 |
| remove_cart | 0 | 0 | 0 | 0 |
| clear_cart | 0 | 0 | 0 | 0 |
| search_items | 0 | 0 | 0 | 0 |
| get_purchase_history | 0 | 0 | 0 | 0 |
| make_purchase | 0 | 0 | 0 | 0 |
| get_seller_rating | 0 | 0 | 0 | 0 |




### Design aspects:

    1. Communication between server and DB is acheived using gRPC
    2. Communication between client and server is acheived using REST API via HTTP
    3. Customer DB is replicated using a custom Atomic Broadcast protocol
    4. This protocol assumes only transient communication failures (i.e. no partition and no process failure)
    5. A global sequence number 's' is assigned by node with id, s % num_nodes.
    6. With these assumptions, a RPC request with assigned global sequence cannot be lost, hence a majority check is not necessary before delivering a msg and is not implemented.


### Things that work:

    - Customer DB using atomic broadcast protocol
    - Product DB using raft

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






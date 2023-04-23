
## CSCI 5673 Distributed Systems PA 4

Nikhil Barhate and Sriranga Kalkunte Ramaswamy


### Performance Numbers:

#### Scenarios

1. Average response time for each client function when all replicas run normally (no failures).
2. Average response time for each client function when one server-side sellers interface replica and one server-side buyers interface to which some of the clients are connected fail.
3. Average response time for each client function when one product database replica (not the leader) fails.
4. Average response time for each client function when the product database replica acting as leader fails.


#### Average Response time (sec)

| seller client function | scenario 1 | scenario 2 | scenario 3 | scenario 4 |
| --- | --- | --- | --- | --- |
| create_seller | 0.9269 | 0.8709 | 0.8681 | 0.8334 |
| login_seller | 0.8855 | 0.8829 | 0.8864 | 0.9001 |
| add_item | 1.0717 | 1.1217 | 1.2141 | 1.2264 |
| get_seller_rating | 0.7836 | 0.7911 | 0.9193 | 0.8042 |
| remove_item | 0.9468 | 1.1188 | 1.0768 | 1.2526 |
| change_price | 1.0346 | 1.0576 | 1.0789 | 1.1936 |
| all_items_by_seller | 0.8256 | 0.8315 | 0.9236 | 0.9287 |
| logout_seller | 0.8144 | 0.8395 | 0.8892 | 0.8718 |

| buyer client function | scenario 1 | scenario 2 | scenario 3 | scenario 4 |
| --- | --- | --- | --- | --- |
| create_buyer | 0.9150 | 0.9715 | 0.9245 | 0.9762 |
| login_buyer | 0.8894 | 0.9575 | 0.9771 | 0.9812 |
| logout_buyer | 0.8216 | 0.9891 | 0.9802 | 0.9955 |
| display_cart | 1.6051 | 1.7531 | 1.6262 | 1.6594 |
| add_to_cart | 1.8829 | 1.9215 | 1.9287 | 1.9755 |
| remove_cart | 0.8497 | 0.8562 | 0.8519 | 0.8630 |
| clear_cart | 1.4623 | 1.6972 | 1.6436 | 1.6320 |
| search_items | 0.5687 | 0.5781 | 0.5946 | 0.5910 |
| get_purchase_history | 1.7875 | 1.8618 | 1.8720 | 1.8609 |
| make_purchase | 2.6436 | 2.5718 | 3.6691 | 3.3875 |
| get_seller_rating | 0.6987 | 0.7258 | 0.7967 | 0.8483 |




### Design aspects:

    1. Communication between server and DB is acheived using gRPC
    2. Communication between client and server is acheived using REST API via HTTP
    3. Customer DB is replicated using a custom Atomic Broadcast protocol
    4. This protocol assumes only transient communication failures (i.e. no partition and no process failure)
    5. A global sequence number 's' is assigned by node with id, s % num_nodes.
    6. With these assumptions, a RPC request with assigned global sequence cannot be lost, hence a majority check is not necessary before delivering a msg.


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





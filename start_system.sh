#!/bin/bash

python3 -m customer_DB.customer_db
python3 -m product_DB.product_db
python3 -m server.buyer_server
python3 -m server.seller_server


# Global Variables

# ====================================================

HTTP_TIME_OUT = 10
MAX_WORKERS = 1     # Keep it 1 for sequential Customer DB (otherwise concurrent)

CUSTOMER_DB_MAX_WORKERS = 1

UDP_SOCKET_TIMEOUT = 1.0
UDP_PACKET_SIZE = 1024 # 1024 / 4096 / 8192

META_DATA_DELIM = ';'
WHILE_LOOP_DELAY = 0.3

# ====================================================

FINANCIAL_TRANSACTION_HOST = '127.0.0.1'
FINANCIAL_TRANSACTION_PORT = '50000'

BUYER_SERVER_HOST = '127.0.0.1'
BUYER_SERVER_PORT = '10000'

SELLER_SERVER_HOST = '127.0.0.1'
SELLER_SERVER_PORT = '20000'

PRODUCT_DB_HOST = '127.0.0.1'
PRODUCT_DB_PORT = '30000'

CUSTOMER_DB_HOST = '127.0.0.1'
CUSTOMER_DB_PORT = '40000'

# ====================================================

BUYER_SERVER_HOST_0 = '127.0.0.1'
BUYER_SERVER_PORT_0 = '10001'

BUYER_SERVER_HOST_1 = '127.0.0.1'
BUYER_SERVER_PORT_1 = '10002'

BUYER_SERVER_HOST_2 = '127.0.0.1'
BUYER_SERVER_PORT_2 = '10003'

BUYER_SERVER_HOST_3 = '127.0.0.1'
BUYER_SERVER_PORT_3 = '10004'

BUYER_SERVER_HOST_4 = '127.0.0.1'
BUYER_SERVER_PORT_4 = '10005'

BUYER_SERVER_LIST = [
            (BUYER_SERVER_HOST_0, BUYER_SERVER_PORT_0),
            (BUYER_SERVER_HOST_1, BUYER_SERVER_PORT_1),
            (BUYER_SERVER_HOST_2, BUYER_SERVER_PORT_2),
            (BUYER_SERVER_HOST_3, BUYER_SERVER_PORT_3),
            (BUYER_SERVER_HOST_4, BUYER_SERVER_PORT_4),
        ]


# ====================================================

SELLER_SERVER_HOST_0 = '127.0.0.1'
SELLER_SERVER_PORT_0 = '20001'

SELLER_SERVER_HOST_1 = '127.0.0.1'
SELLER_SERVER_PORT_1 = '20002'

SELLER_SERVER_HOST_2 = '127.0.0.1'
SELLER_SERVER_PORT_2 = '20003'

SELLER_SERVER_HOST_3 = '127.0.0.1'
SELLER_SERVER_PORT_3 = '20004'

SELLER_SERVER_HOST_4 = '127.0.0.1'
SELLER_SERVER_PORT_4 = '20005'

SELLER_SERVER_LIST = [
            (SELLER_SERVER_HOST_0, SELLER_SERVER_PORT_0),
            (SELLER_SERVER_HOST_1, SELLER_SERVER_PORT_1),
            (SELLER_SERVER_HOST_2, SELLER_SERVER_PORT_2),
            (SELLER_SERVER_HOST_3, SELLER_SERVER_PORT_3),
            (SELLER_SERVER_HOST_4, SELLER_SERVER_PORT_4),
        ]


# ====================================================

PRODUCT_DB_HOST_0 = '127.0.0.1'
PRODUCT_DB_PORT_0 = '30001'

PRODUCT_DB_HOST_1 = '127.0.0.1'
PRODUCT_DB_PORT_1 = '30002'

PRODUCT_DB_HOST_2 = '127.0.0.1'
PRODUCT_DB_PORT_2 = '30003'

PRODUCT_DB_HOST_3 = '127.0.0.1'
PRODUCT_DB_PORT_3 = '30004'

PRODUCT_DB_HOST_4 = '127.0.0.1'
PRODUCT_DB_PORT_4 = '30005'

PRODUCT_DB_LIST = [
            (PRODUCT_DB_HOST_0, PRODUCT_DB_PORT_0),
            (PRODUCT_DB_HOST_1, PRODUCT_DB_PORT_1),
            (PRODUCT_DB_HOST_2, PRODUCT_DB_PORT_2),
            (PRODUCT_DB_HOST_3, PRODUCT_DB_PORT_3),
            (PRODUCT_DB_HOST_4, PRODUCT_DB_PORT_4),
        ]

# ====================================================

CUSTOMER_DB_HOST_0 = '127.0.0.1'
CUSTOMER_DB_PORT_0 = '40001'

CUSTOMER_DB_HOST_1 = '127.0.0.1'
CUSTOMER_DB_PORT_1 = '40002'

CUSTOMER_DB_HOST_2 = '127.0.0.1'
CUSTOMER_DB_PORT_2 = '40003'

CUSTOMER_DB_HOST_3 = '127.0.0.1'
CUSTOMER_DB_PORT_3 = '40004'

CUSTOMER_DB_HOST_4 = '127.0.0.1'
CUSTOMER_DB_PORT_4 = '40005'

CUSTOMER_DB_LIST = [
            (CUSTOMER_DB_HOST_0, CUSTOMER_DB_PORT_0),
            (CUSTOMER_DB_HOST_1, CUSTOMER_DB_PORT_1),
            (CUSTOMER_DB_HOST_2, CUSTOMER_DB_PORT_2),
            (CUSTOMER_DB_HOST_3, CUSTOMER_DB_PORT_3),
            (CUSTOMER_DB_HOST_4, CUSTOMER_DB_PORT_4),
        ]





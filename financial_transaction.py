from spyne import Application, rpc, ServiceBase, Integer, String, Boolean
# from spyne.model.primitive import Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import random

from global_variables import *


class YesNoService(ServiceBase):
    @rpc(Integer,String,String , _returns=Boolean)
    def get_yes_or_no(ctx, num, creditcard, username):
        if random.random() < 0.1:
            return False
        else:
            return True


if __name__ == '__main__':
    application = Application([YesNoService], 'test', in_protocol=Soap11(validator='lxml'),out_protocol=Soap11())
    wsgi_application = WsgiApplication(application)
    from wsgiref.simple_server import make_server
    server = make_server(FINANCIAL_TRANSACTION_HOST, int(FINANCIAL_TRANSACTION_PORT), wsgi_application)

    
    print("=============================")
    print("Server running")
    print("=============================")
    
    server.serve_forever()

    print("=============================")
    print("Server shutdown")
    print("=============================")


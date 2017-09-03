from debug import *
from zoodb import *
import rpclib

def login(username, password):
    ## Fill in code here.
    
    with rpclib.client_connect('/authsvc/sock') as c:
        token = c.call('login', username=username, password=password)
        return token
        

def register(username, password):
    ## Fill in code here.

def check_token(username, token):
    ## Fill in code here.
    with rpclib.client_connect('/authsvc/sock') as c:
        ret_token = c.call('check_token', username=username)
        if ret_token is not None and ret_token == token:
            return True
        else:
            return False

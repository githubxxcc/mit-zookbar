#!/usr/bin/python

import rpclib
import sys
import auth
from debug import *

class AuthRpcServer(rpclib.RpcServer):
    def rpc_login(self, username, password):
        db = cred_setup()
        cred = db.query(Cred).get(username)
        if not cred:
            return None 
        if cred.password == password:
            return auth.newtoken(db, cred)
        else:
            return None
 
    #def rpc_check_token(self, s):





(_, dummy_zookld_fd, sockpath) = sys.argv

s = AuthRpcServer()
s.run_sockpath_fork(sockpath)

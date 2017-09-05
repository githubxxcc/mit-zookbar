#!/usr/bin/python
#
# Insert bank server code here.
#

import rpclib
import sys
import time
from zoodb import *
from debug import *

class BankRpcServer(rpclib.RpcServer):
    def rpc_transfer(self, sender, recipient, zoobars):
        bankdb = bank_setup()
        senderB = bankdb.query(Bank).get(sender)
        recipientB = bankdb.query(Bank).get(recipient)
        
        s_bal = senderB.zoobars - zoobars
        r_bal = recipientB.zoobars + zoobars

        if s_bal < 0 or r_bal < 0:
            raise ValueError()

        senderB.zoobars = s_bal
        recipientB.zoobars = r_bal
        bankdb.commit()
        
        transfer = Transfer()
        transfer.sender = sender
        transfer.recipient = recipient
        transfer.time = time.asctime()
        transfer.amount = zoobars

        transferdb = transfer_setup()
        transferdb.add(transfer)
        transferdb.commit()        

    def rpc_balance(self, username):
        db = bank_setup()
        acc = db.query(Bank).get(username)
        return acc.zoobars
    
    def rpc_get_log(self, username):
        db = transfer_setup()
        logs = db.query(Transfer).filter(or_(Transfer.sender==username, 
                                             Transfer.recipient==username))
        if logs is not None:
            return logs
        else:
            return None
    
    def rpc_init_account(self, username):
        db = bank_setup()
        acc = Bank()
        acc.username = username

        db.add(acc)
        db.commit()



(_, dummy_zookld_fd, sockpath) = sys.argv

s = BankRpcServer()
s.run_sockpath_fork(sockpath)

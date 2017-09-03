from zoodb import *
from debug import *

import hashlib
import random

#def newtoken(db, person):
#    hashinput = "%s%.10f" % (person.password, random.random())
#    person.token = hashlib.md5(hashinput).hexdigest()
#    db.commit()
#    return person.token

def newtoken(db, cred):
    hashinput = "%s%.10f" % (cred.password, random.random())
    cred.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return cred.token
   

def login(username, password):
    db = person_setup()
    person = db.query(Person).get(username)
    if not person:
        return None
    if person.password == password:
        return newtoken(db, person)
    else:
        return None

def register(username, password):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if cred:
        return None
    new_cred = Cred()
    new_cred.username = username
    new_cred.password = password
    db.add(new_cred)
    db.commit()

    return newtoken(db, new_cred)    


def check_token(username, token):
    db = person_setup()
    person = db.query(Person).get(username)
    if person and person.token == token:
        return True
    else:
        return False

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
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if not cred:
        return None
    if cred.password == password:
        return newtoken(db, cred)
    else:
        return None    


def register(username, password):
    cred_db = cred_setup()
    cred = cred_db.query(Cred).get(username)
    if cred:
        return None

    person_db = person_setup()
    person = person_db.query(Person).get(username)
    
    if person: 
        return None

    new_cred = Cred()
    new_cred.username = username
    new_cred.password = password
    cred_db.add(new_cred)

    new_person = Person()
    new_person.username = username
    person_db.add(new_person)

    cred_db.commit()
    person_db.commit()

    return newtoken(cred_db, new_cred)    


def check_token(username, token):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if cred and cred.token == token:
        return True
    else:
        return False


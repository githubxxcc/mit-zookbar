from zoodb import *
from debug import *
from base64 import b64encode, b64decode

import hashlib
import random
import pbkdf2


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

    test_password = pbkdf2.PBKDF2(password, b64decode(cred.salt)).hexread(32)
    if cred.password == test_password:
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
    salt = os.urandom(8)
    new_cred.salt = b64encode(salt)
    new_cred.password = pbkdf2.PBKDF2(password,salt).hexread(32)
    new_cred.username = username

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


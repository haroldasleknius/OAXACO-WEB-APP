import hashlib
import bcrypt

def salting():
    salt = bcrypt.gensalt().decode('utf-8')
    return salt

def hashingLocally(password):
    password = hashlib.sha3_256(password.encode()).hexdigest()
    return password

def hashingFromDatabase(salt,password):
    if len(salt) > 0:
        salt = salt[0]
        salt = salt[0]
        password = password + salt
    password = hashlib.sha3_256(password.encode()).hexdigest()
    return password

def authenticate(password,comparePassword):
    if password in str(comparePassword):
        return True
    return False

def authenticateRole(role):
    Waiter = 'Waiter'
    Kitchen = 'Kitchen'
    Customer = 'Customer'
    if Waiter in str(role):
        return Waiter
    elif Kitchen in str(role):
        return Kitchen
    else:
        return Customer
    

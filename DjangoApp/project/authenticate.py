dictionary = {"Haroldas": "33c36592000fdca92f064fe43b385f11bd7fa884e8dccab41185c493e34ee859"}

def authenticate(username,password):
    if dictionary[username] == password:
        return True
    return False
import random

salt_user = {}
def get_salt_login():
    ALPHABET = "!@#$0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars=[]
    for _ in range(16):
        chars.append(random.choice(ALPHABET))
    salt = "".join(chars)

    salt_user["user"] = salt
    return salt

password = "asenha" + get_salt_login()
data ={"username": "user",
       "password": password}


print('password: ',password)

def remove_salt(data):
    print(salt_user[data['username']])
    print(data['password'])
    if salt_user[data['username']] in data['password']:
        data['password'] = data['password'].replace(salt_user[data['username']], '')
        return data
    return False

data = remove_salt(data)
print(salt_user)
print(data)
print(salt_user)
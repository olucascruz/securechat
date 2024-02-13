import json
import os
from utils import generate_unique_id

folder_path = os.getcwd() 
path_db_users = os.path.join(folder_path, r'db\users.json')

def get_users():
    with open(path_db_users, 'r') as file:
        db = json.load(file)    
    return db

def get_users_without_password():
    db = get_users()
    data = []
    for user in db:
        data_user = {
            "username":db[user]["username"],
            "id":user,
            "is_online":db[user]["is_online"],
            }
        data.append(data_user)
    
    return data

def auth_user(username:str, password:str)->str:
    users = get_users()
    for user_id in users:
        is_auth = (users[user_id]['username'] == username and
                   users[user_id]['password'] == password)
        
        if is_auth: return user_id

def insert_user(username:str, password:str) -> bool:
    users = get_users()
    print("insert user")
    for user_id in users:
        if users[user_id]['username'] == username:
            return False
    new_user = {
        "username":username,
        "password":password,
        "is_online":False,
        "public_key":""
    }

    new_id = generate_unique_id(users.keys())
    users[new_id] = new_user

    with open(path_db_users, 'w') as file:
        json.dump(users, file, indent=2)

    return True

    

def update_user(id, new_public_key='', is_online=False):
    users = get_users()

    users[id]['public_key'] = str(new_public_key)
    users[id]['is_online'] = is_online

    if not new_public_key and not is_online: return False
    
    with open(path_db_users, 'w') as file:
        json.dump(users, file, indent=2)

    return True

def get_public_key_by_id(id:str) -> str:
    user = get_user_by_id(id)
    
    if "public_key" in user:
        public_key = user["public_key"]
        return public_key
        
    return ''

def get_is_online_by_id(id:str) -> bool:
    user = get_user_by_id(id)
    
    if "is_online" in user:
        is_online = user["is_online"]
        return is_online
        


def get_user_by_id(id:str) -> dict:
    users = get_users()
    if id in users:
        return users[id]
    
    return {}   
if __name__ == "__main__":
    users = get_users()
    print(users)
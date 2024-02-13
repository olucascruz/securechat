import json
import os

folder_path = os.getcwd() 
path_db_token = os.path.join(folder_path, r"db\auth.json")


def get_auth():
    with open(path_db_token, 'r') as file:
        db = json.load(file)    
    return db


def get_auth_by_username(username):
    try:
        authentication= get_auth()[username]
        return authentication
    except Exception as ex:
        print(ex)
        return False


def update_auth(username, id, new_token):
    obj_auth = {"token":new_token, "id":id}
    db = get_auth()
    db[username] = obj_auth

    with open(path_db_token, 'w') as file:
        json.dump(db, file, indent=2) 

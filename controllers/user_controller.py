from repositories import update_user, auth_user, insert_user, get_auth, update_auth, get_auth_by_username, get_users_without_password, get_public_key_by_id, get_is_online_by_id
from utils import generate_unique_id
from .validations.validations import login_validate, register_validate
from flask import jsonify

def error(message):
    return jsonify({'error': message}), 400


def auth_login(data_login):
    is_valid = login_validate(data_login)
    if not is_valid: return error('data not is valid')

    username, password, public_key = data_login.values()

    if len(public_key) != 130: 
        print('error length public key')
        return error('error length public key')

    new_token = generate_unique_id()
    auth = {}
    try:    
        user_id = auth_user(username, password) 
        if not user_id: return error('invalid credentials')
    
        update_auth(username=username, 
                    id=user_id, 
                    new_token=new_token)
        
        update_user(id=user_id,
                    new_public_key=public_key, 
                    is_online=True)
        
        auth = get_auth_by_username(username)
    except Exception as ex:
        return error('invalid credentials')
        
    if not auth: return error('invalid credentials')
    
    return jsonify(auth), 200


def register_controller(data_register):
    is_valid = register_validate(data_register)
    
    if not is_valid: return error('data not is valid')
    username, password = data_register.values()
    try:
        inserted_user = insert_user(username, password)
        if not inserted_user: return error('User already exists')
        return jsonify({'insert_user':'successful'}), 200
    except Exception as ex:
        return error("cannot insert user")


def logout_controller(data_request:dict):
    id = data_request["id"]
    try:
        update_user(id, new_public_key="", is_online=False)
        return jsonify({'logout':'successful'}), 200
    except Exception as ex:
        print("logouttt", ex)
        return error("error logout")


def get_users_controller()->list:
    try:
        return get_users_without_password()
    except Exception as ex:
        return error("not is possible get users")


def get_public_key_controller(user_id:str):
    try:
        public_key = get_public_key_by_id(user_id)
        if not public_key: return error("not found public key")
        return jsonify({"public_key":public_key}), 200
    except Exception as ex:
        return error("not is possible get public key")


def get_is_online_controller(user_id:str):
    try:
        is_online = get_is_online_by_id(user_id)
        return jsonify({"is_online":is_online}), 200
    except Exception as ex:
        return error("not is possible get is_online")
    
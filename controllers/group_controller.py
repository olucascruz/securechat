from flask import jsonify
from repositories import get_groups_with_user_include, insert_group
from .validations.validations import create_group_validate
def error(message):
    return jsonify({'error': message}), 400

def get_groups_with_user_included_controller(user_id:str)->list:
    try:
        groups = get_groups_with_user_include(user_id)
        print("listGroup",groups)
        return groups
    except Exception as ex:
        print(ex)
        return []
    
def create_group_controller(data_request):
    try:
        is_valid = create_group_validate(data_request)
        if not is_valid: return error("data not is valid")
        name, members = data_request.values()
        insert_group(name, members)
        return jsonify({"create group":"successful"})
    except Exception as ex:
        return error("data error to create group")
def check_fields(fields_expected:list, 
                 request_data:dict)->bool:
    for field in fields_expected:
        if field not in request_data:
            return False 
    return True

def login_validate(request_data_login):
    fields_expected = ["username", "password", "public_key", "auth_key"]
    has_expected_fields = check_fields(fields_expected, request_data_login)
    if not has_expected_fields: return False
    return True

def register_validate(request_data_register):
    fields_expected = ["username", "password"]
    has_expected_fields = check_fields(fields_expected, request_data_register)
    if not has_expected_fields: return False
    return True

def create_group_validate(request_data_create_group):
    fields_expected = ["name", "members_id"]
    has_expected_fields = check_fields(fields_expected, request_data_create_group)
    if not has_expected_fields: return False
    return True
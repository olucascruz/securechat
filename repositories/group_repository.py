import os
import json
from utils import generate_unique_id

folder_path = os.getcwd() 
path_db_group = os.path.join(folder_path, r"db\groups.json")

def get_groups():
    with open(path_db_group, 'r') as file:
        db = json.load(file)    
    return db


def get_groups_with_user_include(user_id):
    groups = get_groups()

    groups_includes_user = []
    for group_id in groups:
        if user_id in groups[group_id]["members_id"]:
            data_group = {
                "name":groups[group_id]["name"],
                "id":group_id,
                "members":groups[group_id]["members_id"],
            }
            groups_includes_user.append(data_group)    
    return groups_includes_user


def insert_group(name, members):
    groups = get_groups()
    id = generate_unique_id(groups)
    groups[id] = {"name":name, "members_id":members}
    with open(path_db_group, 'w') as file:
        json.dump(groups, file, indent=2)

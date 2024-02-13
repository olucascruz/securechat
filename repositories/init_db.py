import os
import json

def init_db():
    folder_path = os.getcwd() 
    path_db = os.path.join(folder_path, r"db")

    db_exists = os.path.exists(path_db)

    if not db_exists:
        os.makedirs(path_db)
        with open(os.path.join(path_db, r"users.json"), 'w') as users_file,\
            open(os.path.join(path_db, r"auth.json"), 'w') as auth_file, \
            open(os.path.join(path_db, r"groups.json"), 'w') as groups_file:
                    json.dump({}, users_file, indent=4)
                    json.dump({}, auth_file, indent=4)
                    json.dump({}, groups_file, indent=4)
                
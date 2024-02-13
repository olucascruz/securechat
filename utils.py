import uuid

def generate_unique_id(existing_ids=None):
    # cria uma chave única, caso a chave já exista na lista passada  
    new_id = str(uuid.uuid4())
    if not existing_ids: return new_id
    while True:
        new_id = str(uuid.uuid4())
        if new_id not in existing_ids:
            return new_id
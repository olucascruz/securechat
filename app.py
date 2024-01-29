from flask import Flask, jsonify, request, Response
from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask_cors import CORS
import json
import time
import threading
import os
import uuid

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:5173"])
watch_thread = None

clients = 0
folder_path = os.path.dirname(__file__)
path_db = os.path.join(folder_path, r"db\db.json")
path_db_token = os.path.join(folder_path, r"db\auth.json")

def watch_json_changes():
    global clients
    while clients > 0:
        time.sleep(1)
        try:
            mtime = os.path.getmtime(path_db)
            if 'last_mtime' not in watch_json_changes.__dict__ or mtime > watch_json_changes.last_mtime:
                print('Arquivo JSON alterado. Notificando clientes.')
                with open(path_db, "r") as file:
                    db = json.load(file)
                    socketio.emit('jsonChanged', db, namespace='/')
                watch_json_changes.last_mtime = mtime
        except FileNotFoundError:
            pass

@socketio.on('connect')
def handle_connect():

    print('Cliente conectado')
    global watch_thread
    global clients

    clients += 1
    if watch_thread is None or not watch_thread.is_alive():
        print('Iniciando thread de observação...')
        watch_thread = threading.Thread(target=watch_json_changes, daemon=True)
        watch_thread.start()

@socketio.on('disconnect')
def handle_disconnect():
    global clients
    clients -= 1
    print('Cliente desconectado')


@app.route("/login", methods=['POST'])
def login():
    data_request = request.json

    # Create new pair keys log
    print("\n" + "---" * 10 + "LOG : Server is receiving the public key because the user logged into their account" + "---" * 10)
    print("\nUsername: ", data_request["username"])
    print("\nPublic Key Serializaded:\n\n", data_request["public_key"])
    print("---" * 70 + "\n\n")

    with open(path_db, 'r') as file:
        db = json.load(file)

    with open(path_db_token, 'r') as file:
        db_token = json.load(file)
    
    for id in db:
        user_is_in_db = (db[id]["username"] == data_request["username"] and
                     db[id]["password"] == data_request["password"])
        
        if user_is_in_db:
            token = generate_unique_id(db.keys())
            obj_auth = {"token":token, "id":id}
            db_token[db[id]["username"]] = obj_auth
            with open(path_db_token, 'w') as file:
                json.dump(db_token, file, indent=2)

            db[id]["is_online"] = True
            db[id]["public_key"] = data_request["public_key"]
            with open(path_db, 'w') as file:
                json.dump(db, file, indent=2)
            print(db_token[db[id]["username"]])
            return jsonify(db_token[db[id]["username"]])
    return Response(
            "Error:not exist",
            status=400)


@app.route("/register", methods=['POST'])
def register():

    """
    Função que registra usuário no banco de dados do servidor.

    expected format:{
    username:username, password:password, public_key:public_key
    }"""

    # Retira o json da requisição, já o lendo como dict
    data_request = request.json

    print("\n" + "---" * 15 + "LOG : Server is receiving the public key because user create a new account" + "---" * 15)
    print("\nUsername: ", data_request["username"])
    print("\nNew Public Key Serializaded:\n\n", data_request["public_key"])
    print("---" * 40 + "\n\n")

    data_expected = ["username", "password"]

    """ Verifica se foi enviado os campos necessários"""
    for fields in data_expected:
        if fields not in data_request.keys():
            return Response(
            "Error: incorrect format",
            status=400)
    
    """ Verifica se os campos estão vazios"""
    for key in data_request.keys():
        if data_request[key] == "": 
            return Response(
            "Error: empty value",
            status=400,)
        
    obj_db ={
        "username":data_request["username"],
        "password":data_request["password"],
        "is_online":False,
        "public_key":data_request["public_key"]
    }
    

    ###Abre o arquivo onde fica registrado os usuários###
    with open(path_db, 'r') as file:
        db = json.load(file)
    
    ###Verifica se o usuário já existe no banco###
    for db_data in db:
        if db[db_data]["username"] == data_request["username"]:
           return Response(
            "Error: usúario já existe",
            status=400,)
        
    # Cria a chave única para cada usuário
    user_id = generate_unique_id(db.keys())

    # Aqui ele cria o usuário com o id novo no objeto da leitura do arquivo do banco 
    db[user_id] = obj_db

    # Aqui é onde é feito o save no banco 
    with open(path_db, 'w') as file:
        json.dump(db, file, indent=2)

    return jsonify({})


def generate_unique_id(existing_ids):
    # cria uma chave única, caso a chave já exista na lista
    # passada
    while True:
        new_id = str(uuid.uuid4())
        if new_id not in existing_ids:
            return new_id


@app.route("/logout", methods=['POST'])
def logout():
    data_request = request.json
    with open(path_db, 'r') as file:
        db = json.load(file)

    for id in db:
        if id == data_request["id"]:
            db[id]["is_online"] = False
            with open(path_db, 'w') as file:
                json.dump(db, file, indent=2)
            return jsonify({"msg":"logout"})

@app.route("/users")      
def getUsers():
    with open(path_db, 'r') as file:
        db = json.load(file)
    return db


@socketio.on('message')
def handle_message(data_request):
    receiver = data_request["receiver"]
    print(data_request)
    emit(f"message-{receiver}", data_request, broadcast=True)
    # emit(f"teste", data_request, broadcast=True)

@socketio.on('message_test')
def handle_message(data_request):
    print(data_request)
    emit(f"teste", data_request, broadcast=True)


if __name__ == "__main__":
    socketio.run(app,  debug=True)


@app.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "POST":
        print(request.json)
        return jsonify({"test":0})
    print("test")
    return jsonify({"test":0})

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
obj_db ={
    "username":"",
    "password":"",
    "is_online":False,
    "public_key":""
}

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
    data = request.json
    with open(path_db, 'r') as file:
        db = json.load(file)

    with open(path_db_token, 'r') as file:
        db_token = json.load(file)
    
    for id in db:
        user_is_in_db = (db[id]["username"] == data["username"] and
                     db[id]["password"] == data["password"])
        
        if user_is_in_db:
            token = generate_unique_id(db.keys())
            obj_auth = {"token":token, "id":id}
            db_token[db[id]["username"]] = obj_auth
            with open(path_db_token, 'w') as file:
                json.dump(db_token, file, indent=2)

            db[id]["is_online"] = True
            db[id]["public_key"] = data["public_key"]
            with open(path_db, 'w') as file:
                json.dump(db, file, indent=2)
            print(db_token[db[id]["username"]])
            return jsonify(db_token[db[id]["username"]])
    return Response(
            "Error:not exist",
            status=400)

@app.route("/register", methods=['POST'])
def register():
    """expected format:{
    username:username, password:password, public_key:public_key
    }"""
    data = request.json
    print(data)

    data_expected = ["username", "password"]

    for de in data_expected:
        if de not in data.keys():
            return Response(
            "Error: incorrect format",
            status=400)
    
    for key in data.keys():
        if data[key] == "": 
            return Response(
            "Error: empty value",
            status=400,)
    
    obj_db["is_online"] = True
    obj_db["username"] = data["username"]
    obj_db["password"] = data["password"]
    obj_db["public_key"] = data["public_key"]


    with open(path_db, 'r') as file:
        db = json.load(file)

    user_id = generate_unique_id(db.keys()) 
    db[user_id] = obj_db

    with open(path_db, 'w') as file:
        json.dump(db, file, indent=2)

    return jsonify({})


def generate_unique_id(existing_ids):
    while True:
        new_id = str(uuid.uuid4())
        if new_id not in existing_ids:
            return new_id
        
@app.route("/logout", methods=['POST'])
def logout():
    data = request.json
    with open(path_db, 'r') as file:
        db = json.load(file)

    for id in db:
        if id == data["id"]:
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
def handle_message(data):
    receiver = data["receiver"]
    print(data)
    emit(f"message-{receiver}", data, broadcast=True)

if __name__ == "__main__":
    socketio.run(app,  debug=True)


@app.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "POST":
        print(request.json)
        return jsonify({"test":0})
    print("test")
    return jsonify({"test":0})

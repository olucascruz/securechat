from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask_cors import CORS
import json
import time
import threading
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:5173"])
watch_thread = None

obj_db ={ 
    "is_online":False,
    "public_key":""
}

clients = 0
folder_path = os.path.dirname(__file__)
path_db = os.path.join(folder_path, r"db\db.json")

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

@app.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "POST":
        print(request.json)
        return jsonify({"test":0})
    print("test")
    return jsonify({"test":0})
@app.route("/register", methods=['POST'])

def register():
    data = request.json
    print("register debug",data)
    obj_db["is_online"] = True
    obj_db["public_key"] = data["public_key"]
    with open(path_db, 'r') as file:
        db = json.load(file)

    for username in db:
        if username == data["username"]:
            db[username]["is_online"] = True
            db[username]["public_key"] = data["public_key"]
            with open(path_db, 'w') as file:
                json.dump(db, file, indent=2)
            return jsonify({"msg":"user já existe"})

    db[data["username"]]= obj_db

    with open(path_db, 'w') as file:
        json.dump(db, file, indent=2)

    return jsonify({})

@app.route("/logout", methods=['POST'])
def logout():
    data = request.json
    with open(path_db, 'r') as file:
        db = json.load(file)

    for username in db:
        if username == data["username"]:
            db[username]["is_online"] = False
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
    emit(f"message-{receiver}", data, broadcast=True)

if __name__ == "__main__":
    socketio.run(app,  debug=True)
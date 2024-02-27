from flask import Flask, jsonify, request, Response
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from logs import login_log, register_log
from controllers import auth_login, register_controller, get_users_controller, get_public_key_controller, get_is_online_controller, logout_controller, get_groups_with_user_included_controller, create_group_controller


app = Flask(__name__)
CORS(app)
socket_io:SocketIO = SocketIO(app, cors_allowed_origins=["http://localhost:5173"] )
watch_thread = None

clients = 0

@socket_io.on('connect')
def handle_connect():
    print('Cliente conectado')
    global clients

    clients += 1

@socket_io.on('disconnect')
def handle_disconnect():
    global clients
    clients -= 1
    print('Cliente desconectado')


@app.route("/register", methods=['POST'])
def register():

    """
    Função que registra usuário no banco de dados.

    expected format:{
        username:username,
        password:password
    }"""

    # Retira o json da requisição, já o lendo como dict
    data_request = request.json

    response = register_controller(data_request)
    register_log(data_request)
    return response


@app.route("/login", methods=['POST'])
def login():
    data_request = request.json
  
    auth = auth_login(data_request)
    if auth:
        login_log(data_request)
        socket_io.emit("new_user_connected", "update")
    
    return auth
        
    
@app.route("/logout", methods=['POST'])
def logout():
    data_request = request.json
    response = logout_controller(data_request)
    socket_io.emit("new_user_connected", "update")
    return response


@app.route("/users")      
def get_users():
    data = get_users_controller()
    return data
    

@app.route("/getPublicKey") 
def get_public_key():
    user_id = request.args.get('user_id')
    response = get_public_key_controller(user_id)
    return response


@app.route("/getIsOnline") 
def get_is_online():
    user_id = request.args.get('user_id')
    response = get_is_online_controller(user_id)
    return response


@app.route("/create_group", methods=['POST'])
def create_group():
    data_request = request.json
    response = create_group_controller(data_request)
    return response


@app.route("/get_group", methods=['POST'])
def get_groups():
    data_request = request.json
    # Verifica se "id" está presente em data_request
    user_id = data_request.get("id")
    list_groups = get_groups_with_user_included_controller(user_id)
    return list_groups


@socket_io.on('message')
def handle_message(data_request):
    print("message event - ",data_request)
    try:
        receiver = data_request["receiver"]
        print("data_request", data_request)
        emit(f"message-{receiver}", data_request, broadcast=True)
    except Exception as er: print(er)


@socket_io.on('message-group')
def handle_message(data_request):
    print("message group event - ",data_request)
    try:
        group_id = data_request["groupId"]
        receiver = data_request["receiver"]
        emit(f"message-group-{group_id}-{receiver}", data_request, broadcast=True)
    except Exception as ex: print(ex)


if __name__ == "__main__":
    socket_io.run(app,  debug=True)
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask import request
from .utils.logger import logger
from .extensions import socketio


active_users = {}  # Armazena usuários conectados
focused_users = {}  # Armazena usuários em foco

@socketio.on("connect")
def handle_connect():
    user_id = request.args.get("user_id")
    username = request.args.get("username")

    # emit("user_connected", {"user_id": user_id}, broadcast=True)
    logger.info(f"Usuário {username} ({user_id}) conectado ao websocket.")


# @socketio.on("disconnect")
# def handle_disconnect():
#     """ Remove um usuário ativo ao desconectar. """
#     user_id = None

#     # Encontrar o usuário desconectado (porque request.args pode não estar disponível)
#     for uid, session in active_users.items():
#         if request.sid == session:  # Verifica o ID da sessão
#             user_id = uid
#             break

#     if user_id:
#         del active_users[user_id]
#         emit("user_disconnected", {"user_id": user_id}, broadcast=True)
#         print(f"Usuário {user_id} desconectado.")


@socketio.on("enter_focus")
def enter_focus(data):
    user_id = data.get("user_id")
    username = data.get("username")

    task_name = data.get("task_name")
    start_time = data.get("start_time")

    if user_id:
        # join_room("focus_session")
        focused_users[user_id] = {"start_time": start_time, "username": username, "task_name": task_name }
        emit("focus_user_joined", { user_id: {"start_time": start_time, "username": username, "task_name": task_name } }, broadcast=True)

@socketio.on("leave_focus")
def leave_focus(data):
    user_id = data.get("user_id")

    if user_id in focused_users:
        #leave_room("focus_session")
        del focused_users[user_id]
        emit("focus_user_left", {"user_id": user_id}, broadcast=True)

@socketio.on("get_focus_users")
def get_focus_users():
    emit("update_focus_users", {"focused_users": focused_users}, broadcast=True)
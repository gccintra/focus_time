from flask import Blueprint, request
from app.controllers.todo_controller import ToDoController

# Cria o Blueprint específico para ToDo
todo_bp = Blueprint("todo", __name__, url_prefix="/todo")
todo_controller = ToDoController()

@todo_bp.route("/new_todo", methods=["POST"])
def new_todo_route():
    """Cria um novo ToDo para uma tarefa específica."""
    data = request.get_json()
    return todo_controller.create_task_to_do(data)

@todo_bp.route("/change_state/<todo_id>", methods=["PUT"])
def change_to_do_state_route(todo_id):
    """Altera o estado de um ToDo específico."""
    data = request.get_json()
    return todo_controller.change_to_do_state(data, todo_id)

@todo_bp.route("/delete/<todo_id>", methods=["DELETE"])
def delete_todo_route(todo_id):
    """Deleta um ToDo específico."""
    return todo_controller.delete_to_do(todo_id)

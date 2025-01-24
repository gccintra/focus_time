from flask import Blueprint, request
from app.controllers.task_controller import TaskController


task_bp = Blueprint("task", __name__, url_prefix="/tasks")
controller = TaskController()


@task_bp.route("/", methods=["GET"])
def tasks_route():
    return controller.my_tasks()

@task_bp.route("/get_data_for_chart_my_tasks_menu/<task_id>", methods=["GET"])
def task_data_for_my_tasks_chart(task_id):
    return controller.get_data_for_chart(task_id)

@task_bp.route("/new_task", methods=["POST"])
def new_task_route():
    data = request.get_json()
    return controller.new_task(data)

@task_bp.route("/<task_id>", methods=["GET"])
def start_task_route(task_id):
    return controller.start_task(task_id)

@task_bp.route("/update_task_time/<task_id>", methods=["POST", "PUT"])
def update_task_time_route(task_id):
    data = request.get_json()
    return controller.update_task_time(task_id, data)

@task_bp.route("/<task_id>/new_task_to_do", methods=["POST"])
def new_task_to_do_route(task_id):
    data = request.get_json()
    return controller.create_task_to_do(task_id, data)

@task_bp.route("/<task_id>/change_to_do_state", methods=["PUT"])
def change_to_do_state_route(task_id):
    data = request.get_json()
    return controller.change_to_do_state(task_id, data)

@task_bp.route("/<task_id>/delete_to_do", methods=["DELETE"])
def delete_to_do(task_id):
    data = request.get_json()
    return controller.delete_to_do(task_id, data)



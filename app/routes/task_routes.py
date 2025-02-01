from flask import Blueprint, request
from app.controllers.task_controller import TaskController


task_bp = Blueprint("task", __name__, url_prefix="/task")
task_controller = TaskController()

@task_bp.route("/", methods=["GET"])
def tasks_route():
    return task_controller.my_tasks()

@task_bp.route("/get_data_for_all_doughnut_home_charts", methods=["GET"])
def get_data_for_all_charts_menu_route():
    return task_controller.get_data_for_all_charts()

@task_bp.route("/new_task", methods=["POST"])
def new_task_route():
    data = request.get_json()
    return task_controller.new_task(data)

@task_bp.route("/<task_id>", methods=["GET"])
def start_task_route(task_id):
    return task_controller.start_task(task_id)

@task_bp.route("/update_task_time/<task_id>", methods=["POST", "PUT"])
def update_task_time_route(task_id):
    data = request.get_json()
    return task_controller.update_task_time(task_id, data)

@task_bp.route("/get_data_for_last_365_days_home_chart", methods=["GET"])
def get_data_for_last_365_days_home_chart_route():
    return task_controller.get_data_for_last_365_days_home_chart()




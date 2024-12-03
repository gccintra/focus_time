from flask import Blueprint, request, redirect, url_for, render_template, jsonify
from app.models.task import Task
from .data_record import DataRecord
from ..models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/tasks")
db = DataRecord("user.json")


@task_bp.route("/", methods=["GET"])
def my_tasks():
    tasks_data = db.get_models()
    tasks = []

    for task_data in tasks_data:
        task_data = Task(
            identificator=task_data.get('identificator'),
            title=task_data.get('title'),
            color=task_data.get('color'), 
            minutes_in_focus_per_day=task_data.get("minutes_in_focus_per_day")
        )
        tasks.append(task_data)

        
    return render_template("my_tasks.html", title="My Tasks", active_page="home", tasks=tasks)

@task_bp.route("/new_task", methods=["POST"])
def new_task():
    data = request.get_json()  # Obtém os dados do corpo da requisição (nome e cor)
    task_name = data.get('name')
    task_color = data.get('color')

    identificator = db.generate_unique_id()
    new_task = Task(identificator=identificator, title=task_name, color=task_color)
 
    db.write(new_task)

    # Retorna os dados da tarefa criada para o frontend
    return jsonify({
        'id': new_task.identificator,
        'name': new_task.title, 
        'color': new_task.color,
        'today_total_time': new_task.today_total_time,
        'week_total_time': new_task.week_total_time
    })

@task_bp.route("/<task_id>", methods=["GET"])
def start_task(task_id):
    tasks_data = db.get_models()
    
    for task_data in tasks_data:
        if task_id == task_data.get('identificator'):
            principal_task = Task(
            identificator=task_data.get('identificator'),
            title=task_data.get('title'),
            color=task_data.get('color'), 
            minutes_in_focus_per_day=task_data.get("minutes_in_focus_per_day")
            )
    
    return render_template("start_task.html", title="Start Task", task=principal_task)


@task_bp.route("/update_task_time/<task_id>", methods=["POST"])
def update_task_time(task_id):
    tasks_data = db.get_models()
    data = request.get_json()
    minutes = int(data.get("elapsed_minutes"))

    for task_data in tasks_data:
        if task_id == task_data.get('identificator'):
            task = Task(
            identificator=task_data.get('identificator'),
            title=task_data.get('title'),
            color=task_data.get('color'), 
            minutes_in_focus_per_day=task_data.get("minutes_in_focus_per_day")
            )
            break

    task.set_minutes_in_focus_per_day(minutes)
    db.save()
    return jsonify({
        'minutes': task.today_total_minutes,
    })


@task_bp.route("/get_data_for_chart", methods=["GET"])
def task_data():
    tasks_data = db.get_models()
    tasks_for_chart = []

    for task_data in tasks_data:
        task = Task(
            identificator=task_data.get('identificator'),
            title=task_data.get('title'),
            color=task_data.get('color'), 
            minutes_in_focus_per_day=task_data.get("minutes_in_focus_per_day")
        )
        if task.today_total_minutes != 0:
            tasks_for_chart.append({
                "identificator": task.identificator,
                "title": task.title,
                "color": task.color,
                "minutes": task.today_total_minutes
            })

    # Só enviar as tasks se tiver today_total_minutes
    create_chart = len(tasks_for_chart) > 0
    return jsonify({"tasks": tasks_for_chart, "createChart": create_chart})
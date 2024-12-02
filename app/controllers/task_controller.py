from flask import Blueprint, request, redirect, url_for, render_template, jsonify
from app.models.task import Task
from .data_record import DataRecord
from ..models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/tasks")
db = DataRecord("user.json")


# ver como atualizar os dados, chamar esse metodo, sempre que o usuario dar f5, atualmente so funciona se fechar e abrir o servidor.

@task_bp.route("/", methods=["GET"])
def my_tasks():
    tasks_data = db.get_models()
    tasks = []

    for task_data in tasks_data:
        task_data = Task(
            identificator=task_data.get('identificator'),
            title=task_data.get('title'),
            color=task_data.get('color'), 
            time_in_focus_per_day=task_data.get("time_in_focus_per_day")
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
        'name': new_task.title,
        'color': task_color,
        'today_total_time': new_task.today_total_time,
        'week_total_time': new_task.week_total_time
    })

@task_bp.route("/start_task/<task_id>", methods=["GET", "POST"])
def start_task(task_id):
    tasks_data = db.get_models()

    for task_data in tasks_data:
        if task_id == task_data.get('identificator'):
            task = Task(
            identificator=task_data.get('identificator'),
            title=task_data.get('title'),
            color=task_data.get('color'), 
            time_in_focus_per_day=task_data.get("time_in_focus_per_day")
            )
            break
       

    return render_template("start_task.html", title="Start Task", task=task)




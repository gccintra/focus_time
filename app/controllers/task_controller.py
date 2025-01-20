from flask import Blueprint, request, redirect, url_for, render_template, jsonify
from app.models.task import Task
from .task_record import TaskRecord
from ..models.task import Task
from app.models.task_to_do_list import TaskToDoList
from datetime import datetime

task_bp = Blueprint("task", __name__, url_prefix="/tasks")
db = TaskRecord("user.json")


@task_bp.route("/", methods=["GET"])
def my_tasks():
    tasks_data = db.get_models()
    tasks = []

    for task_data in tasks_data:
        task_data = Task(
            identificator=task_data.get('identificator'),
            title=task_data.get('title'),
            color=task_data.get('color'), 
            seconds_in_focus_per_day=task_data.get("seconds_in_focus_per_day"),
            task_to_do_list = task_data.get("task_to_do_list")
            )
        tasks.append(task_data)

        
    return render_template("my_tasks.html", title="My Tasks", active_page="home", tasks=tasks)

@task_bp.route("/new_task", methods=["POST"])
def new_task():
    data = request.get_json()  
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
    task = get_task_instance_by_id(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Altera a formatação da data/hora para visualização
    # Talvez seja legal eu mudar as  "to_do_created_time_formatted"/"to_do_completed_time_formatted" 
    # e "to_do_created_time_iso"/"to_do_completed_time_iso"
    for to_do_item in task.task_to_do_list:
        created_time_iso = to_do_item.to_do_created_time
        to_do_item.to_do_created_time = datetime.fromisoformat(created_time_iso).strftime("%m-%d-%Y %H:%M")

        if to_do_item.to_do_completed_time:
            completed_time_iso = to_do_item.to_do_completed_time
            to_do_item.to_do_completed_time = datetime.fromisoformat(completed_time_iso).strftime("%m-%d-%Y %H:%M")

    return render_template("start_task.html", title="Start Task", task=task, to_do_list=task.task_to_do_list)


@task_bp.route("/update_task_time/<task_id>", methods=["POST", "PUT"])
def update_task_time(task_id):
    data = request.get_json()
    seconds = int(data.get("elapsed_seconds"))

    
    task = get_task_instance_by_id(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    task.set_seconds_in_focus_per_day(seconds)
    db.save_seconds_in_focus_per_day_in_db(task)
    return jsonify({
        'message': "success! the seconds has been saved."
    }), 200

@task_bp.route("/get_data_for_chart_my_tasks_menu/<task_id>", methods=["GET"])
def task_data_for_my_tasks_chart(task_id):
    tasks_data = db.get_models()
    tasks_for_chart = []

    for task_data in tasks_data:
        task = Task(
            identificator=task_data.get('identificator'),
            title=task_data.get('title'),
            color=task_data.get('color'), 
            seconds_in_focus_per_day=task_data.get("seconds_in_focus_per_day"),
            task_to_do_list = task_data.get("task_to_do_list")
            )
        task_color = task.color if task.identificator == task_id else '#474747'
        tasks_for_chart.append({
            "identificator": task.identificator,
            "title": task.title,
            "color": task_color,
            "minutes": task.week_total_minutes
        })
       
    # Só enviar as tasks se tiver today_total_minutes
    create_chart = len(tasks_for_chart) > 0
    return jsonify({"tasks": tasks_for_chart, "createChart": create_chart})



@task_bp.route("/<task_id>/new_task_to_do", methods=["POST"])
def new_task_to_do(task_id):
    data = request.get_json()  
    to_do_name = data.get('name')

    new_task_to_do = TaskToDoList(title=to_do_name)
    if not db.create_to_do(task_id, new_task_to_do):
            return jsonify({'error': 'Task not found or could not add to-do'}), 404
    

    formatted_created_time = datetime.fromisoformat(new_task_to_do.to_do_created_time).strftime("%m-%d-%Y %H:%M")
    
    return jsonify({
        'to_do_identificator': new_task_to_do.to_do_identificator,
        'to_do_title': new_task_to_do.to_do_title, 
        'to_do_created_time': formatted_created_time,
        'to_do_status': new_task_to_do.to_do_status,
        'to_do_completed_time': new_task_to_do.to_do_completed_time
    })


@task_bp.route("/<task_id>/change_to_do_state", methods=["PUT"])
def change_to_do_state(task_id):
    data = request.get_json()  
    to_do_id = data.get('id')
    new_status = data.get('status')

    task = get_task_instance_by_id(task_id)
    if not task:
        return jsonify({"success": False, "error": "Task not found"}), 404


    for to_do in task.task_to_do_list:
        if to_do.to_do_identificator == to_do_id:
            to_do.to_do_status = new_status
            to_do.to_do_completed_time = datetime.now().isoformat() if new_status == 'completed' else None
            
            if not db.update_to_do(task.identificator, to_do):
                return jsonify({"success": False}), 503
            
            formatted_created_time = datetime.fromisoformat(to_do.to_do_created_time).strftime("%m-%d-%Y %H:%M") 

            if to_do.to_do_completed_time:
                formatted_completed_time = datetime.fromisoformat(to_do.to_do_completed_time).strftime("%m-%d-%Y %H:%M") 
                
                return jsonify({"success": True, "status": new_status, "completed_time": formatted_completed_time, "created_time": formatted_created_time}), 200
                        
            return jsonify({"success": True, "status": new_status, "created_time": formatted_created_time}), 200
        
    return jsonify({"success": False, "error": "To-Do not found"}), 404



@task_bp.route("/<task_id>/delete_to_do", methods=["DELETE"])
def delete_to_do(task_id):
    data = request.get_json()
    to_do_id = data.get('id')

    task = get_task_instance_by_id(task_id)
    if not task:
        return jsonify({"success": False, "error": "Task not found"}), 404


    for to_do in task.task_to_do_list:
        if to_do.to_do_identificator == to_do_id:
            task.task_to_do_list.remove(to_do)
            db.save_task_to_do_list_in_db(task)
            return jsonify({"success": True}), 200

    return jsonify({"success": False, "error": "To-Do not found"}), 404



# Utils:
    
def get_task_instance_by_id(task_id):
    tasks_data = db.get_models()

    for record in tasks_data:
        if task_id == record.get('identificator'):
            return Task(
                identificator=record.get('identificator'),
                title=record.get('title'),
                color=record.get('color'),
                seconds_in_focus_per_day=record.get("seconds_in_focus_per_day"),
                task_to_do_list=record.get("task_to_do_list"),
            )
    return None  # Retorna None se a tarefa não for encontrada

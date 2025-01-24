from flask import jsonify, render_template, abort
from app.services.task_service import TaskService

class TaskController:
    def __init__(self):
        self.service = TaskService()

    def my_tasks(self):
        tasks = self.service.get_all_tasks()
        return render_template("my_tasks.html", title="My Tasks", active_page="home", tasks=tasks)
    
    def get_data_for_chart(self, task_id):
        tasks_for_chart, create_chart = self.service.get_data_for_chart(task_id)
        return jsonify({"tasks": tasks_for_chart, "createChart": create_chart})

    def new_task(self, data):
        task_name = data.get('name')
        task_color = data.get('color')
        task = self.service.create_new_task(task_name, task_color)
        return jsonify({
            'id': task.identificator,
            'name': task.title,
            'color': task.color,
            'today_total_time': task.today_total_time,
            'week_total_time': task.week_total_time
        })

    def start_task(self, task_id):
        task = self.service.get_task_by_id(task_id)
        if not task:
            return abort(404)
        return render_template("start_task.html", title="Start Task", task=task, to_do_list=task.task_to_do_list)

    def update_task_time(self, task_id, data):
        elapsed_seconds = int(data.get("elapsed_seconds"))
        task = self.service.update_task_time(task_id, elapsed_seconds)
        if not task:
            return jsonify({"error": "Task not found"}), 404
        return jsonify({'message': "success! the seconds have been saved."}), 200

    def create_task_to_do(self, task_id, data):
        to_do_name = data.get('name')
        new_to_do = self.service.create_task_to_do(task_id, to_do_name)
        if not new_to_do:
            return jsonify({'error': 'Task not found or could not add to-do'}), 404

        return jsonify({
            'to_do_identificator': new_to_do.to_do_identificator,
            'to_do_title': new_to_do.to_do_title,
            'to_do_created_time': new_to_do.to_do_created_time_formatted,
            'to_do_status': new_to_do.to_do_status,
        })

    def change_to_do_state(self, task_id, data):
        to_do_id = data.get('id')
        new_status = data.get('status')

        updated_to_do = self.service.change_to_do_state(task_id, to_do_id, new_status)
        if not updated_to_do:
            return jsonify({"success": False, "error": "Task or To-Do not found"}), 404

        return jsonify({
            "success": True,
            "status": updated_to_do.to_do_status,
            "created_time": updated_to_do.to_do_created_time_formatted,
            "completed_time": getattr(updated_to_do, "to_do_completed_time_formatted", None)
        }), 200
    

    # Melhorar Tratativa de erros, esses return de True, False, None ta zuado
    def delete_to_do(self, task_id, data):
        to_do_id = data.get('id')
        if not self.service.delete_to_do(task_id, to_do_id):
            return jsonify({"success": False, "error": "Task or To-Do not found"}), 404


        return jsonify({"success": True}), 200

    
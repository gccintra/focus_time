from flask import jsonify, render_template, abort
from app.services.task_service import TaskService
from ..models.exceptions import DatabaseError, TaskNotFoundError, TaskTodoNotFoundError, TaskValidationError
from ..utils.logger import logger

class TaskController:
    def __init__(self):
        try:
            self.service = TaskService()
        except DatabaseError as e:
            raise DatabaseError(f"Failed to initialize TaskService: {str(e)}")

    def my_tasks(self):
        tasks = self.service.get_all_tasks()
        return render_template("my_tasks.html", title="My Tasks", active_page="home", tasks=tasks)

    def get_data_for_all_charts(self):
        tasks_for_chart = self.service.get_data_for_all_charts()
        return jsonify({"success": True, "data": {"tasks": tasks_for_chart}, "error": None})

    def new_task(self, data):
        try:
            task_name = data.get('name')
            task_color = data.get('color')
            task = self.service.create_new_task(task_name, task_color)
            return jsonify({
                "success": True,
                "data": {
                    'id': task.identificator,
                    'name': task.title,
                    'color': task.color,
                    'today_total_time': task.today_total_time,
                    'week_total_time': task.week_total_time
                },
                "error": None
            }), 200
        except (TypeError, Exception):
            return jsonify({"success": False, "data": None, "error": "Internal Server Error"}), 500

    def start_task(self, task_id):
        try:
            task = self.service.get_task_by_id(task_id)
            return render_template("start_task.html", title="Start Task", task=task, to_do_list=task.task_to_do_list)
        except (Exception, TaskNotFoundError) :
            return abort(404)
        except Exception:
            return jsonify({"success": False, "data": None, "error": "Internal Server Error"}), 500

    def update_task_time(self, task_id, data):
        try:
            elapsed_seconds = int(data.get("elapsed_seconds"))
            self.service.update_task_time(task_id, elapsed_seconds)
            return jsonify({"success": True, "data": {"message": "The seconds have been saved."}, "error": None}), 200
        except TaskNotFoundError:
            return jsonify({"success": False, "data": None, "error": "Task not found"}), 404
        except TaskValidationError as e:
            logger.error(f"Erro ao atualizar o tempo de foco diário para a task {task_id}")
            return jsonify({"success": False, "data": None, "error": "Validation Error"}), 400
        except Exception as e:
            logger.error(f"Erro ao atualizar o tempo de foco diário para a task {task_id}: {str(e)}")
            return jsonify({"success": False, "data": None, "error": "Internal Server Error"}), 500

    def create_task_to_do(self, task_id, data):
        try:
            to_do_name = data.get('name')
            new_to_do = self.service.create_task_to_do(task_id, to_do_name)
            return jsonify({
                "success": True,
                "data": {
                    'to_do_identificator': new_to_do.to_do_identificator,
                    'to_do_title': new_to_do.to_do_title,
                    'to_do_created_time': new_to_do.to_do_created_time_formatted,
                    'to_do_status': new_to_do.to_do_status,
                },
                "error": None
            }), 200
        except TaskNotFoundError:
            return jsonify({"success": False, "data": None, "error": "Task not found"}), 404
        except Exception as e:
            logger.error(f"Erro ao criar to-do para a task {task_id}: {str(e)}")
            return jsonify({"success": False, "data": None, "error": "Internal Server Error"}), 500

    def change_to_do_state(self, task_id, data):
        try:
            to_do_id = data.get('id')
            new_status = data.get('status')
            updated_to_do = self.service.change_to_do_state(task_id, to_do_id, new_status)
            return jsonify({
                "success": True,
                "data": {
                    "status": updated_to_do.to_do_status,
                    "created_time": updated_to_do.to_do_created_time_formatted,
                    "completed_time": getattr(updated_to_do, "to_do_completed_time_formatted", None)
                },
                "error": None
            }), 200
        except TaskNotFoundError:
            return jsonify({"success": False, "data": None, "error": "Task not found"}), 404
        except TaskTodoNotFoundError:
            return jsonify({"success": False, "data": None, "error": "To-Do not found"}), 404
        except TaskValidationError as e:
            logger.error(f"Erro ao atualizar o status To-Do {to_do_id}")
            return jsonify({"success": False, "data": None, "error": "Validation Error"}), 400
        except Exception as e:
            logger.error(f"Erro ao atualizar o status do to-do para a task {task_id}: {str(e)}")
            return jsonify({"success": False, "data": None, "error": "Internal Server Error"}), 500
    
    def delete_to_do(self, task_id, data):
        try:
            to_do_id = data.get('id')
            self.service.delete_to_do(task_id, to_do_id)
            return jsonify({"success": True, "data": {"message": "To-Do deleted successfully."}, "error": None}), 200
        except TaskNotFoundError:
            return jsonify({"success": False, "data": None, "error": "Task not found"}), 404        
        except TaskTodoNotFoundError:
            return jsonify({"success": False, "data": None, "error": "To-Do not found"}), 404
        except Exception:
            return jsonify({"success": False, "data": None, "error": "Internal Server Error"}), 500


    
from flask import jsonify, render_template, abort
from app.services.todo_service import ToDoService
from ..models.exceptions import DatabaseError, ToDoValidationError, TodoNotFoundError
from ..utils.logger import logger

class ToDoController:
    def __init__(self):
        try:
            self.service = ToDoService()
        except DatabaseError as e:
            raise DatabaseError(f"Failed to initialize TaskService: {str(e)}")

    def create_task_to_do(self, data):
        try:
            to_do_name = data.get('name')
            task_id = data.get('task_id')
            new_to_do = self.service.create_todo(task_id, to_do_name)
            return jsonify({
                "success": True,
                "message": "To-Do created successfully",
                "data": {
                    "id": new_to_do.to_do_identificator,
                    "title": new_to_do.to_do_title,
                    "created_time": new_to_do.to_do_created_time_formatted,
                    "status": new_to_do.to_do_status
                },
                "error": None
            }), 201
        except Exception as e:
            logger.error(f"Erro ao criar to-do para a task {task_id}: {str(e)}")
            return jsonify({
                "success": False,
                "message": "Something went wrong. Please try again later.",
                "data": None,
                "error": {
                    "code": 500,
                    "type": "InternalServerError",
                    "details": str(e)
                }
            }), 500


    def change_to_do_state(self, data, todo_id):
        try:
            new_status = data.get('status')
            updated_to_do = self.service.change_to_do_state(todo_id, new_status)
            return jsonify({
                "success": True,
                "message": "To-Do status changed successfully",
                "data": {
                    "status": updated_to_do.to_do_status,
                    "created_time": updated_to_do.to_do_created_time_formatted,
                    "completed_time": getattr(updated_to_do, "to_do_completed_time_formatted", None)
                },
                "error": None
            }), 200
        except TodoNotFoundError as e:
           return jsonify({
                "success": False,
                "message": "To-Do not found.",
                "data": None,
                "error": {
                    "code": 404,
                    "type": "TodoNotFoundError",
                    "details": str(e)
                }
            }), 404
        except ToDoValidationError as e:
            logger.error(f"Erro ao atualizar o status To-Do {todo_id}")
            return jsonify({
                "success": False,
                "message": "An error occurred while processing your request. Please check the information provided and try again.",
                "data": None,
                "error": {
                    "code": 400,
                    "type": "ToDoValitantionError",
                    "details": str(e)
                }
            }), 400
        except Exception as e:
            logger.error(f"Erro ao atualizar o status do to-do {todo_id}: {str(e)}")
            return jsonify({
                "success": False,
                "message": "Something went wrong. Please try again later.",
                "data": None,
                "error": {
                    "code": 500,
                    "type": "InternalServerError",
                    "details": str(e)
                }
            }), 500
        

    def delete_to_do(self, todo_id):
        try:
            self.service.delete_to_do(todo_id)
            return jsonify({
                "success": True,
                "message": "To-Do deleted successfully.",
                "data": None,
                "error": None
            }), 200
        except TodoNotFoundError as e:
            return jsonify({
                "success": False,
                "message": "To-Do not found.",
                "data": None,
                "error": {
                    "code": 404,
                    "type": "TodoNotFoundError",
                    "details": str(e)
                }
            }), 404
        except Exception as e:
            return jsonify({
                "success": False,
                "message": "Something went wrong. Please try again later.",
                "data": None,
                "error": {
                    "code": 500,
                    "type": "InternalServerError",
                    "details": str(e)
                }
            }), 500
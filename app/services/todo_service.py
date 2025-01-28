from ..models.todo import ToDo
from ..models.exceptions import ToDoValidationError, TodoNotFoundError
from ..repository.todo_record import ToDoRecord
from datetime import datetime
from ..utils.logger import logger
from ..models.exceptions import DatabaseError

class ToDoService:
    def __init__(self):
        try:
            self.db = ToDoRecord("todo.json")
        except ValueError as e:
            logger.error(f"Erro ao inicializar ToDoRecord: {e}")
            raise DatabaseError("Erro ao inicializar o banco de dados.")

    def create_todo(self, task_id, to_do_name):
        try:
            identificator = self.db.generate_unique_id()
            new_to_do = ToDo(to_do_title=to_do_name, to_do_identificator=identificator, task_FK=task_id)
            self.db.write(new_to_do)
            logger.info(f'To do {to_do_name} para a task {task_id} criado com sucesso!')
            return new_to_do
        except (TypeError, Exception):
            raise

    def get_todo_list(self, task_id):
        try:
            todo_list = []
            todo_data = self.db.get_models()
            for todo in todo_data:
                if todo.task_FK == task_id:
                    todo_list.append(todo)
            logger.info(f'Retornando a lista de todo para a task {task_id} com sucesso!')
            return todo_list
        except Exception as e:
            logger.error(e)
    
    def change_to_do_state(self, todo_id, new_status):
        try:
            todo = self.get_todo_by_id(todo_id)
            todo.to_do_status = new_status
            todo.to_do_completed_time = (
                datetime.now().isoformat() if new_status == "completed" else None
            )
            self.db.save()      
            logger.info(f'Status do To Do com id {todo_id} atualizado para {new_status} com sucesso!')
            return todo
        except ToDoValidationError as e:
            logger.error(e)
            raise
        except TodoNotFoundError as e:
            logger.warning(f'Erro ao atualizar o status to-do: {e}')
            raise         
        except Exception as e:
            logger.error(f'Erro ao atualizar o status to-do: {e}')
            raise

    def delete_to_do(self, to_do_id):
        try:
            todo_list = self.db.get_models()
            for to_do in todo_list:
                if to_do.to_do_identificator == to_do_id:
                    todo_list.remove(to_do)
                    self.db.save()
                    logger.info(f'To-do {to_do.to_do_title} ({to_do.to_do_identificator}) removido com sucesso!')
                    return
            raise TodoNotFoundError(to_do_id)
        except TodoNotFoundError as e:
            logger.warning(f'Erro ao deletar o to-do {to_do_id}: {e}')
            raise         
        except Exception as e:
            logger.error(f'Erro ao deletar o to-do {to_do_id}: {e}')
            raise

    def get_todo_by_id(self, todo_id):
        try:
            return self.db.get_todo_by_id(todo_id)
        except (TodoNotFoundError, Exception):
            raise

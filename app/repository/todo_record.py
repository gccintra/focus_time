from .data_record import DataRecord
from ..models.task import Task
from ..models.exceptions import TaskNotFoundError, TodoNotFoundError
import uuid
from ..utils.logger import logger

class ToDoRecord(DataRecord):
    def __init__(self, filename):
        super().__init__(filename)
  
    def id_exists(self, todo_list, new_id):
        return any(todo.to_do_identificator == new_id for todo in todo_list)
    
    def generate_unique_id(self):
        todo_full_list = self.get_models()
        new_id = str(uuid.uuid4())
        while self.id_exists(todo_full_list, new_id):
            new_id = str(uuid.uuid4()) 
        return new_id
    
    def get_todo_by_id(self, todo_id):
        todo_full_list = self.get_models()
        try:
            for record in todo_full_list:
                if record.to_do_identificator == todo_id:
                    logger.info(f'To Do com id {todo_id} encontrada com sucesso!')
                    return record
            raise TodoNotFoundError(task_id=todo_id)
        except TodoNotFoundError as e:
            logger.warning(e)
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar task por ID '{todo_id}': {e}")
            raise
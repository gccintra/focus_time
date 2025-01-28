from .data_record import DataRecord
from ..models.task import Task
from ..models.exceptions import TaskNotFoundError
import uuid
from ..utils.logger import logger

class TaskRecord(DataRecord):
    def __init__(self, filename):
        super().__init__(filename)

    def id_exists(self, task_list, new_id):
        return any(task.identificator == new_id for task in task_list)

    def generate_unique_id(self):
        task_full_list = self.get_models()
        new_id = str(uuid.uuid4())
        while self.id_exists(task_full_list, new_id):
            new_id = str(uuid.uuid4()) 
        return new_id
    
    def get_task_by_id(self, task_id):
        task_full_list = self.get_models()
        try:
            for record in task_full_list:
                if record.identificator == task_id:
                    logger.info(f'Task com id {task_id} encontrada com sucesso!')
                    return record
            raise TaskNotFoundError(task_id=task_id)
        except TaskNotFoundError as e:
            logger.warning(e)
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar task por ID '{task_id}': {e}")
            raise
    

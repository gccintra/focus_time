from .data_record import DataRecord
from ..models.task import Task
from ..models.exceptions import TaskNotFoundError, TaskTodoNotFoundError
import uuid
from ..utils.logger import logger

class TaskRecord(DataRecord):
    def __init__(self, filename):
        super().__init__(filename)

    def id_exists(self, tasks, new_id):
        return any(task.identificator == new_id for task in tasks)

    def generate_unique_id(self):
        new_id = str(uuid.uuid4())
        while self.id_exists(self._models, new_id):
            new_id = str(uuid.uuid4()) 
        return new_id
    
    def generate_unique_to_do_id(self, task_to_do_list):
        new_id = str(uuid.uuid4())
        while self.to_do_id_exists(task_to_do_list, new_id):
            new_id = str(uuid.uuid4())  
        return new_id
        
    def to_do_id_exists(self, task_to_do_list, new_id):
        return any(to_do.to_do_identificator == new_id for to_do in task_to_do_list)

    def get_task_by_id(self, task_id):
        try:
            for record in self._models:
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
    
    def create_to_do(self, task_id, to_do_instance):
        """Adiciona um to-do a uma tarefa específica."""
        try:
            task_instance = self.get_task_by_id(task_id)
            to_do_instance.to_do_identificator = self.generate_unique_to_do_id(task_instance.task_to_do_list)
            task_instance.task_to_do_list.append(to_do_instance)
            self.save_task_to_do_list_in_db(task_instance)
            logger.info(f"To-do criado com sucesso para a task '{task_id}'.")
        except TaskNotFoundError as e:
            logger.error(f"Erro inesperado ao criar to-do para a task '{task_id}': {e}")
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao criar to-do para a task '{task_id}': {e}")
            raise

    def update_to_do_status(self, task, updated_to_do):
        """Atualiza o status de um to-do em uma tarefa."""
        try:
            for to_do in task.task_to_do_list:
                if to_do.to_do_identificator == updated_to_do.to_do_identificator:
                    to_do.to_do_status = updated_to_do.to_do_status
                    to_do.to_do_completed_time = updated_to_do.to_do_completed_time
                    self.save_task_to_do_list_in_db(task)
                    logger.info(f"Status do to-do '{to_do.to_do_identificator}' atualizado com sucesso.")
                    return
            raise TaskTodoNotFoundError(updated_to_do.to_do_identificator)
        except TaskTodoNotFoundError as e:
            logger.warning(f"Erro ao atualizar status do to-do: {e}")
            raise
        except TaskNotFoundError as e:
            logger.warning(f"Erro ao atualizar status do to-do: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar status do to-do: {e}")
            raise


    def save_task_to_do_list_in_db(self, task_instance):
        try:
            self._update_record_field(task_instance, "task_to_do_list", task_instance.task_to_do_list)
        except (Exception, TaskNotFoundError):
            logger.error(f"Erro ao salvar lista de to-dos para a task '{task_instance.identificator}")
            raise

    def save_seconds_in_focus_per_day_in_db(self, task_instance):
        try:
            self._update_record_field(task_instance, "seconds_in_focus_per_day", task_instance.seconds_in_focus_per_day)
        except (Exception, TaskNotFoundError):
            logger.error(f"Erro ao salvar tempo de foco diário para a task '{task_instance.identificator}")
            raise

    def save_color_in_db(self, task_instance):
        try:
            self._update_record_field(task_instance, "color", task_instance.color)
        except (Exception, TaskNotFoundError):
            logger.error(f"Erro ao salvar a cor para a task '{task_instance.identificator}")
            raise

    def save_title_in_db(self, task_instance):
        try:
            self._update_record_field(task_instance, "title", task_instance.title)
        except (Exception, TaskNotFoundError):
            logger.error(f"Erro ao salvar o título para a task '{task_instance.identificator}")
            raise

    def _update_record_field(self, task_instance, field, value):
        try:
            for record in self._models:
                if record.identificator == task_instance.identificator:
                    setattr(record, field, value)
                    self.save()
                    logger.info(f"Campo '{field}' atualizado com sucesso para a task '{task_instance.identificator}'.")
                    return
            raise TaskNotFoundError(task_id=task_instance.identificator)
        except TaskNotFoundError as e:
            logger.warning(f"Erro ao atualizar o campo '{field}' da task '{task_instance.identificator}': {e}")
            raise
        except Exception as e:
            logger.error(f"Erro ao atualizar o campo '{field}' da task '{task_instance.identificator}': {e}")
            raise




from ..models.task import Task
from ..models.task_to_do import TaskToDo
from ..models.exceptions import TaskNotFoundError, TaskTodoNotFoundError, TaskValidationError
from ..repository.task_record import TaskRecord
from datetime import datetime
from ..utils.logger import logger
from ..models.exceptions import DatabaseError

class TaskService:
    def __init__(self):
        try:
            self.db = TaskRecord("task.json")
        except ValueError as e:
            logger.error(f"Erro ao inicializar TaskRecord: {e}")
            raise DatabaseError("Erro ao inicializar o banco de dados.")

    def get_all_tasks(self):
        return self.db.get_models()
      
    def get_data_for_all_charts(self):
        tasks_data = self.db.get_models()
        tasks_for_charts = []

        for task in tasks_data:
            if task.week_total_minutes > 0:  
                tasks_for_charts.append({
                    "identificator": task.identificator,
                    "title": task.title,
                    "color": task.color,
                    "minutes": task.week_total_minutes
                })
        return tasks_for_charts

    def create_new_task(self, name, color):
        try:
            identificator = self.db.generate_unique_id()
            new_task = Task(identificator=identificator, title=name, color=color)
            self.db.write(new_task)
            logger.info(f'Task {name} criada com sucesso!')
            return new_task
        except (TypeError, Exception):
            raise
       
    def update_task_time(self, task_id, elapsed_seconds):
        try:
            task = self.get_task_by_id(task_id)
            task.set_seconds_in_focus_per_day(elapsed_seconds)
            self.db.save_seconds_in_focus_per_day_in_db(task)
        except TaskValidationError as e:
            logger.error(e)
            raise
        except (TaskNotFoundError, Exception):   
            raise

    def create_task_to_do(self, task_id, to_do_name):
        try:
            new_to_do = TaskToDo(to_do_title=to_do_name)
            self.db.create_to_do(task_id, new_to_do)
            logger.info(f'To do {to_do_name} para a task {task_id} criado com sucesso!')
            return new_to_do
        except (TaskNotFoundError, Exception):
            raise

    def change_to_do_state(self, task_id, to_do_id, new_status):
        try:
            task = self.get_task_by_id(task_id)
            for to_do in task.task_to_do_list:
                if to_do.to_do_identificator == to_do_id:
                    to_do.to_do_status = new_status
                    to_do.to_do_completed_time = (
                        datetime.now().isoformat() if new_status == "completed" else None
                    )
                    self.db.update_to_do_status(task, to_do)
                    return to_do
            raise TaskTodoNotFoundError(to_do_id)
        except TaskValidationError as e:
            logger.error(e)
            raise
        except TaskTodoNotFoundError as e:
            logger.warning(f'Erro ao atualizar o status to-do: {e}')
            raise         
        except (TaskNotFoundError, Exception):
            raise

    def delete_to_do(self, task_id, to_do_id):
        try:
            task = self.get_task_by_id(task_id)
            for to_do in task.task_to_do_list:
                if to_do.to_do_identificator == to_do_id:
                    task.task_to_do_list.remove(to_do)
                    self.db.save_task_to_do_list_in_db(task) 
                    logger.info(f'To-do {to_do_id} da task {task.title} removido com sucesso!')
                    return
            raise TaskTodoNotFoundError(to_do_id)
        except TaskTodoNotFoundError as e:
            logger.warning(f'Erro ao deletar o to-do {to_do_id}: {e}')
            raise         
        except (TaskNotFoundError, Exception):
            raise
    
    def get_task_by_id(self, task_id):
        try:
            return self.db.get_task_by_id(task_id)
        except (TaskNotFoundError, Exception):
            raise

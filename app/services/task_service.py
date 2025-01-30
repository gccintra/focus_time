from ..models.task import Task
from ..models.exceptions import TaskNotFoundError, TaskValidationError
from ..repository.task_record import TaskRecord
from ..utils.logger import logger
from ..models.exceptions import DatabaseError

class TaskService:
    def __init__(self):
        try:
            self.task_db = TaskRecord("task.json")
        except ValueError as e:
            logger.error(f"Erro ao inicializar TaskRecord: {e}")
            raise DatabaseError("Erro ao inicializar o banco de dados.")

    def get_all_tasks(self):
        return self.task_db.get_models()
      
    def get_data_for_all_charts(self):
        tasks_data = self.task_db.get_models()
        tasks_for_charts = []

        for task in tasks_data:
        #    if task.week_total_minutes > 0:  
                tasks_for_charts.append({
                    "identificator": task.identificator,
                    "title": task.title,
                    "color": task.color,
                    "minutes": task.week_total_minutes
                })
        return tasks_for_charts

    def create_new_task(self, name, color):
        try:
            identificator = self.task_db.generate_unique_id()
            new_task = Task(identificator=identificator, title=name, color=color)
            self.task_db.write(new_task)
            logger.info(f'Task {name} criada com sucesso!')
            return new_task
        except (TypeError, Exception):
            raise
       
    def update_task_time(self, task_id, elapsed_seconds):
        try:
            task = self.get_task_by_id(task_id)
            task.set_seconds_in_focus_per_day(elapsed_seconds)
            self.task_db.save()
        except TaskValidationError as e:
            logger.error(f"Erro ao salvar tempo de foco diário para a task '{task.identificator}: {str(e)}")
            raise
        except (TaskNotFoundError, Exception):   
            logger.error(f"Erro ao salvar tempo de foco diário para a task '{task.identificator}")
            raise
    
    def get_task_by_id(self, task_id):
        try:
            return self.task_db.get_task_by_id(task_id)
        except (TaskNotFoundError, Exception):
            raise

 

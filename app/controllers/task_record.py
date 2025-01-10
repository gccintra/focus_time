from .data_record import DataRecord
from ..models.task import Task
import uuid

class TaskRecord(DataRecord):
    def __init__(self, filename):
        super().__init__(filename)

    def id_exists(self, tasks, new_id):
        return any(task.get('identificator', 0) == new_id for task in tasks)

    def generate_unique_id(self):
        new_id = str(uuid.uuid4())
        while self.id_exists(self._models, new_id):
            new_id = str(uuid.uuid4())  # Tenta gerar outro se já existir
        return new_id
    
    def create_to_do(self, task_id, to_do_obj):
        for record in self._models:
            if record["identificator"] == task_id:
                task_instance = Task(
                    identificator=record.get('identificator'),
                    title=record.get('title'),
                    color=record.get('color'), 
                    seconds_in_focus_per_day=record.get("seconds_in_focus_per_day"),
                    task_to_do_list=record.get("task_to_do_list"))
                
                to_do_obj.to_do_identificator = self.generate_unique_to_do_id(task_instance.task_to_do_list)

                task_instance.task_to_do_list.append(to_do_obj)
                record["task_to_do_list"] = [vars(to_do) for to_do in task_instance.task_to_do_list]

                self.save()

                return True
        return False
    

    def generate_unique_to_do_id(self, task_to_do_list):
        new_id = str(uuid.uuid4())
        while self.to_do_id_exists(task_to_do_list, new_id):
            new_id = str(uuid.uuid4())  # Tenta gerar outro se já existir
        return new_id
        
    def to_do_id_exists(self, task_to_do_list, new_id):
        return any(to_do.to_do_identificator == new_id for to_do in task_to_do_list)

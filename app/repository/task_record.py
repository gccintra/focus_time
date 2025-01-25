from .data_record import DataRecord
from ..models.task import Task
import uuid

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
        for record in self._models:
            if record.identificator == task_id:
                return record
        return None
    

##################  (Acho que ainda ta confuso isso aqui, depois ajustar)

    def create_to_do(self, task_id, to_do_instance):
        task_instance = self.get_task_by_id(task_id)
        if not task_instance:
            return False
                
        to_do_instance.to_do_identificator = self.generate_unique_to_do_id(task_instance.task_to_do_list)
        task_instance.task_to_do_list.append(to_do_instance)
    
        return self.save_task_to_do_list_in_db(task_instance)
    

    def update_to_do_status(self, task, updated_to_do):
        for to_do in task.task_to_do_list:
            if to_do.to_do_identificator == updated_to_do.to_do_identificator:
                to_do.to_do_status = updated_to_do.to_do_status
                to_do.to_do_completed_time = updated_to_do.to_do_completed_time
                return self.save_task_to_do_list_in_db(task)
        return False


    def save_task_to_do_list_in_db(self, task_instance):
        return self._update_record_field(task_instance, "task_to_do_list", task_instance.task_to_do_list)

    def save_seconds_in_focus_per_day_in_db(self, task_instance):
        return self._update_record_field(task_instance, "seconds_in_focus_per_day", task_instance.seconds_in_focus_per_day)

    def save_color_in_db(self, task_instance):
        return self._update_record_field(task_instance, "color", task_instance.color)

    def save_title_in_db(self, task_instance):
        return self._update_record_field(task_instance, "title", task_instance.title)

    def _update_record_field(self, task_instance, field, value):
        for record in self._models:
            if record.identificator == task_instance.identificator:
                setattr(record, field, value)
                self.save()
                return True
        return False



    
################## 

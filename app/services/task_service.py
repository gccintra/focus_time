from ..models.task import Task
from ..models.task_to_do import TaskToDo
from ..models.exceptions import TaskError
from ..controllers.task_record import TaskRecord
from datetime import datetime

class TaskService:
    def __init__(self):
        self.db = TaskRecord("task.json")

    def get_all_tasks(self):
        return self.db.get_models()           

    def get_data_for_chart(self, task_id):
        tasks_data = self.db.get_models()
        tasks_for_chart = []
        create_chart = False

        for task in tasks_data:

            if task.week_total_minutes > 0:
                tasks_for_chart.append( {

                        "identificator": task.identificator,
                        "title": task.title,
                        "color": task.color if task.identificator == task_id else "#474747",
                        "minutes": task.week_total_minutes
                    }) 
                
                if task.identificator == task_id:
                    create_chart = True

        return tasks_for_chart, create_chart

    def create_new_task(self, name, color):
        identificator = self.db.generate_unique_id()
        new_task = Task(identificator=identificator, title=name, color=color)
        self.db.write(new_task)
        return new_task

    def get_task_by_id(self, task_id):
        tasks = self.db.get_models()
        for task in tasks:
            if task.identificator == task_id:
                return task
        return None

    def update_task_time(self, task_id, elapsed_seconds):
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        task.set_seconds_in_focus_per_day(elapsed_seconds)
        self.db.save_seconds_in_focus_per_day_in_db(task)
        return task

    def create_task_to_do(self, task_id, to_do_name):
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        new_to_do = TaskToDo(title=to_do_name)
        if self.db.create_to_do(task_id, new_to_do):
            return new_to_do
        return None

    def change_to_do_state(self, task_id, to_do_id, new_status):
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        for to_do in task.task_to_do_list:
            if to_do.to_do_identificator == to_do_id:
                to_do.to_do_status = new_status
                to_do.to_do_completed_time = (
                    datetime.now().isoformat() if new_status == "completed" else None
                )
                if self.db.update_to_do_status(task, to_do):
                    return to_do
        return None
    
    def delete_to_do(self, task_id, to_do_id):
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        for to_do in task.task_to_do_list:
            if to_do.to_do_identificator == to_do_id:
                task.task_to_do_list.remove(to_do)
                return self.db.save_task_to_do_list_in_db(task)
            
        return False

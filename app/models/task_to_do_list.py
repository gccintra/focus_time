from datetime import datetime
import uuid


# TaaskToDoItem e não TaskToDoList ...
class TaskToDoList():
    def __init__(self, title, identificator=None, to_do_completed_time=None, to_do_status=None, to_do_created_time=None):
        self.to_do_title = title
        self.to_do_identificator = identificator or str(uuid.uuid4())
        self.to_do_created_time = to_do_created_time or datetime.now().isoformat()
        self.to_do_status = to_do_status or 'in progress'
        self.to_do_completed_time = to_do_completed_time



    def set_to_do_status(self, new_status):
        self.to_do_status = new_status


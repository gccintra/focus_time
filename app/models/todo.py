from app.models.base_model import BaseModel
from datetime import datetime
from app.models.exceptions import ToDoValidationError


class ToDo(BaseModel):
    def __init__(self, title, identificator, task_FK, created_time=None, status=None, completed_time=None):
        self._title = title
        self.__identificator = identificator 
        self.__task_FK = task_FK
        self._status = status or 'in progress'
        self._created_time = created_time or datetime.now().isoformat()
        self.completed_time = completed_time

    @property
    def title(self):
        return self._title
    
    @property
    def identificator(self):
        return self.__identificator
    
    @property
    def task_FK(self):
        return self.__task_FK   

    @property
    def status(self):
        return self._status

    @property
    def completed_time_formatted(self):
        return datetime.fromisoformat(self.completed_time).strftime("%m-%d-%Y %H:%M") if self.completed_time else None
    

    @property
    def created_time(self):
        return self._created_time
    
    @property
    def created_time_formatted(self):
        return datetime.fromisoformat(self._created_time).strftime("%m-%d-%Y %H:%M")


    @status.setter
    def status(self, value):
        valid_statuses = ["in progress", "completed", "deleted"]
        if value not in valid_statuses:
            raise ToDoValidationError('To-do Status', f"Invalid Status. Choose one: {', '.join(valid_statuses)}.")
        self._status = value  # Atribuindo ao atributo interno _status

    def mark_as_deleted(self):
        self.status = 'deleted' 

    def mark_as_in_progress(self):
        self.status = 'in progress' 
        self.completed_time = None 

    def mark_as_completed(self):
        self.status = 'completed' 
        self.completed_time = datetime.now().isoformat() 

    def to_dict(self):
        return {
            "task_FK": self.__task_FK,
            "title": self._title,
            "identificator": self.__identificator,
            "status": self._status,
            "created_time": self._created_time,
            "completed_time": self.completed_time
        }

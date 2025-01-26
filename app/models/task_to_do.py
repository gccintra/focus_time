from app.models.base_model import BaseModel
from datetime import datetime
import uuid
from app.models.exceptions import TaskValidationError


class TaskToDo(BaseModel):
    def __init__(self, to_do_title, to_do_identificator=None, to_do_completed_time=None, to_do_status=None, to_do_created_time=None):
        self.to_do_title = to_do_title
        self._to_do_identificator = to_do_identificator or str(uuid.uuid4())
        self.to_do_created_time = to_do_created_time or datetime.now().isoformat()
        self._to_do_status = to_do_status or 'in progress'
        self.to_do_completed_time = to_do_completed_time


    @property
    def to_do_completed_time_formatted(self):
        return datetime.fromisoformat(self.to_do_completed_time).strftime("%m-%d-%Y %H:%M") if self.to_do_completed_time else None
    
    @property
    def to_do_created_time_formatted(self):
        return datetime.fromisoformat(self.to_do_created_time).strftime("%m-%d-%Y %H:%M")
    
    @property
    def to_do_status(self):
        return self._to_do_status
    
    @property
    def to_do_identificator(self):
        return self._to_do_identificator
    
    @to_do_status.setter
    def to_do_status(self, value):
        valid_statuses = ["in progress", "completed"]
        if value not in valid_statuses:
            raise TaskValidationError('To-do Status', f"Invalid Status. Choose one: {', '.join(valid_statuses)}.")
        self._to_do_status = value

    @to_do_identificator.setter
    def to_do_identificator(self, value):
        self._to_do_identificator = value

    def to_dict(self):
        return {
            "to_do_title": self.to_do_title,
            "to_do_identificator": self._to_do_identificator,
            "to_do_created_time": self.to_do_created_time,
            "to_do_status": self.to_do_status,
            "to_do_completed_time": self.to_do_completed_time,
        }
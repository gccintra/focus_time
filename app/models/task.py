from datetime import date, timedelta
from app.models.task_to_do import TaskToDo
from app.models.base_model import BaseModel

class Task(BaseModel):    
    def __init__(self, identificator, title, color, seconds_in_focus_per_day={}, task_to_do_list=[]):
        self.identificator = identificator
        self.title = title
        self.color = color
        self.seconds_in_focus_per_day = seconds_in_focus_per_day

        # Garante que `task_to_do_list` contenha apenas instâncias de `TaskToDoList`
        self.task_to_do_list = [
            TaskToDo(
                title=to_do.get('to_do_title'),
                identificator=to_do.get('to_do_identificator'),
                to_do_created_time=to_do.get('to_do_created_time'),
                to_do_status=to_do.get('to_do_status'),
                to_do_completed_time=to_do.get('to_do_completed_time'),
            ) if isinstance(to_do, dict) else to_do for to_do in task_to_do_list
        ]

         
    @property
    def today_total_seconds(self):
        today = str(date.today())  
        total_seconds = self.seconds_in_focus_per_day.get(today, 0)
        return int(total_seconds)

    @property
    def today_total_minutes(self):
        return round(self.today_total_seconds / 60, 1)
    
    @property
    def today_total_time(self):
        hours, remainder = divmod(self.today_total_seconds, 3600)
        minutes = round(remainder / 60)
        formatted_time = f"{hours:02}h{minutes:02}m"
        return formatted_time
    
    @property
    def today_total_time_timer(self):
        hours, remainder = divmod(self.today_total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
        return formatted_time  
    
    @property
    def week_total_seconds(self):
        today = date.today()
        last_7_days = [(today - timedelta(days=i)).isoformat() for i in range(7)]

        total_week_seconds = 0
        for day in last_7_days:
            seconds_day = int(self.seconds_in_focus_per_day.get(day, 0)) 
            total_week_seconds += seconds_day
        
        return int(total_week_seconds)

    @property
    def week_total_minutes(self):
        return round(self.week_total_seconds / 60.0, 1)

    @property
    def week_total_time(self):
        hours, remainder = divmod(self.week_total_seconds, 3600)
        minutes = round(remainder / 60)
        formatted_time = f"{hours:02}h{minutes:02}m"
        return formatted_time
    

    def set_seconds_in_focus_per_day(self, seconds):
        today = str(date.today()) 
        self.seconds_in_focus_per_day[today] = seconds


    def to_dict(self):
        return {
            "identificator": self.identificator,
            "title": self.title,
            "color": self.color,
            "seconds_in_focus_per_day": self.seconds_in_focus_per_day,
            "task_to_do_list": [to_do.to_dict() for to_do in self.task_to_do_list]
        }
from datetime import date, timedelta

class Task:
    def __init__(self, identificator, title, color, minutes_in_focus_per_day={}):
        self.identificator = identificator
        self.title = title
        self.color = color
        self.minutes_in_focus_per_day = minutes_in_focus_per_day

    @property
    def today_total_time(self):
        today = str(date.today())  
        total_minutes = self.minutes_in_focus_per_day.get(today, "0")
        hours, minutes = divmod(int(total_minutes), 60)
        return f"{hours}h{minutes}m"
 
    @property
    def week_total_time(self):
        today = date.today()
        last_7_days = [(today - timedelta(days=i)).isoformat() for i in range(7)]

        total_minutes = 0
        for day in last_7_days:
            minute_str = int(self.minutes_in_focus_per_day.get(day, "0"))
            total_minutes += minute_str

        hours, minutes = divmod(total_minutes, 60)
        return f"{hours}h{minutes}m"
    


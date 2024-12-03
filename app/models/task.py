from datetime import date, timedelta

class Task:    
    def __init__(self, identificator, title, color, minutes_in_focus_per_day={}):
        self.identificator = identificator
        self.title = title
        self.color = color
        self.minutes_in_focus_per_day = minutes_in_focus_per_day

    @property
    def today_total_minutes(self):
        today = str(date.today())  
        total_minutes = self.minutes_in_focus_per_day.get(today, "0")
        return int(total_minutes)
    
    @property
    def today_total_time(self):
        hours, minutes = divmod(self.today_total_minutes, 60)
        formatted_time = f"{hours:02}h{minutes:02}m"
        return formatted_time

    @property
    def week_total_minutes(self):
        today = date.today()
        last_7_days = [(today - timedelta(days=i)).isoformat() for i in range(7)]

        total_minutes = 0
        for day in last_7_days:
            minute_str = int(self.minutes_in_focus_per_day.get(day, "0"))
            total_minutes += minute_str
        
        return int(total_minutes)

    @property
    def week_total_time(self):
        hours, minutes = divmod(self.week_total_minutes, 60)
        formatted_time = f"{hours:02}h{minutes:02}m"
        return formatted_time
    
    @property
    def today_total_time_timer(self):
        hours, minutes = divmod(self.today_total_minutes, 60)
        formatted_time = f"{hours:02}:{minutes:02}:00"
        return formatted_time 

    @property
    def today_total_seconds_timer(self):
        seconds = self.today_total_minutes * 60
        return seconds 
    

    def set_minutes_in_focus_per_day(self, minutes):
        today = str(date.today()) 
        self.minutes_in_focus_per_day[today] = minutes

    



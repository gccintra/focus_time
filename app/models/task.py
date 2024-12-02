from datetime import date, timedelta

class Task:
    def __init__(self, identificator, title, color, time_in_focus_per_day={}):
        self.identificator = identificator
        self.title = title
        self.color = color
        self.time_in_focus_per_day = time_in_focus_per_day


    @property
    def today_total_time(self):
        today = str(date.today())  
        return self.time_in_focus_per_day.get(today, "0h0m")
 
   
    @property
    def week_total_time(self):
        # Obter as datas dos últimos 7 dias
        today = date.today()
        last_7_days = [(today - timedelta(days=i)).isoformat() for i in range(7)]

        # Converter tempos diários para minutos
        total_minutes = 0
        for day in last_7_days:
            time_str = self.time_in_focus_per_day.get(day, "0h0m")
            total_minutes += self._time_to_minutes(time_str)

        # Converter minutos totais de volta para horas e minutos
        hours, minutes = divmod(total_minutes, 60)
        return f"{hours}h{minutes}m"

    def _time_to_minutes(self, time_str):
        """Converte uma string no formato 'XhYm' para minutos."""
        hours, minutes = 0, 0
        if "h" in time_str:
            hours = int(time_str.split("h")[0])
            time_str = time_str.split("h")[1]
        if "m" in time_str:
            minutes = int(time_str.split("m")[0])
        return hours * 60 + minutes
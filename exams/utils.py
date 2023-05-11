from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import DateExam, Aula
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, id=0, checklist=[], checkspan=[], span=0):
        self.year = year
        self.month = month
        self.id = id
        self.checklist = checklist
        self.checkspan = checkspan
        self.span = span
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, weekday, events, aula):
        events_per_day = events.filter(data__day=day)
        aula = aula.filter(data__day=day)
        d = ''
        if not events_per_day and weekday != 5 and weekday != 6:
            if aula.filter(nome=3):
                d += f'<li id=\'room\' ><b>Disponibilità<br>FA-2F:</b><br>'
                for sp in aula.filter(nome=3):
                    d += f'{sp.span_disponibilità}<br>'
                d += f'</li>'
            if aula.filter(nome=2):
                d += f'<li id=\'room\' ><b>Disponibilità<br>Fa-2g:</b><br>'
                for sp in aula.filter(nome=2):
                    d += f'{sp.span_disponibilità}<br>'
                d += f'</li>'
            if aula.filter(nome=1):
                d += f'<li id=\'room\' ><b>Disponibilità<br>FA-2E:</b><br>'
                for sp in aula.filter(nome=1):
                    d += f'{sp.span_disponibilità}<br>'
                d += f'</li>'
        for event in events_per_day:
            d += f'<li id=\'event\' > {event.exam}<br>{event.data.time()} </li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events, aula):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, weekday, events, aula)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        aula = Aula.objects.filter(data__year=self.year, data__month=self.month)
        events = DateExam.objects.filter(exam__facoltà_id=self.id, data__year=self.year, data__month=self.month)
        if not self.checklist:
            pass
        elif 1 not in self.checklist and 2 not in self.checklist and 3 not in self.checklist:
            if 4 not in self.checklist:
                events = events.exclude(exam__semestre=1)
            if 5 not in self.checklist:
                events = events.exclude(exam__semestre=2)
            if 6 not in self.checklist:
                events = events.exclude(exam__semestre=3)
        elif 4 not in self.checklist and 5 not in self.checklist and 6 not in self.checklist:
            if 1 not in self.checklist:
                events = events.exclude(exam__anno=1)
            if 2 not in self.checklist:
                events = events.exclude(exam__anno=2)
            if 3 not in self.checklist:
                events = events.exclude(exam__anno=3)
        else:
            if 1 not in self.checklist:
                events = events.exclude(exam__anno=1)
            if 2 not in self.checklist:
                events = events.exclude(exam__anno=2)
            if 3 not in self.checklist:
                events = events.exclude(exam__anno=3)
            if 4 not in self.checklist:
                events = events.exclude(exam__semestre=1)
            if 5 not in self.checklist:
                events = events.exclude(exam__semestre=2)
            if 6 not in self.checklist:
                events = events.exclude(exam__semestre=3)
        if 1 not in self.checkspan:
            aula = aula.exclude(nome=1)
        if 2 not in self.checkspan:
            aula = aula.exclude(nome=2)
        if 3 not in self.checkspan:
            aula = aula.exclude(nome=3)

        events = events.order_by("data")
        aula = aula.order_by("nome")
        cal = f'<table style="width:70%" border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events, aula)}\n'
        cal += f'</table>'
        return cal

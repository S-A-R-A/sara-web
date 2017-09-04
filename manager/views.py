from django.shortcuts import render
from .models import Day
from .models import Room
from .models import TimeInterval
from .models import Slot
from .models import Class
from .models import Period
from .models import Area

def show_timetabling(request, dayid=0, periodid=0, areaid=0):
    days = Day.objects.all()
    areas = Area.objects.all()
    periods = Period.objects.all()

    if int(dayid) == 0:
        day = Day.objects.first()
    else:
        day = Day.objects.get(id = int(dayid))

    table = dict(day = day, time_intervals = day.time_intervals.all(),
                 rooms = Room.objects.all(), slots = list(Slot.objects.filter(day = day)))

    return render(request, 'manager/show_timetabling.html', {'days': days, 'areas': areas, 'areaid': int(areaid),
                                                             'periods': periods, 'periodid': int(periodid),
                                                             'table': table, 'rooms_count': len(table["rooms"]) + 1})

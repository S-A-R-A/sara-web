from django.shortcuts import render
from .models import Day
from .models import Room
from .models import TimeInterval
from .models import Slot
from .models import Class

def show_timetabling(request):
    tables = []
    days = Day.objects.all()
    for day in days:
        table = dict(day = day, time_intervals = day.time_intervals.all(),
                     rooms = Room.objects.all(), slots = Slot.objects.filter(day = day))
        tables.append(table)

    return render(request, 'manager/show_timetabling.html', {'tables': tables})

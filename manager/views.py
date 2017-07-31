from django.shortcuts import render
from .models import Day
from .models import Room
from .models import TimeInterval
from .models import Slot
from .models import Class

def show_timetabling(request):
    days = Day.objects.all()
    slots_data_set = []
    rooms = Room.objects.all()

    for day in days:
        slots_data_set.append(Slot.objects.filter(day = day))

    return render(request, 'manager/show_timetabling.html', {'days': days, 'rooms': rooms, 'slots_data_set': slots_data_set})

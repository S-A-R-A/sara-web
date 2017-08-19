from django.db import models


class SlotManager(models.Manager):

    def slots_by_day(self, day, time_interval):
        return self.filter(day = day)

    def slots_by_day_time_interval(self, day, time_interval):
        return self.filter(day = day, time_interval = time_interval)

    def slots_by_room(self, room):
        return self.filter(room = room)

    def slot(self, room, day, time_interval):
        return self.filter(room = room, day = day, time_interval = time_interval)

class ScheduleManager(models.Manager):

    def reset_all_schedules(self):
        for s_class in Class.objects.all():
            del s_class.schedules[:]

    def reset_schedules_by_day(self, day):
        for s_class in Class.objects.all():
            for schedule in s_class.schedules.get(day = day):
                s_class.schedules.remove(schedule)

    def reset_schedules_by_course(self, course):
        for s_class in Class.objects.get(course = course):
            del s_class.schedules[:]

    def reset_class_schedules(self, id):
        s_class = Class.objects.get(id = id)
        if s_class:
            del s_class.schedules[:]

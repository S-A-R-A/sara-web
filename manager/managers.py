from django.db import models

class SlotManager(models.Manager):

    def slots_by_day(self, day):
        return self.filter(day = day)

    def slots_by_day_time_interval(self, day, time_interval):
        return self.filter(day = day, time_interval = time_interval)

    def slots_by_room(self, room):
        return self.filter(room = room)

    def slot(self, room, day, time_interval):
        return self.filter(room = room, day = day, time_interval = time_interval)

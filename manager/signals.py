from .models import Day, Room, TimeInterval, Slot, Schedule
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

@receiver(m2m_changed, sender=Day.time_intervals.through, dispatch_uid='slot_day_identifier')
def create_slot_per_day(sender, instance, action, model, **kwargs):
    if action == "post_add":
        for room in Room.objects.all():
             for interval in sender.objects.filter(day = instance.id).all():
                slot_new = Slot.objects.create(day = instance, room = room, time_interval = interval.timeinterval)
                slot_new.save()

@receiver(post_save, sender=TimeInterval, dispatch_uid='slot_time_interval_identifier')
def create_slot_per_time_interval(sender, instance, created, **kwargs):
    if created:
        for room in Room.objects.all():
            for day in Day.objects.all():
                if day.time_intervals.filter(id = instance.id).all():
                    slot_new = Slot.objects.create(day = day, room = room, time_interval = instance)
                    slot_new.save()

@receiver(post_save, sender=Room, dispatch_uid='slot_room_identifier')
def create_slot_per_room(sender, instance, created, **kwargs):
    if created:
        for day in Day.objects.all():
            for interval in TimeInterval.objects.all():
                if day.time_intervals.filter(id = interval.id).all():
                    slot_new = Slot.objects.create(day = day, room = instance, time_interval = interval)
                    slot_new.save()

@receiver(m2m_changed, sender=Day.time_intervals.through, dispatch_uid='schedule_day_identifier')
def create_schedule_per_day(sender, instance, action, model, **kwargs):
    if action == "post_add":
        for interval in sender.objects.filter(day = instance.id).all():
            schedule_new = Schedule.objects.create(day = instance, time_interval = interval.timeinterval)
            schedule_new.save()

@receiver(post_save, sender=TimeInterval, dispatch_uid='schedule_time_interval_identifier')
def create_schedule_per_time_interval(sender, instance, created, **kwargs):
    if created:
        for day in Day.objects.all():
            if day.time_intervals.filter(id = instance.id).all():
                schedule_new = Schedule.objects.create(day = day, time_interval = instance)
                schedule_new.save()

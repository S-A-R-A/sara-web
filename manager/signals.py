from .models import Day, Room, TimeInterval, Slot
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Day, dispatch_uid='day_identifier')
def create_slot_per_day(sender, instance, created, **kwargs):
    if created:
        for room in Room.objects.all():
            for interval in TimeInterval.objects.all():
                slot_new = Slot.objects.create(day = instance, room = room, time_interval = interval)
                slot_new.save()

@receiver(post_save, sender=TimeInterval, dispatch_uid='time_interval_identifier')
def create_slot_per_time_interval(sender, instance, created, **kwargs):
    if created:
        for room in Room.objects.all():
            for day in Day.objects.all():
                slot_new = Slot.objects.create(day = day, room = room, time_interval = instance)
                slot_new.save()

@receiver(post_save, sender=Room, dispatch_uid='room_identifier')
def create_slot_per_room(sender, instance, created, **kwargs):
    if created:
        for day in Day.objects.all():
            for interval in TimeInterval.objects.all():
                slot_new = Slot.objects.create(day = day, room = instance, time_interval = interval)
                slot_new.save()

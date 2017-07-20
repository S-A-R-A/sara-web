from .models import Day, Room, TimeInterval, Slot
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Room, dispatch_uid='room_indentifier')
@receiver(post_save, sender=TimeInterval, dispatch_uid='time_interval_indentifier')
@receiver(post_save, sender=Day, dispatch_uid='day_indentifier')
def create_slot(sender, instance, created, **kwargs):
    if created:
        for day in Day.objects.all():
            for room in Room.objects.all():
                for interval in TimeInterval.objects.all():                    
                    slot_new = Slot.objects.create(day = day, room = room, time_interval = interval)
                    slot_new.save()

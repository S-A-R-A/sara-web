from .models import Day, Room, RoomType, TimeInterval, Slot, Schedule, Class, GAConfig
from django.db.models.signals import post_save, m2m_changed, pre_delete, pre_save
from django.dispatch import receiver

@receiver(m2m_changed, sender=Class.schedules.through, dispatch_uid='class_schedules_identifier')
def clear_unused_slot(sender, instance, action, model, **kwargs):
    if action == "pre_remove" :
        schedules = Schedule.objects.filter(pk__in = kwargs.pop('pk_set', None))
        for schedule in schedules:
            unused_slot = Slot.objects.filter(day = schedule.day, s_class = instance, time_interval = schedule.time_interval)
            unused_slot.update(s_class = None)

@receiver(m2m_changed, sender=Day.time_intervals.through, dispatch_uid='slot_day_identifier')
def create_slot_per_day(sender, instance, action, model, **kwargs):
    if action == "post_add":
        for room in Room.objects.all():
             for interval in sender.objects.filter(day = instance.id).all():
                slot_new = Slot.objects.create(day = instance, room = room, time_interval = timeinterval)
                slot_new.save()
    elif action == "pre_remove":
        time_intervals = TimeInterval.objects.filter(pk__in = kwargs.pop('pk_set', None))
        Slot.objects.filter(day = instance, time_interval__in = time_intervals).delete()

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

@receiver(pre_delete, sender=Class, dispatch_uid='class_delete_identifier')
def clean_slot_before_delete_class(sender, instance, using, **kwargs):
    slots = Slot.objects.filter(s_class = instance)
    slots.update(s_class=None)

@receiver(post_save, sender=Class, dispatch_uid='default_room_type_identifier')
def add_default_room_type_to_class(sender, instance, created, **kwargs):
    if created:
        if not instance.type_rooms_wanted.all():
            room_type_default = RoomType.objects.first()
            instance.type_rooms_wanted.add(room_type_default)

@receiver(pre_save, sender=GAConfig, dispatch_uid='create_ga_config_identifier')
def create_ga_config(sender, instance, raw, **kwargs):
    GAConfig.objects.all().update(is_default=False)

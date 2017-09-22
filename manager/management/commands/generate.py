from django.core.management.base import BaseCommand, CommandError
from manager.models import Class
from manager.models import Schedule
from manager.models import Slot
from manager.models import Room
import json



class Command(BaseCommand):

    def load_json_data(self, file_name):
        with open(file_name) as json_data:
            f_json = json.load(json_data)
        return f_json

    def create_json_data(self, file_name, data):
        with open(file_name, 'w') as file:
            file.write(str(data))

    def models_to_file(self, file_name):
        models = {
            "slots": [],
            "classes": [],
            "rooms": []
        }

        slots = Slot.get_slots_by_schedules(Schedule.get_used_slots())
        classes = Class.get_scheduled_classes()
        rooms = Room.objects.all()

        for slot in slots:
            slot_model = {
                "id": slot.id,
                "capacity": slot.room.capacity,
                "room": slot.room.id,
                "schedule": Schedule.objects.get(day = slot.day, time_interval = slot.time_interval).id
            }
            models["slots"].append(slot_model)

        for s_class in classes:
            class_model = {
                "id": s_class.id,
                "size": s_class.size,
                "requirements": s_class.requirements
            }
            models["classes"].append(class_model)

        for room in rooms:
            room_model = {
                "id": room.id,
                "specifications": list(room.specifications.through.objects.all())
            }
            models["rooms"].append(room_model)
        self.create_json_data(file_name, json.dumps(models, indent=4, sort_keys=False))


    def add_arguments(self, parser):
        parser.add_argument('type_request', type=str)
        parser.add_argument('file_name', type=str)

    def handle(self, *args, **options):
        type_request = options['type_request']
        file_name = options['file_name']
        print("processing request...")

        if type_request == "request":
            file_name = "teste.json"
            print("creating {0} file...".format(file_name))
            self.models_to_file(file_name)
            print("the file was created...")
            print("request \"{0}\" completed successfully...".format(type_request))

        else:
            print("type request invalid!")

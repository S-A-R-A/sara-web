from django.core.management.base import BaseCommand, CommandError
from manager.models import Class
from manager.models import Schedule
from manager.models import Slot
import json

class Command(BaseCommand):

    def load_json_data(self, file_name):
        with open(file_name) as json_data:
            f_json = json.load(json_data)
        return f_json

    def create_json_data(self, file_name, data):
        with open(file_name, 'w') as file:
            file.write(str(data))

    def prepare_allocation_file(self, file_name):
        list_models=[]
        for slot in Slot.objects.all():
            dict_model = {
                "code": slot.id,
                "capacity": slot.room.capacity,
                "requirements": []
            }
            list_models.append(dict_model)
        self.generate_allocation_file(file_name, json.dumps(list_models, indent=4, sort_keys=True))

    def add_arguments(self, parser):
        parser.add_argument('type_request', type=str)
        parser.add_argument('file_name', type=str)

    def handle(self, *args, **options):
        type_request = options['type_request']
        file_name = options['file_name']
        print("processing request...")

        if type_request == "empty":
            for x in Slot.get_empty_slots() :
                print(x)
        elif type_request == "filled":
           for x in Slot.get_filled_slots() :
               print(x)

        else:
            print("type request invalid!")

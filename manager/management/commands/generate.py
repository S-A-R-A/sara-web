from django.core.management.base import BaseCommand, CommandError
from manager.models import Class
from manager.models import Schedule
from manager.models import Slot
from manager.models import Room
from manager.models import Requirement
from manager.models import GAConfig

import json



class Command(BaseCommand):

    def load_json_data(self, file_name):
        with open(file_name) as json_data:
            f_json = json.load(json_data)
        return f_json

    def create_json_data(self, file_name, data):
        with open(file_name, 'w') as file:
            file.write(str(data))

    def models_to_file(self, file_name, is_new_mapping, compact_file):
        models = {}

        models["request_type"] = "class_assignment" if is_new_mapping else "eval_solution"

        if is_new_mapping:
            models["ga_config"] = {}

        models["requirements"] = []
        models["schedules"] = []
        models["rooms"] = []
        models["slots"] = []
        models["classes"] = []

        print ("Just a second: [#.........]", end="\r")
        ga_config = GAConfig.get_default()
        schedules = Schedule.get_used_schedules()
        slots = Slot.get_slots_by_schedules(schedules)
        classes = Class.get_scheduled_classes()
        rooms = Room.objects.all()
        print ("Just a second: [##........]", end="\r")

        if(is_new_mapping and ga_config):
            ga_config_model = {
                "population_number": ga_config.population_number,
                "max_generation": ga_config.max_generation,
                "mutation_probability": ga_config.mutation_probability,
                "crossover_probability": ga_config.crossover_probability,
                "select_probability": ga_config.select_probability,
                "elitism_probability": ga_config.elitism_probability
            }
            models["ga_config"] = ga_config_model

        print ("Just a second: [###.......]", end="\r")
        for requirement in Requirement.objects.all():
            requirement_model = {
                "id" : requirement.id,
                "type": requirement.type.id,
                "priority": requirement.priority
            }
            models["requirements"].append(requirement_model)

        print ("Just a second: [####......]", end="\r")
        for schedule in schedules:
            schedules_model = {
                "id": schedule.id,
                "day": schedule.day.id,
                "time_interval": schedule.time_interval.id
            }
            models["schedules"].append(schedules_model)

        print ("Just a second: [#####.....]", end="\r")
        for slot in slots:
            slot_model = {
                "id": slot.id,
                ##"capacity": slot.room.capacity,
                "room": slot.room.id,
                "schedule": Schedule.objects.get(day = slot.day, time_interval = slot.time_interval).id
            }
            if not is_new_mapping:
                if slot.s_class:
                    slot_model["s_class"] = slot.s_class.id
            models["slots"].append(slot_model)

        print ("Just a second: [######....]", end="\r")
        for s_class in classes:
            class_model = {
                "id": s_class.id,
                "size": s_class.size,
                "schedules": list(s_class.schedules.all().values_list('id', flat=True)),
                "requirements": list(s_class.requirements.all().values_list('id', flat=True))
            }
            models["classes"].append(class_model)

        print ("Just a second: [#######...]", end="\r")
        for room in rooms:
            room_model = {
                "id": room.id,
                "specifications": list(room.specifications.all().values_list('id', flat=True)),
                "area": room.area.id,
                "capacity": room.capacity
            }
            models["rooms"].append(room_model)

        print ("Just a second: [#######..]", end="\r")

        if compact_file == 'true':
            self.create_json_data(file_name, json.dumps(models, sort_keys=False, separators=(',', ':')))
        else:
            self.create_json_data(file_name, json.dumps(models, indent=4, sort_keys=False, separators=(',', ':')))
        print ("Just a second: [#########]", end="\r")

    def add_arguments(self, parser):
        parser.add_argument('request_type', type=str)
        parser.add_argument('file_name', type=str)
        parser.add_argument('compact_file', type=str,  choices=['true', 'false'], default='true')

    def handle(self, *args, **options):
        request_type = options['request_type']
        file_name = options['file_name']
        compact_file = options['compact_file']
        print("processing request...")

        if any(request_type in t for t in ('room_mapping', 'rmp', 'evaluate_current_room_mapping', 'ecrm')):
            print("creating {0} file...".format(file_name))
            print ("Just a second: [..........]", end="\r")
            self.models_to_file(file_name, any(request_type in t for t in ('room_mapping', 'rmp')), compact_file)
            print("the file {0} was created...".format(file_name))
            print("request \"{0}\" completed successfully...".format(request_type))

        else:
            print("type request invalid!")
            print("please, type \"{}\" or \"{}\" to generate a new room mapping")

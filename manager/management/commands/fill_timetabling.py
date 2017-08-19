from django.core.management.base import BaseCommand, CommandError
from manager.models import Class
from manager.models import Schedule
import json

class Command(BaseCommand):

    def reset_timetabling(self):
        Class.reset_all_schedules()

    def load_json_data(self, file_name):
        with open(file_name) as json_data:
            f_json = json.load(json_data)
        return f_json

    def fill_timetabling(self, data):
        pass
        #for j in data:
        #    print(j)
        #print(Class.objects.get(id=1))
        #print(Schedule.objects.get(day=1, time_interval=14))

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str)

    def handle(self, *args, **options):
        file_name = options['file_name']

        self.reset_timetabling()
        print("schedules were deleted...")

        data = self.load_json_data(file_name)
        print("json file was loaded...")

        self.fill_timetabling(data)
        print("schedules were deleted...")

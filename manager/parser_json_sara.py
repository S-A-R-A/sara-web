# -*- coding: utf-8 -*-
import os
import importlib
from manager.models import Slot
import json


class LoadModelClasses(object):
    FILE_NAME = "manager/allocation_data.json"

    def open_allocation_file(self):
        with open(self.FILE_NAME) as data_file:
            data = json.load(data_file)
        return data

    def generate_allocation_file(self, file_name_arg, data):
        with open(file_name_arg, 'w') as file:
            file.write(str(data))

    def prepare_allocation_file(self):
        list_models=[]
        for slot in Slot.objects.all():
            dict_model = {
                "code": slot.id,
                "capacity": slot.room.capacity,
                "requirements": []
            }
            list_models.append(dict_model)
        self.generate_allocation_file(self.FILE_NAME, json.dumps(list_models, indent=4, sort_keys=True))

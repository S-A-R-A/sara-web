# -*- coding: utf-8 -*-
import os
import importlib
from manager.models import Slot
import json


class LoadModelClasses(object):

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
        self.generate_allocation_file("manager/allocation_data.json", json.dumps(list_models, indent=4, sort_keys=True))

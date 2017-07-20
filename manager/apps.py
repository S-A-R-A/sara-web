from django.apps import AppConfig


class ManagerConfig(AppConfig):
    name = 'manager'
    verbose_name = 'Sara Web'


    def ready(self):
        from . import signals

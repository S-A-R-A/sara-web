language = python
project_name = saraweb
environment = myvenv
data_path = manager/fixtures
initial_data = $(data_path)/initial_data.json
fake_classes = $(data_path)/fake_classes.json
fake_rooms = $(data_path)/fake_rooms.json
ads_classes = $(data_path)/ads_classes.json
other_classes = $(data_path)/other_classes.json
ads_rooms = $(data_path)/ads_rooms.json
other_rooms = $(data_path)/other_rooms.json
ads_timetabling = $(data_path)/ads_class_schedules.json
others_timetabling = $(data_path)/other_classes_schedules.json
ads_class_assignment = $(data_path)/ads_room_mapping_20171.json
manage = manage.py
activate = . $(environment)/bin/activate
fill_timetabling = fill_data timetabling
fill_class_assignment = fill_data class_assignment

venv:
	$(language) -m venv $(environment)
	$(activate)

migrate:
	$(activate)
	$(environment)/bin/pip install -r requirements.txt
	$(environment)/bin/$(language) $(manage) makemigrations manager
	$(environment)/bin/$(language) $(manage) migrate

default-data:
	$(activate)
	$(environment)/bin/$(language) $(manage) loaddata $(initial_data)

fake-data:
	$(environment)/bin/$(language) $(manage) loaddata $(fake_classes)
	$(environment)/bin/$(language) $(manage) loaddata $(fake_rooms)

ads-data:
	$(environment)/bin/$(language) $(manage) loaddata $(ads_classes)
	$(environment)/bin/$(language) $(manage) loaddata $(ads_rooms)
	$(environment)/bin/$(language) $(manage) $(fill_timetabling) $(ads_timetabling)
	$(environment)/bin/$(language) $(manage) $(fill_class_assignment) $(ads_class_assignment)

all-data:
	$(environment)/bin/$(language) $(manage) loaddata $(other_rooms)
	$(environment)/bin/$(language) $(manage) loaddata $(other_classes)
	$(environment)/bin/$(language) $(manage) $(fill_timetabling) $(others_timetabling)

run:
	$(activate)
	$(environment)/bin/$(language) $(manage) createsuperuser
	$(environment)/bin/$(language) $(manage) runserver

install-default: venv migrate default-data
install-ads: install-default ads-data
install-fake: install-default fake-data
install: install-ads all-data
all: install run

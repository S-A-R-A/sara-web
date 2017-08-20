language = python
project_name = saraweb
environment = myvenv
initial_data = manager/fixtures/initial_data.json
manage = manage.py
activate = . $(environment)/bin/activate
local_settings = local_settings.py

venv:
	$(language) -m venv $(environment)
	$(activate)

migrate:
	$(activate)
	$(environment)/bin/pip install -r requirements.txt
	cp $(project_name)/.$(local_settings) $(project_name)/$(local_settings)
	$(environment)/bin/$(language) $(manage) makemigrations manager
	$(environment)/bin/$(language) $(manage) migrate

default-data:
	$(activate)
	$(environment)/bin/$(language) $(manage) loaddata $(initial_data)
run:
	$(activate)
	$(environment)/bin/$(language) $(manage) createsuperuser
	$(environment)/bin/$(language) $(manage) runserver

install: venv migrate default-data

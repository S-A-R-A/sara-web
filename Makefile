language = python
environment = myvenv
initial_data = manager/fixtures/initial_data.json
manage = manage.py
activate = source $(environment)/bin/activate

venv:
	pip install virtualenv
	virtualenv $(environment)
	$(activate)

migrate:
	$(activate)
	pip install -r requirements.txt
	$(language) $(manage) makemigrations manager
	$(language) $(manage) migrate

default-data:
	$(activate)
	$(language) $(manage) loaddata $(initial_data)
run:
	$(activate)
	source $(environment)/bin/activate
	$(language) $(manage) createsuperuser
	$(language) $(manage) runserver

install: venv migrate default-data

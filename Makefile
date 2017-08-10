language = python
environment = myvenv
initial_data = manager/fixtures/initial_data.json
manage = manage.py
activate = . $(environment)/bin/activate

venv:
	myvenv/bin/pip install virtualenv
	virtualenv $(environment)
	$(activate)

migrate:
	$(activate)
	myvenv/bin/pip install -r requirements.txt
	myvenv/bin/$(language) $(manage) makemigrations manager
	myvenv/bin/$(language) $(manage) migrate

default-data:
	$(activate)
	myvenv/bin/$(language) $(manage) loaddata $(initial_data)
run:
	$(activate)
	myvenv/bin/$(language) $(manage) createsuperuser
	myvenv/bin/$(language) $(manage) runserver

install: venv migrate default-data

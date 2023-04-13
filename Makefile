WORKDIR = api_yamdb
MANAGE = python $(WORKDIR)/manage.py

default:
	$(MANAGE) makemigrations
	$(MANAGE) migrate
	$(MANAGE) runserver

style:
	black -S -l 79 $(WORKDIR)
	isort $(WORKDIR)
	flake8 $(WORKDIR)
	mypy $(WORKDIR)

migrations:
	$(MANAGE) makemigrations compositions --name $(name) --empty

nameless_migrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

run:
	$(MANAGE) runserver

test:
	pytest

shell:
	$(MANAGE) shell

app:
	$(MANAGE) startapp $(name) ./api_yamdb/$(name)

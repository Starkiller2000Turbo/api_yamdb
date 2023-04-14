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

import_categories:
	$(MANAGE) import_categories

import_genres:
	$(MANAGE) import_genres

import_titles:
	$(MANAGE) import_titles

import users:
	$(MANAGE) import_users

import comments:
	$(MANAGE) import_comments

import reviews:
	$(MANAGE) import_reviews

import:
	$(MANAGE) import_categories
	$(MANAGE) import_genres
	$(MANAGE) import_titles
	$(MANAGE) import_users
	$(MANAGE) import_comments
	$(MANAGE) import_reviews

clear:
	$(MANAGE) flush

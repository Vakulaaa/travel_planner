.PHONY: makemigrations migrate runserver test lint format fix coverage

makemigrations:
	.venv/bin/python manage.py makemigrations

migrate:
	.venv/bin/python manage.py migrate

run:
	.venv/bin/python manage.py runserver

test:
	.venv/bin/python manage.py test

lint:
	.venv/bin/ruff check apps config manage.py

format:
	.venv/bin/ruff format apps config manage.py

fix:
	.venv/bin/ruff check --fix apps config manage.py

coverage:
	.venv/bin/coverage erase
	.venv/bin/coverage run --source=apps/planner manage.py test
	.venv/bin/coverage report -m

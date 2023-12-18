SHELL := /bin/bash
py_warn = PYTHONDEVMODE=1


.DEFAULT_GOAL := pre-commit


install:
	poetry install --all-extras

docs:
	mkdocs serve

pre-commit:
	pre-commit run --all-files

format:
	poetry run ruff . --fix; \
	poetry run black .;

test:
	poetry run pytest --cov=. --cov-report=term-missing:skip-covered --cov-branch --cov-append --cov-report=xml tests;

supertest:
	make ci_supertest; \
	rm coverage.xml .coverage;
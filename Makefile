# Define variables
PYTHON := python3
PIP := pip
FLASK := flask
DOCKER := docker-compose

# Define targets and commands
.PHONY: install run migrate

install:
	$(PIP) install -r requirements.txt

migrate:
	$(FLASK) db migrate

apply-migrate:
	$(FLASK) db upgrade

dev:
	$(PYTHON) app.py

docker-remove:
	$(DOCKER) down

docker-build:
	$(DOCKER) build --no-cache

docker-run:
	$(DOCKER) up
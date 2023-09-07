# Define variables
PYTHON := python
PIP := pip
FLASK := flask
ALEMBIC := alembic

# Define targets and commands
.PHONY: install run migrate

install:
	$(PIP) install -r requirements.txt

migrate:
	$(ALEMBIC) upgrade head

alembic:
	alembic init alembic

# Add more targets and commands as needed

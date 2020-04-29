clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + > /dev/null 2>&1
	find . -type f -name "*.pyc" -exec rm -rf {} + > /dev/null 2>&1

start:
	python manage.py --runserver

lint:
	flake8 --show-source core

test:
	flake8 --show-source core
	isort --check-only -rc core --diff
	pytest --cov=core --cov-report=term --cov-report=html

all: clean lint

fix:
	black core
	isort -rc core

install:
	pip install -r requirements/dev.txt
	pre-commit install

# Path of the virtualenv directory
VENV?=.venv
IN_VENV=. $(VENV)/bin/activate ;

test: clean
	docker build -t open_parliament .
	docker run --rm -w /app/ open_parliament python -m pytest tests

test-local:
	python -m pytest --confcutdir=. tests

clean:
	find . -name "*.pyc" -delete

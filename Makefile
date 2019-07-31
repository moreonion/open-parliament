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

requirements: clean-reqs requirements/requirements.txt requirements/requirements-test.txt requirements/requirements-dev.txt

clean-reqs:
	rm -f requirements/*.txt

requirements/requirements.txt: requirements/requirements.in
	pip-compile --rebuild --output-file $@ requirements/requirements.in > /dev/null

requirements/requirements-test.txt: requirements/requirements-test.in requirements/requirements.in
	pip-compile --rebuild --output-file $@ requirements/requirements.in requirements/requirements-test.in > /dev/null

requirements/requirements-dev.txt: requirements/requirements.in requirements/requirements-test.in requirements/requirements-dev.in
	pip-compile --rebuild --output-file $@ requirements/requirements.in requirements/requirements-test.in requirements/requirements-dev.in > /dev/null

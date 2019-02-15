FROM python:3.6 as base

RUN mkdir /app
ADD ./requirements/ /app/requirements/
RUN pip install -r /app/requirements/requirements-dev.txt


FROM base as test
ADD . /app
WORKDIR /app/

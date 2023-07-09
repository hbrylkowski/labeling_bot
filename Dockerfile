FROM python:3.11

RUN mkdir /app
COPY /labeler /app

COPY pyproject.toml poetry.lock /app/

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --only main


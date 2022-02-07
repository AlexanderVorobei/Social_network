FROM python:3.9.2

# set working directory
WORKDIR /app

# set environment varibles
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV POETRY_VIRTUALENVS_CREATE=false

# install poetry
RUN pip install poetry

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install --no-dev --no-interaction

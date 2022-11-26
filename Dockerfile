FROM python:3.11.0-slim

RUN pip install poetry
WORKDIR /app/
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install

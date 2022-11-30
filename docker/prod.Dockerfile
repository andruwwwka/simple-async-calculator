FROM python:3.11.0-slim

RUN apt-get update && apt-get install make && apt-get --assume-yes install netcat
RUN pip install poetry
WORKDIR /app/
COPY poetry.lock .
COPY pyproject.toml .
COPY Makefile .
RUN make install-deps deps=production
COPY . .
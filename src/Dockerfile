FROM python:3.13-alpine

WORKDIR /usr/RatrWatch/src

ENV PYTHONUNBUFFERED=1 \
    TZ="Europe/Moscow"

RUN apk add curl --no-cache && \
    pip install poetry==2.3.2 --no-cache-dir

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-cache --without dev --no-root

COPY . .

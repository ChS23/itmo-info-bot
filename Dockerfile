FROM python:3.12.4-slim-bullseye AS base

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends curl cron git build-essential python3-setuptools python3-distutils \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/apt/lists/* \
    && rm -rf /var/cache/apt/*

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH" \
    POETRY_VERSION=1.8.0
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false \
    && mkdir -p /cache/poetry \
    && poetry config cache-dir /cache/poetry

FROM base AS runner

WORKDIR /app

COPY pyproject.toml ./

COPY . ./

RUN poetry install

RUN chmod 777 /app/scripts/entry

ENTRYPOINT ["/bin/bash", "/app/scripts/entry"]

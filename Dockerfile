FROM ubuntu:20.04

LABEL maintainer="Axel Rodríguez Chang <edgysquirrel@pm.me>"
LABEL version="0.1.0.0"

ARG PROJECT_ENV
ARG PROJECT_PATH="/home/src/"

ENV PROJECT_ENV=${PROJECT_ENV} \
    DEBIAN_FRONTEND=noninteractive \
    # python
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=$PYTHONPATH:${PROJECT_PATH} \
    # poetry
    POETRY_VERSION=1.1.7 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_CACHE_DIR="/var/cache/pypoetry" \
    PATH="$PATH:/root/.poetry/bin"

# system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libpq-dev \
    python3-dev \
    python3-pip \
    python-is-python3 \
    # python-is-python3 is needed so poetry can run the main.py file successfully.
    # it is a workaround that may need fixing in the future.
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
    && poetry --version \
    # clean cache
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR $PROJECT_PATH

COPY ./pyproject.toml ./poetry.lock $PROJECT_PATH

# Project initialization
RUN poetry --version \
    && poetry install \
    $(if [ "$PROJECT_ENV" = "production" ]; then echo "--no-dev"; fi) --no-interaction --no-ansi \
    # clean poetry installation's cache for production
    && if [ "$PROJECT_ENV" = "production" ]; then rm -rf "$POETRY_CACHE_DIR"; fi

COPY . $PROJECT_PATH

EXPOSE 8000
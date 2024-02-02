FROM python:3.8-slim

ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache
ENV PATH="${PATH}:${POETRY_HOME}/bin"

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

RUN mkdir /app
COPY pyproject.toml /app

COPY . /app

WORKDIR /app

RUN pip --default-timeout=1000 install poetry-plugin-export
RUN poetry export -f requirements.txt | pip --default-timeout=1000 install -r /dev/stdin

ENTRYPOINT ["python3.8", "-m", "str_producer.main"]
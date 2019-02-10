FROM python:3.7-alpine

RUN apk update && apk upgrade
RUN apk add --no-cache git bash

# Add build files for PyNaCl
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev

RUN set -ex && mkdir /app
WORKDIR /app
ADD . /app

COPY logzio.conf logzio.conf
COPY credentials.JSON credentials.JSON
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN pip install poetry
RUN poetry install --no-dev

RUN apk del .pynacl_deps

CMD ["python", "-m", "bot"]
FROM python:3.7-alpine

RUN apk update && apk upgrade
RUN apk add --no-cache git bash

# Add build files for PyNaCl
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev

RUN set -ex && mkdir /app
WORKDIR /app
ADD . /app

COPY credentials.JSON credentials.JSON
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apk del .pynacl_deps

CMD ["python", "-m", "bot"]
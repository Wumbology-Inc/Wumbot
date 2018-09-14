FROM python:3.6-alpine
# Add git
RUN apk update && apk upgrade && apk add --no-cache git
RUN apk add --no-cache bash

# Add build files for PyNaCl
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev

# Add user space
RUN addgroup -g 1168 -S wumbology
RUN adduser -S -G wumbology -H -u 1169 wumbot

RUN set -ex && mkdir /app
WORKDIR /app
ADD . /app

COPY requirements.txt requirements.txt
RUN set -ex && pip install -r requirements.txt

RUN apk del .pynacl_deps

COPY credentials.JSON credentials.JSON
USER wumbot
CMD ["python", "wumbotLogin.py"]
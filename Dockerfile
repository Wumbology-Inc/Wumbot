FROM python:3.6

RUN set -ex && mkdir /app
RUN set -ex && mkdir /log

WORKDIR /app
ADD . /app
RUN set -ex && pip install -r requirements.txt

COPY credentials.JSON credentials.JSON
CMD ["python", "wumbotLogin.py"]
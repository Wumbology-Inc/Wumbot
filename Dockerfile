FROM python:3.6

RUN set -ex && mkdir /app
WORKDIR /app

ADD . /app
COPY credentials.JSON credentials.JSON
RUN set -ex && pip install -r requirements.txt

CMD ["python", "wumbotLogin.py"]
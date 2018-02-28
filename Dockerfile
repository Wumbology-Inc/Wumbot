FROM python:3.6

RUN set -ex && mkdir /app

WORKDIR /app
ADD . /app
RUN set -ex && pip install -r requirements.txt

COPY credentials.JSON credentials.JSON
CMD ["python", "wumbotLogin.py"]
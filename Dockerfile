FROM python:3.6

RUN set -ex && mkdir /app
WORKDIR /app

RUN git clone -b develop https://github.com/Wumbology-Inc/Wumbot.git .
COPY credentials.JSON credentials.JSON

COPY requirements.txt requirements.txt
RUN set -ex && pip install -r requirements.txt

CMD ["python", "wumbotLogin.py"]
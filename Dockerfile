FROM python:3.10-slim-buster as build

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y wget netcat libpq-dev gcc && apt-get clean

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY requirements.txt ./
RUN pip install --no-cache-dir gunicorn psycopg2
RUN pip install --no-cache-dir -r requirements.txt

COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

COPY /app .

ENTRYPOINT ["./entrypoint.sh"]

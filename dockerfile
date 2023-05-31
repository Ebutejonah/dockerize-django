FROM python:3.10.5-alpine

# install django-crontab
RUN apk add --update apk-cron && rm -rf /var/cache/apk/*
RUN alias py=python

#set your working directory
WORKDIR /usr/src/dormafrica

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY ../dormafrica .
COPY ./requirements.txt .

RUN pip install -r requirements.txt

# django-crontab logfile
RUN mkdir /cron
RUN touch /cron/django_cron.log

EXPOSE 8000

CMD service cron start && python manage.py runserver 0.0.0.0:8000

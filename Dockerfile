FROM python:3.8
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/

RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN pip install urllib3
RUN pip install django-sslify
RUN pip install django-ckeditor

RUN apt update

COPY . /code/

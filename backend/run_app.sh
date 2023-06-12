#!/bin/bash
yes | python manage.py makemigrations;
python manage.py migrate;
python manage.py collectstatic --noinput;
gunicorn --bind 0:8000 foodgram.wsgi;

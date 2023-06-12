#!/bin/bash
python manage.py migrate;
python manage.py collectstatic --noinput;
gunicorn --bind 0:8000 foodgram.wsgi;

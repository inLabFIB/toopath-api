#!/bin/bash

python manage.py migrate --settings=TooPath3.settings.docker

export DJANGO_SETTINGS_MODULE=TooPath3.settings.docker
exec gunicorn -b 0.0.0.0:8080 TooPath3.wsgi


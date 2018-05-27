#!/bin/bash

python manage.py migrate --settings=TooPath3.settings.local

export DJANGO_SETTINGS_MODULE=TooPath3.settings.local
exec gunicorn -b 0.0.0.0:8080 TooPath3.wsgi


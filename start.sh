#!/usr/bin/env bash

# Configure Virtual Environment Wrapper
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export WORKON_HOME=~/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
workon toopath

# Install requirements
pip install -r requirements.txt

# Migrate
python manage.py migrate --settings=TooPath3.settings.production

# Start TooPath API
PID_FILE=~/toopath-api/toopath.pid
LOG_FILE=~/toopath-api/toopath.log
HOST=$(hostname -i)
export DJANGO_SETTINGS_MODULE=TooPath3.settings.production
gunicorn -b ${HOST}:8080 -D --access-logfile ${LOG_FILE} --log-file ${LOG_FILE} -p ${PID_FILE} TooPath3.wsgi


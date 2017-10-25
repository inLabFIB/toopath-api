#!/usr/bin/env bash

# Configure Virtual Environment Wrapper
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export WORKON_HOME=~/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
workon toopath

# Install requirements
pip install -r requirements.txt

# Migrate
python manage.py migrate --settings=TooPath3.settings.production || exit 1

# Start TooPath API
PID_FILE=~/toopath-api/toopath.pid
LOG_FILE=~/toopath-api/toopath.log
ACCESS_LOG_FILE=~/toopath-api/toopath-access.log
HOST=$(hostname -i)
export DJANGO_SETTINGS_MODULE=TooPath3.settings.production || exit 1
gunicorn -b 127.0.0.1:8080 ${HOST}:8080 -D --access-logfile ${ACCESS_LOG_FILE} --log-file ${LOG_FILE} -p ${PID_FILE} TooPath3.wsgi || exit 1


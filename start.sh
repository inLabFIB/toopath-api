#!/bin/bash

# Configure Virtual Environment Wrapper
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export WORKON_HOME=~/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
workon tootpath

# Install requirements
pip install -r requirements.txt

# Migrate
python manage.py migrate --settings=TooPath3.settings.production

# Start TooPath API
python manage.py runserver 0.0.0.0:8000 --settings=TooPath3.settings.production >> toopath.log 2>&1 &

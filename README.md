# TooPath v3

## Base Instructions

1. Install **[python 3.6.1](https://www.python.org/downloads/)**
2. Install **[virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper-win)** via ```easy_install virtualenvwrapper-win```.
3. Create new environment using ```mkvirtualenv env```
4. If **env** is not automatically activated, then use ```workon env```
5. Install all requirements with ```pip install -r requirements.txt```
6. Install **OSGeo4W** following the steps in **[GeoDjango Tutorial](https://docs.djangoproject.com/en/1.11/ref/contrib/gis/install/#osgeo4w)**
7. Install **[VirtualBox 5.1](https://www.virtualbox.org/wiki/Downloads)**  and turn on Vagrant machine with ```vagrant up```

## PyCharm setup

1. Go to  *File>Settings>Project:"name">Project interpreter>Add local*
2. Select **python.exe** from **env** folder
3. Mark *Associate this virtual environment with current project*
4. Configure the settings **INSTALLED_APPS** and **DATABASES** following the steps in **[Configure settings.py](https://docs.djangoproject.com/en/1.11/ref/contrib/gis/tutorial/#configure-settings-py)**

## Django commands

### Migrations
With Django, migrations become easier, it will generate migrations from the data models. Migrations will be saved with an automatic number identifier in *migrations* folder inside of the corresponding app.

Use ```python manage.py makemigrations --settings=TooPath3.settings.local``` to create migrations

Use ```python manage.py migrate --settings=TooPath3.settings.local``` to apply migrations

### Get it up
Use ```python manage.py runserver x.x.x.x:aaaa``` where x.x.x.x is the address and aaaa is the port

On local use ```python manage.py runserver 127.0.0.1:8080 --settings=TooPath3.settings.local```

On DEMO-VM use ```python manage.py runserver 127.0.0.1:8080 --settings=TooPath3.settings.production```

In case of migrates aren't applied you can follow the steps of the Migrations section using ```--settings=TooPath3.settings.production```
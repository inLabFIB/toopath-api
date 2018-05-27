# TooPath v3

[![Code coverage][shield-coverage]](#)
[![Requirements][shield-requirements]](#)
[![MIT licensed][shield-license]](#)
[![Last stable version][shield-version]](#)

[shield-coverage]: https://img.shields.io/badge/coverage-100%25-brightgreen.svg
[shield-license]: https://img.shields.io/badge/license-MIT-blue.svg
[shield-requirements]: https://img.shields.io/badge/requirements-up--to--date-brightgreen.svg
[shield-version]: https://img.shields.io/badge/last%20stable%20version-v1.0.0-green.svg

TooPath v3 is an API that let you manage tracks and locations related to a device. This API is protected with [JWT](https://jwt.io/) authentication and follows the [GeoJSON](http://geojson.org/) RFC 7946.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Docker image

If you only want to run TooPath you can use the available Docker image, after setting up database (see *Database section* below) you can do:

```
docker build -t toopath .
docker run --name toopath --net=host -p 8080:8080 toopath

```

And a working instance of TooPath will be available on port 8080.

### Prerequisites

* Install **[python 3.6.1](https://www.python.org/downloads/)**.
* Install **OSGeo4W** following the steps in **[GeoDjango Tutorial](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/tutorial/)** (make sure to install the same bit version of python and OSGeo4W.
* Install **[PyCharm](https://www.jetbrains.com/pycharm/download/)** (optional, recommended for Windows users).
 
#### Windows

* Install **[virtualenvwrapper-win](https://pypi.python.org/pypi/virtualenvwrapper-win)** via ```easy_install virtualenvwrapper-win```
* Install **[VirtualBox 5.1](https://www.virtualbox.org/wiki/Downloads)**.
* Install **[Vagrant 2.0.1](https://www.vagrantup.com/downloads.html)**.

#### Linux

* Install **[virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)** via ```pip install virtualenvwrapper```.
* Install **[PostgreSQL 9.6](https://www.postgresql.org/download/)**.
* Install **[PostGIS 2.3](http://postgis.net/install/)**.

### Environment setup

This environment setup can be done via console and also, via PyCharm console (if you have installed this IDE).
First of all, create a virtual environment:

```
mkvirtualenv [virtual_environment_name]
```

If the virtual environment is not automatically activated, then use:

```
workon [virtual_environment_name]
```

Install all the python requirements:

```
pip install -r requirements.txt
```

As it is recommended on this **[settings tutorial](https://medium.com/@ayarshabeer/django-best-practice-settings-file-for-multiple-environments-6d71c6966ee2)**, this project has production and local separate settings. To use the local settings setup your **DJANGO_SETTINGS_MODULE** environment variable to ```TooPath3.settings.local```.

#### Database setup

There is a **Vagrant** file and a **Docker** image with **PostgreSQL** and **PostGIS** installed and configured with local settings.

For those who prefer to use Vagrant, follow this **[Getting started of Vagrant](https://www.vagrantup.com/intro/getting-started/index.html)** to create a virtual machine with.

Docker users should build image and run a container using:

```
cd bootstrap
docker build -t toopath/postgres .
docker run --name postgres -p 15432:5432 toopath/postgres
```

Of course, manual configuration is available, you can create the database with the **PostgreSQL** and **PostGIS** versions mentioned above.

Apply all the migrations with:

```
python manage.py migrate
```

#### PyCharm setup

1. Go to  *File>Settings>Project:"name">Project interpreter>Add local*
2. Select **python.exe** from **[virtual_environment_name]** folder
3. Mark *Associate this virtual environment with current project*
4. Configure the settings **INSTALLED_APPS** and **DATABASES** following the steps in **[Configure settings.py](https://docs.djangoproject.com/en/1.11/ref/contrib/gis/tutorial/#configure-settings-py)**

## Running the API

Use ```python manage.py runserver x.x.x.x:aaaa``` where x.x.x.x is the address and aaaa is the port. For local example:

```
python manage.py runserver 127.0.0.1:8080 
```

## Running the tests

Once you’ve written tests, run them using the test command of your project’s **manage.py** utility:

```
python manage.py test
```

If you wanna run a concrete test you can do it specifying the package. For example, to run the devices test:

```
python manage.py test TooPath3.devices.tests
```

## Deployment (production)

To apply the migrations on the production environment use:

```
python manage.py migrate --settings=TooPath3.settings.production
```

To start the API on the production enviroment use:

```
python manage.py runserver x.x.x.x:aaaa --settings=TooPath3.settings.production
```

You can also setup the **DJANGO_SETTINGS_MODULE** environment variable to ```TooPath3.settings.production```.

## Built With

* **[Django REST](http://www.django-rest-framework.org/)** - framework used.
* **[Django REST-gis](https://github.com/djangonauts/django-rest-framework-gis)** - Geographic add-ons for Django REST.
* **[Jenkins](https://jenkins-ci.org/)** - Integration tool

## Authors

* Albert Díaz Benitez - *First stable version* - **[AlbertWayne](https://github.com/AlbertWayne)**

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/AlbertWayne/TooPath/tags). 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

* [inLab FIB](https://github.com/inLabFIB)
* [Jaume Figueras](https://github.com/JaumeFigueras) and [José Francisco Crespo](https://github.com/josefran)

# TooPath v3

[![MIT licensed][shield-license]](LICENSE.md)

[shield-license]: https://img.shields.io/badge/license-MIT-blue.svg

TooPath v3 is an API that let you manage tracks and locations related to a device.  This API is protected 
with [JWT](https://jwt.io/) authentication and follows the [GeoJSON](http://geojson.org/) 
[RFC 7946](https://tools.ietf.org/html/rfc7946).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development 
and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Docker image

If you only want to run TooPath you can use the available Docker image, 
after setting up database (see *Database section* below) you can do:

```bash
docker build -t toopath/api .
docker run --name toopath --network toopathnetwork -p 8080:8080 toopath/api
```

And a working instance of TooPath will be available on port 8080.

Network flag is required to connect this container to database container.

### Prerequisites

* Install **[python 3.6.1](https://www.python.org/downloads/)**.
* Install **OSGeo4W** following the steps in **[GeoDjango Tutorial][reference-to-geodjango]** 
(make sure to install the same bit version of python and OSGeo4W.
* Install **[PyCharm](https://www.jetbrains.com/pycharm/download/)** (optional, recommended for Windows users).

[reference-to-geodjango]: https://docs.djangoproject.com/en/2.0/ref/contrib/gis/tutorial/
 
#### Windows

* Install **[virtualenvwrapper-win](https://pypi.python.org/pypi/virtualenvwrapper-win)** 
via `pip install virtualenvwrapper-win`
* Install **[VirtualBox 5.1](https://www.virtualbox.org/wiki/Downloads)**.
* Install **[Vagrant 2.0.1](https://www.vagrantup.com/downloads.html)**.

#### Linux

* Install **[virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)** via 
`pip install virtualenvwrapper`.
* Install **[PostgreSQL 9.6](https://www.postgresql.org/download/)**.
* Install **[PostGIS 2.3](http://postgis.net/install/)**.

### Environment setup

This environment setup can be done via console and also, via PyCharm console (if you have installed this IDE).
First of all, create a virtual environment:

```bash
mkvirtualenv [virtual_environment_name]
```

If the virtual environment is not automatically activated, then use:

```bash
workon [virtual_environment_name]
```

Install all the python requirements:

```bash
pip install -r requirements.txt
```

As it is recommended on this **[settings tutorial][django-settings]**, this project has production 
and local separate settings. To use the local settings setup your **DJANGO_SETTINGS_MODULE** environment variable 
to `TooPath3.settings.local`.

[django-settings]: https://medium.com/@ayarshabeer/django-best-practice-settings-file-for-multiple-environments-6d71c6966ee2

#### Database setup

There is a **Vagrant** file and a **Docker** file with **PostgreSQL** and **PostGIS** installed and configured 
with local settings.

For those who prefer to use Vagrant, follow this **[Getting started of Vagrant][reference-vagrant]** to create 
a virtual machine with.

[reference-vagrant]: https://www.vagrantup.com/intro/getting-started/index.html

Docker users should build image and run a container using (network flag is required to connect this container 
to TooPath container):

```bash
cd bootstrap
docker build -t toopath/postgres .
docker run --name postgres -p 5432:5432 --network toopathnetwork toopath/postgres
```

Of course, manual configuration is available, you can create the database with the **PostgreSQL** 
and **PostGIS** versions mentioned above.

Apply all the migrations with:

```bash
python manage.py migrate
```

#### PyCharm setup

1. Go to  *File>Settings>Project:"name">Project interpreter>Add local*
2. Select **python.exe** from **[virtual_environment_name]** folder
3. Mark *Associate this virtual environment with current project*
4. Configure the settings **INSTALLED_APPS** and **DATABASES** following the steps 
in **[Configure settings.py](https://docs.djangoproject.com/en/1.11/ref/contrib/gis/tutorial/#configure-settings-py)**

## Running the API

Use `python manage.py runserver x.x.x.x:aaaa` where `x.x.x.x` is the address and `aaaa` is the port. For local example:

```bash
python manage.py runserver 127.0.0.1:8080 
```

## Running the tests

Once you’ve written tests, run them using the test command of your project’s **manage.py** utility:

```bash
python manage.py test
```

If you wanna run a concrete test you can do it specifying the package. For example, to run the devices test:

```bash
python manage.py test TooPath3.devices.tests
```

If you wanna run test inside docker:

```bash
docker exec -it <api_container_name> python manage.py test
```

## Deployment (production)

To apply the migrations on the production environment use:

```bash
python manage.py migrate --settings=TooPath3.settings.production
```

To start the API on the production enviroment use:

```bash
python manage.py runserver x.x.x.x:aaaa --settings=TooPath3.settings.production
```

You can also setup the **DJANGO_SETTINGS_MODULE** environment variable to `TooPath3.settings.production`.

## Built With

* **[Django REST](http://www.django-rest-framework.org/)** - framework used.
* **[Django REST-gis](https://github.com/djangonauts/django-rest-framework-gis)** - Geographic add-ons for Django REST.
* **[Jenkins](https://jenkins-ci.org/)** - Integration tool

## Authors

* Albert Díaz Benitez - *First stable version* - **[AlbertWayne](https://github.com/AlbertWayne)**

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, 
see the [tags on this repository](https://github.com/AlbertWayne/TooPath/tags). 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

* [inLab FIB](https://github.com/inLabFIB)
* [Jaume Figueras](https://github.com/JaumeFigueras) and [José Francisco Crespo](https://github.com/josefran)

from .base import *

DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'toopath',
        'USER': 'django',
        'PASSWORD': 'toopath3',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}

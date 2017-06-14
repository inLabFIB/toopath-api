from .base import *

DEBUG = True

ALLOWED_HOSTS = ['147.83.153.201', '147.83.153.208', '127.0.0.1']

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'toopath',
        'USER': 'toopath',
        'PASSWORD': 'toopath3',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

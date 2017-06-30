from django.conf.urls import url
from TooPath3.location import views as location_views

urlpatterns = [
    url(r'^devices/(?P<id>[0-9]+)/location$', location_views.device_location)
]

from django.conf.urls import url
from TooPath3.locations import views as locations_views
from TooPath3.devices import views as devices_views

urlpatterns = [
    url(r'^devices/(?P<id>[0-9]+)/actualLocation$', locations_views.device_actual_location),
    url(r'^devices/(?P<id>[0-9]+)', devices_views.device_detail),
]

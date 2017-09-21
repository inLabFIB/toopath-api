from django.conf.urls import url
from TooPath3.locations import views as locations_views
from TooPath3.devices import views as devices_views
from TooPath3.users import views as users_views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    url(r'^devices/(?P<id>[0-9]+)/actualLocation/$', locations_views.DeviceActualLocation.as_view()),
    url(r'^devices/(?P<id>[0-9]+)/$', devices_views.DeviceDetail.as_view()),
    url(r'^users', users_views.new_user),
    url(r'^login', obtain_jwt_token),
    url(r'^api-token-refresh', refresh_jwt_token),
    url(r'^api-token-verify', verify_jwt_token),
]

from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import User as UserModel


class Location(models.Model):
    point = gismodels.PointField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        abstract = True


class ActualLocation(Location):
    class Meta(Location.Meta):
        db_table = 'actual_locations'


class RouteLocation(Location):
    class Meta(Location.Meta):
        db_table = 'route_locations'


class Device(models.Model):
    PRIVATE = 'pr'
    PUBLIC = 'pu'
    ANONYMOUS = 'an'
    FRIENDS = 'fr'
    PRIVACY_CHOICES = (
        (PRIVATE, 'Private'),
        (PUBLIC, 'Public'),
        (ANONYMOUS, 'Anonymous'),
        (FRIENDS, 'Friends'),
    )
    ANDROID = 'ad'
    IPHONE = 'io'
    WINDOWS_PHONE = 'wp'
    ENFORA = 'en'
    TYPE_CHOICES = (
        (ANDROID, 'Android'),
        (IPHONE, 'iPhone'),
        (WINDOWS_PHONE, 'Windows Phone'),
        (ENFORA, 'Enfora'),
    )
    did = models.AutoField(primary_key=True, db_index=True, editable=False)
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    trash = models.BooleanField(null=False, default=False)
    ip_address = models.GenericIPAddressField(null=False)
    height = models.FloatField(null=True, default=None)
    speed = models.FloatField(null=True, default=None)
    heading = models.FloatField(null=True, default=None)
    utc = models.DateTimeField(null=True, db_index=True, default=None)
    device_privacy = models.CharField(max_length=2, null=False, choices=PRIVACY_CHOICES, default=PRIVATE)
    device_type = models.CharField(max_length=2, null=False, choices=TYPE_CHOICES, default=ANDROID)
    device_imei = models.CharField(max_length=40, null=True)
    actual_location = models.OneToOneField(ActualLocation, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserModel, related_name='devices', on_delete=models.CASCADE)

    class Meta:
        db_table = 'devices'

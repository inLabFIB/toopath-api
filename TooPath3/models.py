import uuid

from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    jwt_secret = models.UUIDField(
        'Token secret',
        help_text='Changing this will log out user everywhere',
        default=uuid.uuid4)


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
    ip_address = models.GenericIPAddressField(null=True)
    port_number = models.IntegerField(null=True)
    height = models.FloatField(null=True, default=None)
    speed = models.FloatField(null=True, default=None)
    heading = models.FloatField(null=True, default=None)
    utc = models.DateTimeField(null=True, db_index=True, default=None)
    device_privacy = models.CharField(max_length=2, null=False, choices=PRIVACY_CHOICES, default=PRIVATE)
    device_type = models.CharField(max_length=2, null=False, choices=TYPE_CHOICES, default=ANDROID)
    device_imei = models.CharField(max_length=40, null=True)
    owner = models.ForeignKey(CustomUser, related_name='devices', on_delete=models.CASCADE)

    class Meta:
        db_table = 'devices'


class Track(models.Model):
    tid = models.AutoField(primary_key=True, db_index=True, editable=False)
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=200, null=True)
    device = models.ForeignKey(Device, related_name='tracks', null=False)

    class Meta:
        db_table = 'tracks'


class Location(models.Model):
    point = gismodels.PointField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        abstract = True


class ActualLocation(Location):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, primary_key=True)

    class Meta(Location.Meta):
        db_table = 'actual_locations'


class TrackLocation(Location):
    track = models.ForeignKey(Track, related_name='locations', null=False)

    class Meta(Location.Meta):
        db_table = 'track_locations'

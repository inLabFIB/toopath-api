from django.db import models
from django.contrib.gis.db import models as gismodels


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

    class Meta:
        db_table = 'devices'


class Location(models.Model):
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    location = gismodels.PointField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        abstract = True


class ActualLocation(Location):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='actual_location')

    class Meta(Location.Meta):
        db_table = 'actual_location'

    def save(self, *args, **kwargs):
        self.latitude = self.location.y
        self.longitude = self.location.x
        super(Location, self).save(*args, **kwargs)


class RouteLocation(Location):
    class Meta(Location.Meta):
        db_table = 'route_location'

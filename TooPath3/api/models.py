from django.db import models
from django.contrib.gis.db import models as gismodels


class Device(models.Model):
    did = models.AutoField(primary_key=True, db_index=True, editable=False)
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    ip_address = models.GenericIPAddressField(null=False)
    location = gismodels.PointField(dim=2, srid=4326, spatial_index=True, null=True, default=None)
    height = models.FloatField(null=True, default=None)
    speed = models.FloatField(null=True, default=None)
    heading = models.FloatField(null=True, default=None)
    utc = models.DateTimeField(null=True, db_index=True, default=None)
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
    device_type = models.CharField(max_length=2, null=False, choices=TYPE_CHOICES, default=ANDROID)
    device_imei = models.CharField(max_length=40, null=True)
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
    device_privacy = models.CharField(max_length=2, null=False, choices=PRIVACY_CHOICES, default=PRIVATE)
    device_ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'device'

    def __init__(self, *args, **kwargs):
        super(Device, self).__init__(*args, **kwargs)

    @property
    def extract_latitude_point(self):
        return self.location.x

    @property
    def extract_longitude_point(self):
        return self.location.y


class Location(models.Model):
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    location = gismodels.PointField(null=False)
    did = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='device_did')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'location'

    def __init__(self, *args, **kwargs):
        super(Location, self).__init__(*args, **kwargs)

from django.db import models
from django.contrib.gis.db import models


class Device(models.Model):
    id = models.CharField(primary_key=True, max_length=20)

    class Meta:
        db_table = 'device'

    def __init__(self, *args, **kwargs):
        super(Device, self).__init__(*args, **kwargs)


class Location(models.Model):
    point = models.PointField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    class Meta:
        db_table = 'location'

    def __init__(self, *args, **kwargs):
        super(Location, self).__init__(*args, **kwargs)
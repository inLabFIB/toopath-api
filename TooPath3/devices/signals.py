from django.contrib.gis.geos import Point
from django.db.models.signals import *
from django.dispatch import receiver

from TooPath3.models import Device, ActualLocation


@receiver(pre_save, sender=Device)
def create_device(sender, instance, **kwargs):
    ActualLocation.objects.create(pk=instance.did, location=Point(0,0))
    instance.location_id = instance.did
from django.contrib.gis.geos import Point
from django.db.models.signals import *
from django.dispatch import receiver

from TooPath3.models import Device, ActualLocation


@receiver(pre_save, sender=Device)
def create_device(sender, instance, **kwargs):
    if not instance.actual_location_id:
        ActualLocation.objects.create(pk=instance.did, point=Point())
        instance.actual_location_id = instance.did

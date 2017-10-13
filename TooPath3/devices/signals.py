from django.contrib.gis.geos import Point
from django.db.models.signals import *
from django.dispatch import receiver

from TooPath3.models import Device, ActualLocation

# TODO: change signal pre save to post save due to one to one field model changed
@receiver(pre_save, sender=Device)
def create_device(sender, instance, **kwargs):
    if not instance.actual_location_id:
        ActualLocation.objects.create(point=Point())
        instance.actual_location_id = instance.did

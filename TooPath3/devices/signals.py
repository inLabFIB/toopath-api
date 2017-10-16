from django.contrib.gis.geos import Point
from django.db.models.signals import *
from django.dispatch import receiver

from TooPath3.models import Device, ActualLocation


@receiver(post_init, sender=Device)
def create_device(sender, instance, **kwargs):
    if not ActualLocation.objects.filter(pk=instance).exists():
        ActualLocation.objects.create(device=instance, point=Point())

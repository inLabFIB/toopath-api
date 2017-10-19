from django.contrib.gis.geos import Point
from django.db.models.signals import *
from django.dispatch import receiver

from TooPath3.models import Device, ActualLocation


@receiver(post_save, sender=Device)
def create_device(sender, instance, created, raw, **kwargs):
    if not ActualLocation.objects.filter(pk=instance).exists() and created:
        ActualLocation.objects.create(device=instance, point=Point())

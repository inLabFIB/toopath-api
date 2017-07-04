from django.apps import AppConfig


class TooPathConfig(AppConfig):
    name = 'TooPath3'

    def ready(self):
        import TooPath3.devices.signals
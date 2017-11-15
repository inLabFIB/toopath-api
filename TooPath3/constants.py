from django.utils.translation import ugettext_lazy as _

DEFAULT_ERROR_MESSAGES = {
    'invalid_latitude': _('Enter a valid latitude.'),
    'invalid_longitude': _('Enter a valid longitude.'),
    'invalid_format': _('Enter a valid body format.'),
    'invalid_patch': _('You are trying to change the instance representation, use a PUT method to do this.'),
    'patch_track_fields_required': _('You must provide a description or name fields to update the Track instance'),
    'patch_device_fields_required': _('You must provide a valid fields to update the Device instance')
}

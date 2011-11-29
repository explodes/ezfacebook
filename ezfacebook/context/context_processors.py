from django.conf import settings
from django.core.urlresolvers import reverse

from .templatetags import absurl

def facebook(request):
    d = _settings(request)
    d.update(_urls(request))
    return d

def _settings(request):
    return {
        'FACEBOOK_SETTINGS' : settings.FACEBOOK_SETTINGS
    }

def _urls(request):
    relative_channel_url = reverse('facebook-channel-url')
    absolute_channel_url = absurl.absolute_url(relative_channel_url, request=request, strip_protocol=True)
    return {
        'FACEBOOK_CHANNEL_URL' : absolute_channel_url
    }

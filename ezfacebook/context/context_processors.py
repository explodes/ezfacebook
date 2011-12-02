from django.conf import settings
from django.core.urlresolvers import reverse

from . import urls
from .templatetags import absurl

def facebook(request):
    """
    Sets context variables for a request...
    
    - FACEBOOK_SETTINGS : All facebook settings... i.e. scope: {{ FACEBOOK_SETTINGS.my_first_fb_app.scope }}
    
    - FACEBOOK_CHANNEL_URL : The absolute URL to channel.html, i.e {{ FACEBOOK_CHANNEL_URL }} >> //mysitedomain.com/facebookchannel/

    """

    d = _settings(request)
    d.update(_urls(request))
    return d

def _settings(request):
    """
    Put facebook settings into context:
    
    - FACEBOOK_SETTINGS : All facebook settings... i.e. scope: {{ FACEBOOK_SETTINGS.my_first_fb_app.scope }}
    
    """
    return {
        'FACEBOOK_SETTINGS' : settings.FACEBOOK_SETTINGS
    }

def _urls(request):
    """
    Put ezfacebook urls into context:
    
    - FACEBOOK_CHANNEL_URL : The absolute URL to channel.html
    
    """
    relative_channel_url = reverse('facebook-channel-url', urlconf=urls)
    absolute_channel_url = absurl.absolute_url(relative_channel_url, request=request)
    return {
        'FACEBOOK_CHANNEL_URL' : absolute_channel_url
    }

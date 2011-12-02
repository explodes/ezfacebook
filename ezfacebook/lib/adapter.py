import base64
import hashlib
import hmac

from django.conf import settings
from django.utils import simplejson, importlib

from . import api

__all__ = [
    'FacebookGraphAPI',
    'parse_signed_request',
    'parse_cookies',
    'get_graph_from_cookies',
]

def _base64_url_decode(inp):
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "=" * padding_factor
    return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))

def parse_signed_request(signed_request, secret):
    """
    Parse a signed request based on the secret and return the data (dictionary)
    Returns None on failure.
    
    Example:
    
        >>> parse_signed_request(request.POST['signed_request'], 'my_secret')
        {
         u'user_id': u'1234567890', 
         u'algorithm': u'HMAC-SHA256', 
         u'expires': 1322683200, 
         u'oauth_token': u'AAAAAABbbbcccccddddddeeeeeeeeeeeffffffffgHHHHHhhhhhhhhhhIjlkmop', 
         u'user': {
             u'locale': u'en_US', 
             u'country': u'us', 
             u'age': {u'min': 21}
         }, 
         u'issued_at': 1322676598, 
         u'page': {
             u'admin': False, 
             u'liked': True, 
             u'id': u'46326540287'
         }
        }
        
        or 
        
        >>> print parse_signed_request(request.POST['signed_request'], 'my_secret')
        None
        
    """
    l = signed_request.split('.', 2)
    encoded_sig = l[0]
    payload = l[1]

    sig = _base64_url_decode(encoded_sig)
    data = simplejson.loads(_base64_url_decode(payload))

    if data.get('algorithm').upper() != 'HMAC-SHA256':
        return None
    else:
        expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        return None
    else:
        return data

def parse_cookies(cookies, app_id, app_secret):
    """
    Parse cookies and return the Facebook GUID and Access Token found in the cookie, or None.
    
    example:
        >>> parse_cookies(request.COOKIES, 'my_app_id', 'my_secret')
        ('1234567890', 'AAAAAABbbbcccccddddddeeeeeeeeeeeffffffffgHHHHHhhhhhhhhhhIjlkmop')
        
        or 
        
        >>> print parse_cookies(request.COOKIES, 'my_app_id', 'my_secret')
        None
    """
    result = api.get_user_from_cookie(cookies, app_id, app_secret)
    if result: # result: {'access_token': 'AAAAAABbbbcccccddddddeeeeeeeeeeeffffffffgHHHHHhhhhhhhhhhIjlkmop', 'uid': u'1234567890'}
        return result['uid'], result['access_token']

class FacebookGraphAPI(api.GraphAPI):
    """
    Wrapper for the "official" GraphAPI object, the difference is that this object is aware of guid & token.
    Extend this object to add your most frequently used functions, such as posting a link to a wall, vs posting a picture to a wall...
    
    If you extend this class, be sure to set FACEBOOK_GRAPH_API_CLASS in your settings file so that is used by default.
    """
    def __init__(self, facebook_guid, access_token):
        super(FacebookGraphAPI, self).__init__(access_token)
        self.facebook_guid = facebook_guid
        self.access_token = access_token

def _getFacebookGraphAPIClass():
    if hasattr(settings, 'FACEBOOK_GRAPH_API_CLASS'):
        classpath = settings.FACEBOOK_GRAPH_API_CLASS
        paths = classpath.split('.')
        class_name = paths[-1]
        package_path = '.'.join(paths[:-1])
        package = importlib.import_module(package_path)
        return getattr(package, class_name)
    else:
        return FacebookGraphAPI

def get_graph_from_cookies(cookies, app_id, app_secret):
    """
    Returns a FacebookGraphAPI instance or subclass (as specified in the settings), or None, based on cookies.
    
    Example:
    
        >>> get_graph_from_cookies(request.COOKIES, 'my_app_id', 'my_secret')
        <MyFacebookGraphAPI>
        
        or 
        
        >>> print get_graph_from_cookies(request.COOKIES, 'my_app_id', 'my_secret')
        None
    """
    result = parse_cookies(cookies, app_id, app_secret)
    if result:
        return _getFacebookGraphAPIClass()(*result)

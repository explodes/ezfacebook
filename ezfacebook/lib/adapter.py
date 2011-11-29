import base64
import hashlib
import hmac

from django.utils import simplejson

from . import api

__all__ = [
    'FacebookGraphAPI',
    'parse_signed_request',
    'parse_cookie',
    'get_graph_from_cookie',
]

def _base64_url_decode(inp):
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "=" * padding_factor
    return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))

def parse_signed_request(signed_request, secret):
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

def parse_cookie(cookies, app_id, app_secret):
    result = api.get_user_from_cookie(cookies, app_id, app_secret)
    if result:
        return result['uid'], result['access_token']

def get_graph_from_cookie(cookies, app_id, app_secret):
    result = parse_cookie(cookies, app_id, app_secret)
    if result:
        return FacebookGraphAPI(*result)

class FacebookGraphAPI(api.GraphAPI):

    def __init__(self, facebook_guid, access_token):
        super(FacebookGraphAPI, self).__init__(access_token)
        self.facebook_guid = facebook_guid
        self.access_token = access_token

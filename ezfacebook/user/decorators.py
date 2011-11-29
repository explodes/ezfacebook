from django.conf import settings

from ..lib import adapter

__all__ = [
    'graphFromCookies',
    'parseSignedRequest',
]

def _app_id_and_secret(app_name):
    return settings.FACEBOOK_SETTINGS[app_name]['app_id'], settings.FACEBOOK_SETTINGS[app_name]['app_secret']

def graphFromCookies(app_name, use_debug=False, debug_user_id=None, debug_access_token=None):
    if use_debug:
        return _debugGraphFromCookies(debug_user_id, debug_access_token)
    else:
        return _graphFromCookies(app_name)

def _debugGraphFromCookies(debug_user_id, debug_access_token):
    def _debugGraphFromCookies_decorator(func):
        def _debugGraphFromCookies_decorated(request, *args, **kwargs):
            graph = adapter.FacebookGraphAPI(debug_user_id, debug_access_token)
            return func(request, graph, *args, **kwargs)
        return _debugGraphFromCookies_decorated
    return _debugGraphFromCookies_decorator

def _graphFromCookies(app_name):
    def _graphFromCookies_decorator(func):
        def _graphFromCookies_decorated(request, *args, **kwargs):
            app_id, secret = _app_id_and_secret(app_name)
            graph = adapter.parse_cookie(request.cookies, app_id, secret)
            return func(request, graph, *args, **kwargs)
        return _graphFromCookies_decorated
    return _graphFromCookies_decorator

def parseSignedRequest(app_name, use_debug=False, debug_data=None):
    if use_debug:
        return _debugParseSignedRequest(debug_data)
    else:
        return _parseSignedRequest(app_name)

def _debugParseSignedRequest(debug_data):
    def _debugParseSignedRequest_decorator(func):
        def _debugParseSignedRequest_decorated(request, *args, **kwargs):
            return func(request, debug_data, *args, **kwargs)
        return _debugParseSignedRequest_decorated
    return _debugParseSignedRequest_decorator

def _parseSignedRequest(app_name):
    def _parseSignedRequest_decorator(func):
        def _parseSignedRequest_decorated(request, *args, **kwargs):
            dummy, secret = _app_id_and_secret(app_name)
            signed_request = request.POST.get('signed_request', None)
            signed_request_data = None
            if signed_request:
                signed_request_data = adapter.parse_signed_request(signed_request, secret)
            return func(request, signed_request_data, *args, **kwargs)
        return _parseSignedRequest_decorated
    return _parseSignedRequest_decorator



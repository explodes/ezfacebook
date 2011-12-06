from ..lib import adapter, settings

__all__ = [
    'graph_from_cookies',
    'parse_signed_request',
]

def _inject_arg_decorator(app_settings, arg_injector):
    def _wrapper(func):
        def _decorator(request, *args, **kwargs):
            inject = arg_injector(request, app_settings)
            return func(request, inject, *args, **kwargs)
        return _decorator
    return _wrapper

def graph_from_cookies(app_name):
    """
    Put a FacebookGraphAPI (or specified subclass) object into the function arguments, after request.
    
    example:
    
        from django.conf import settings
        from django.core.urlresolvers import reverse
        
        from ezfacebook.context.templatetags import absurl
        from ezfacebook.user import decorators
    
        @decorators.graph_from_cookies('my_first_fb_app') # or graph_from_cookies(settings.FACEBOOK_SETTINGS.my_first_fb_app)
        def post_to_wall(request, graph, *args, **kwargs):
            
            image_url = absolute_url("%simages/fb_image.png" % settings.MEDIA_URL, request=request)
            link = absolute_url(reverse('myviews.index', request=request))
            
            graph.put_object("me", "feed", picture=image_url, name='Whatsup', description='Hello', link=link, caption='Pow Mow Local')
            
            return direct_to_template(request, 'success.html')
    """
    app_settings = settings.app_settings(app_name)
    injector_method = _graph_from_cookies_method(app_settings)
    return _inject_arg_decorator(app_settings, injector_method)

def _graph_from_cookies_method(app_settings):
    if hasattr(app_settings, 'debug_guid') and app_settings.debug_guid != False and hasattr(app_settings, 'debug_token') and app_settings.debug_token != False:
        return _debug_graph_from_cookies
    else:
        return _graph_from_cookies

def _debug_graph_from_cookies(request, app_settings):
    graph = adapter._getFacebookGraphAPIClass()(app_settings.debug_guid, app_settings.debug_token)
    return graph

def _graph_from_cookies(request, app_settings):
    graph = adapter.get_graph_from_cookies(request.COOKIES, app_settings.app_id, app_settings.secret)
    return graph

def parse_signed_request(app_name):
    """
    Put a FacebookGraphAPI object into the function arguments, after request.
    
    example:
    
        from django.conf import settings
        from django.core.urlresolvers import reverse
        
        from ezfacebook.context.templatetags import absurl
        from ezfacebook.user import decorators
    
        @decorators.parse_signed_request('my_first_fb_app') # or graph_from_cookies(settings.FACEBOOK_SETTINGS.my_first_fb_app)
        def index(request, signed_request, *args, **kwargs):
            '''
            >>> print signed_request
            <the debug_signed_request data for 'my_first_fb_app'>
            or
            >>> print signed_request
            None
            or
            >>> print signed_request
            {u'user_id': u'11111111111', u'algorithm': u'HMAC-SHA256', u'expires': 1322683200, u'oauth_token': u'AAAAAAAAAAAAA', 
            u'user': {u'locale': u'en_US', u'country': u'us', u'age': {u'min': 21}}, u'issued_at': 1322676598, 
            u'page': {u'admin': False, u'liked': True, u'id': u'46326540287'}}
            '''
        
            if signed_request:
                page = signed_request.get('page', None)
                if page:
                    liked = page.get('liked', False)
                    if liked:
                        return direct_to_template(request, 'liked.html')
            return direct_to_template(request, 'unliked.html')
    """
    app_settings = settings.app_settings(app_name)
    injector_method = _parse_signed_request_method(app_settings)
    return _inject_arg_decorator(app_settings, injector_method)

def _parse_signed_request_method(app_settings):
    if hasattr(app_settings, 'debug_signed_request') and app_settings.debug_signed_request != False:
        return _debug_parse_signed_request
    else:
        return _parse_signed_request

def _debug_parse_signed_request(request, app_settings):
    signed_request_data = app_settings.debug_signed_request
    return signed_request_data

def _parse_signed_request(request, app_settings):
    signed_request = request.POST.get('signed_request', None)
    if signed_request:
        try:
            return adapter.parse_signed_request(signed_request, app_settings.secret)
        except:
            return None



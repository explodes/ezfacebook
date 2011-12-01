# EZ-Facebook Django Utils (for django 1.3+)

* Under Development, not for production *

_The exact framework is TBD, to allow multiple facebook apps to be used in a single site. This may or may not be a popular feature, let me know what you think..._

The purpose of this package is to make facebook integration with web apps used as page tabs, web apps, 


The current "apps" are context, helpers, and user...


## Context

This 'app' contains context processors and middleware to use the Javascript SDK to let users login or perform dialog functions.

It makes your facebook settings available to the context as well as FACEBOOK_CHANNEL_URL.

Configuration is easy for this, in your settings file:

	TEMPLATE_CONTEXT_PROCESSORS = (
		'ezfacebook.context.context_processors.facebook', # Puts FACEBOOK_SETTINGS and FACEBOOK_CHANNEL_URL in template context
	)
	
	class FACEBOOK_SETTINGS:
	
	    class my_first_fb_app:
	    
	        app_id = '00000000000000',
	        secret = 'abcdef0123456789',
	        scope = 'email,publish_stream,offline_access'
	        
	        debug_signed_request = {'id': 23840238402834}
	        debug_guid = 23840238402834
	        debug_token = 'AAAAAAAAAbbbbbbbbbbccccdefffffffffffffffffffetc'
	        
	    class my_second_fb_app:
	    
	        app_id = '11111111111111',
	        secret = '9876543210abcdef',
	        scope = ''
	        
	        debug_signed_request = False
	        debug_guid = False
	        debug_token = False
	
## Helpers
	
### Middleware

This 'app' has middleware to help out your application.

	MIDDLEWARE_CLASSES = (
		'ezfacebook.helpers.middleware.IEIFrameApplicationMiddleware'
	)

#### IEIFrameApplicationMiddleware

Sets response headers (P3P policy) to allow IE 7-8 to use cookies inside of an iframe.
This is useful for websites that are put in iframes on facebook, such as page tabs and facebook apps.

## User

Under development, the idea here is to use decorators to pass extra variables into views, such as a facebook_user, whether or not they like an app, and their current access rights.

### Decorators

#### parseSignedRequest

Parses the signed request and puts the dictionary in the method arguments after request.
It can be None.
A signed request is good for a lot of things, of which can be found at http://developers.facebook.com/docs/authentication/signed_request/

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
			
#### graphFromCookies

Adds a FacebookGraphAPI instance, or None, to the view arguments after request.

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

			
		
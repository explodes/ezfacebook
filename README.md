# EZ-Facebook Django Utils (for django 1.3+)

*FULLY FUNCTIONAL BETA*

The purpose of this package is to make facebook integration easy WITHOUT having to make your whole app depend on this package.

This package makes facebook integration easy for all kinds of web sites:

- Web Applications
- Facebook Page Tabs
- Facebook Applications

Included in the suite are:

- Easy to use facebook settings with debug settings
- View decorators that extract information from requests, like signed_request, and facebook graph api.
- NEW: Middleware to apply those decorators to all functions for all defined facebook apps.
- Facebook script template tags
- Facebook Channel URL context variable and view
- Facebook Settings context processors
- Absolute Url template tag, minds current protocol. Useful for posting links and images.
- P3P Cookie middleware to enable the use of cookies in your iframes

# Installation

(See ezfacebook/example_settings.py and ezfacebook/example_urls.py for examples, or view below)

## Settings :: example `settings.py` file

	TEMPLATE_CONTEXT_PROCESSORS = (
	    'ezfacebook.context.context_processors.facebook', # ezfacebook.context: Requirement
	)
	
	MIDDLEWARE_CLASSES = (
	    'ezfacebook.helpers.middleware.IEIFrameApplicationMiddleware', # ezfacebook.helpers: Optional
    	'ezfacebook.user.middleware.FacebookRequestMiddleware', # ezfacebook.user: Optional
	)
	
	INSTALLED_APPS = (
	    'django.contrib.sites', # ezfacebook.context: Requirement
	    'ezfacebook.context', # ezfacebook.context: Optional, allows templatetags absurl
	)
	
	# Overrides original FacebookGraphAPI class
	FACEBOOK_GRAPH_API_CLASS = 'myproject.myapp.lib.facebook.MyFacebookGraphAPI' # ezfacebook.lib (affects ezfacebook.user), Optional
	
	class FACEBOOK_SETTINGS: # ezfacebook.user, ezfacebook.context: Requirement
	
	    class my_first_fb_app:
	        app_id = '00000000000000'
	        secret = 'abcdef0123456789'
	        scope = 'email,publish_stream,offline_access'
	
	        debug_signed_request = {'id': 23840238402834} # Simulate the JSON returned by a decoded and parsed signed request
	        debug_guid = 23840238402834 # Pretend the Facebook user has this Facebook GUID
	        debug_token = 'AAAAAAAAAbbbbbbbbbbccccdefffffffffffffffffffetc' # Pretend the Facebook user has this access token
	
	    class my_second_fb_app:
	        app_id = '11111111111111'
	        secret = '9876543210abcdef'
	        scope = ''
        	# Disable debugging by omitting the debug settings or by setting them to false

        
## URLS :: example `urls.py` file

	from django.conf.urls.defaults import patterns, include, url
	
	urlpatterns = patterns('',
	    url(r'^fb/', include('ezfacebook.context.urls')),
	)

# Packages

# Context :: `ezfacebook.context`, installable app (if necessary)

This packages comes with the following features:

- Template Tags
- Context Processors
- channel.html view

## Template Tags :: `ezfacebook.context.templatetags`

This package must be installed in your application to use template tags.

### absurl :: `ezfacebook.context.templatetags.absurl`

#### absolute_url :: `ezfacebook.context.templatetags.absurl.absolute_url`

Builds an absolute URL for the given path.
If request is provided, the protocol (http or https) is determined from the request, otherwise http is used.

Example:

	{% load absurl %}
	
	{{ obj.image.url|absolute_url }}
	{{ obj.image.url|absolute_url:request }}

### fb_script :: `ezfacebook.context.templatetags.fb_script`

These template tags render the HTML required to the Facebook Javascript SDK.

#### fb_script :: `ezfacebook.context.templatetags.fb_script.fb_script`

Renders the Facebook Javascript SDK script required for facebook connectivity.

Example:

    {% load fb_script %}
    
    {% fb_script 'my_first_fb_app' %}
    
    {% fb_script 'my_first_fb_app' use_share=True %} {# Also loads FB.Share javascript #}
    
    {# See http://bugs.developers.facebook.net/show_bug.cgi?id=19042 #}
    {% fb_script 'my_first_fb_app' fix_19042=True %} 
    
    {# See http://bugs.developers.facebook.net/show_bug.cgi?id=20168= #}
    {% fb_script 'my_first_fb_app' fix_20168=True %} 

#### fb_script_with_canvas :: `ezfacebook.context.templatetags.fb_script.fb_script_with_canvas`

Renders the Facebook Javascript SDK script required for facebook connectivity and sets the Facebook Canvas size.
    
Example:
    
    {% load fb_script %}
    
    {% fb_script_with_canvas 'my_first_fb_app' canvas_height=2000 canvas_width=500 %} {# 500 is the recommended width for a Page Tab #}
    
    {% fb_script_with_canvas 'my_first_fb_app' canvas_height=2000 canvas_width=500 use_share=True %} {# 500 is the recommended width for a Page Tab #} {# Also loads FB.Share javascript #}
    
    {# See http://bugs.developers.facebook.net/show_bug.cgi?id=19042 #}
    {% fb_script_with_canvas 'my_first_fb_app' canvas_height=2000 canvas_width=500 fix_19042=True %} 
    
    {# See http://bugs.developers.facebook.net/show_bug.cgi?id=20168= #}
    {% fb_script_with_canvas 'my_first_fb_app' canvas_height=2000 canvas_width=500 fix_20168=True %} 
	
# Helpers :: `ezfacebook.helpers`

This packages comes with the following features:

- Middleware
	
## Middleware :: `ezfacebook.helpers.middleware`

This package has middleware to help out your application.

### IEIFrameApplicationMiddleware :: `ezfacebook.helpers.middleware.IEIFrameApplicationMiddleware`

It is not necessary to install this package as an app to use this middleware.

Sets response headers (P3P policy) to allow IE 7-8 to use cookies inside of an iframe.
This is useful for websites that are put in iframes on facebook, such as page tabs and facebook apps.

To use it, simply add 'ezfacebook.helpers.middleware.IEIFrameApplicationMiddleware' to MIDDLEWARE_CLASSES in your settings file. 

# Lib :: `ezfacebook.lib`

This packages comes with the following features:

- Facebook Graph API
- Library Functions

## Adapter :: `ezfacebook.lib.adapter`

### FacebookGraphAPI :: `ezfacebook.lib.adapter.FacebookGraphAPI`

Wrapper for the "official" `GraphAPI` object, the difference is that this object is aware of guid & token.
Extend this object to add your most frequently used functions, such as posting a link to a wall, vs posting a picture to a wall...
    
If you extend this class, be sure to set `FACEBOOK_GRAPH_API_CLASS` in your settings file so that is used by default.

### parse_signed_request :: `ezfacebook.lib.adapter.parse_signed_request`

Parse a signed request based on the secret and return the data (dictionary)
Returns `None` if the signed_request did not parse properly.
    
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

### parse_cookies :: `ezfacebook.lib.adapter.parse_cookies`

Parse cookies and return the Facebook GUID and Access Token found in the cookie, or `None`.
    
Example:
    
    >>> parse_cookies(request.cookies, 'my_app_id', 'my_secret')
    ('1234567890', 'AAAAAABbbbcccccddddddeeeeeeeeeeeffffffffgHHHHHhhhhhhhhhhIjlkmop')
    
    or 
    
    >>> print parse_cookies(request.cookies, 'my_app_id', 'my_secret')
    None

### get_graph_from_cookies :: `ezfacebook.lib.adapter.get_graph_from_cookies`

Returns a `FacebookGraphAPI` instance or subclass (as specified in the settings), or `None`, based on cookies.
    
Example:
    
    >>> get_graph_from_cookies(request.cookies, 'my_app_id', 'my_secret')
    <MyFacebookGraphAPI>
    
    or 
    
    >>> print get_graph_from_cookies(request.cookies, 'my_app_id', 'my_secret')
    None

# User :: `ezfacebook.user`

This package is responsible for extracting user information from a request.
Currently this is done with the use of decorators.
In the future, some kind of middleware may be added.

This packages comes with the following features:

- Decorators

## Decorators :: `ezfacebook.user.decorators`

These decorators are used on view functions, they will inject the results as the parameter after request.
Any other arguments or keyword arguments are still sent to the view.

### parse_signed_request :: `ezfacebook.user.decorators.parse_signed_request`

Injects a decrypted signed_request into your view function.
It can be `None`.
A signed request is good for a lot of things, of which can be found at http://developers.facebook.com/docs/authentication/signed_request/

Example:

	from django.conf import settings
    from django.core.urlresolvers import reverse
    from django.views.generic.simple import direct_to_template
    
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
        >>> print signed_request # Example signed request
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
			
### graph_from_cookies :: `ezfacebook.user.decorators.graph_from_cookies`

Injects a `FacebookGraphAPI` (or specified subclass) into your view function.
It can be `None`.
`FacebookGraphAPI` is great for making requests to facebook.com, those requests can be found at https://developers.facebook.com/docs/reference/api/

Example:

	from django.conf import settings
    from django.core.urlresolvers import reverse
    from django.views.generic.simple import direct_to_template
    
    from ezfacebook.context.templatetags import absurl
    from ezfacebook.user import decorators

    @decorators.graph_from_cookies('my_first_fb_app') # or graph_from_cookies(settings.FACEBOOK_SETTINGS.my_first_fb_app)
    def post_to_wall(request, graph, *args, **kwargs):
        
        image_url = absolute_url("%simages/fb_image.png" % settings.MEDIA_URL, request=request)
        link = absolute_url(reverse('myviews.index', request=request))
        
        graph.put_object("me", "feed", picture=image_url, name='Whatsup', description='Hello', link=link, caption='Pow Mow Local')
        
        return direct_to_template(request, 'success.html')
			
## Middleware :: `ezfacebook.user.middleware`

This middleware is used to apply the above decorators to all view functions.

### FacebookRequestMiddleware :: `ezfacebook.user.middleware.FacebookRequestMiddleware`

Put signed_request and graph in the request for each facebook app.
Like this: `request.ezfb.my_app_name.graph` or `request.ezfb.my_app_name.signed_request`

This cleans up your code so that decorators are not everywhere. However, it does add a little bit of inefficiency when
your apps are not always being checked against.  Decorators are ugly, but recommended.

Example:

    from django.views.generic.simple import direct_to_template 

	from myapp import models
    
    def my_view(request):
    	"""
    	An example demonstrating some possibilities of FacebookRequestMiddleware.
    	"""
    	
    	# Get or create a FacebookUser from the graph, if present.
    
    	graph = request.ezfb.my_first_fb_app.graph
        if graph:
            fbuser = models.FacebookUser.objects.get_or_create(facebook_guid=graph.facebook_guid)
        else:
        	fbuser = None
        return direct_to_template(request, 'my_first_fb_app/index-liked.html', {'fbuser': fbuser})
        
        # OR!
        # Show the index page, a different version if they like my_second_fb_app
        
        signed_request = request.ezfb.my_second_fb_app.signed_request
        if signed_request:
        	page_data = signed_request.get('page', None)
        	if page_data and page_data.get('liked', False):
        		return direct_to_template(request, 'my_second_fb_app/index-liked.html')
        return direct_to_template(request, 'my_second_fb_app/index-unliked.html')

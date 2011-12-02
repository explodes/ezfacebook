# EZ-Facebook Django Utils (for django 1.3+)

* Under Development, not for production *


The purpose of this package is to make facebook integration with:
- Web sites
- Page Tabs
- Facebook App Pages

Included in the suite are:
- Easy to use facebook settings with debug settings
- Facebook script template tags
- P3P Cookie middleware to enable the use of cookies in your iframes
- Facebook Settings context processors
- Facebook Channel URL context variable and view
- Absolute Url template tag, minds current protocol. Useful for posting links and images.
- View decorators that extract information from requests, like signed_request, and facebook graph api. 

For installation please see:

(See ezfacebook/example_settings.py and ezfacebook/example_urls.py)

# Installation

## Settings :: example settings.py

TEMPLATE_CONTEXT_PROCESSORS = (
    'ezfacebook.context.context_processors.facebook', # ezfacebook.context: Requirement
)

MIDDLEWARE_CLASSES = (
    'ezfacebook.helpers.middleware.IEIFrameApplicationMiddleware' # ezfacebook.helpers: Optional
)

INSTALLED_APPS = (
    'django.contrib.sites', # ezfacebook.context: Requirement
    'ezfacebook.context', # ezfacebook.context: Optional, allows templatetags absurl
)

class FACEBOOK_SETTINGS: # ezfacebook.user, ezfacebook.context: Requirement

    class my_first_fb_app:
        app_id = '00000000000000',
        secret = 'abcdef0123456789',
        scope = 'email,publish_stream,offline_access'

        debug_signed_request = {'id': 23840238402834} # 
        debug_guid = 23840238402834
        debug_token = 'AAAAAAAAAbbbbbbbbbbccccdefffffffffffffffffffetc'

    class my_second_fb_app:
        app_id = '11111111111111',
        secret = '9876543210abcdef',
        scope = ''

        debug_signed_request = False
        debug_guid = False
        debug_token = False
        
## URLS :: example urls.py

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^fb/', include('ezfacebook.context.urls')),
)


# Packages

## Context :: ezfacebook.context, installable app.

This packages comes with the following features:

- Template Tags
- Context Processors
- channel.html view

### Template Tags

This package must be installed in your application to use template tags.

#### absurl

##### absolute_url

Builds an absolute URL for the given path.
If request is provided, the protocol (http or https) is determined from the request, otherwise http is used.

Example:

	{% load absurl %}
	
	{{ obj.image.url|absolute_url }}
	{{ obj.image.url|absolute_url:request }}

#### fb_script

These template tags render the HTML required to the Facebook Javascript SDK.

##### fb_script

Renders the Facebook Javascript SDK script required for facebook connectivity.

Example:

    {% load fb_script %}
    
    {% fb_script 'my_first_fb_app' %}
    
    {% fb_script 'my_first_fb_app' use_share=True %} {# Also loads FB.Share javascript #}
    
    {# See http://bugs.developers.facebook.net/show_bug.cgi?id=19042 #}
    {% fb_script 'my_first_fb_app' fix_19042=True %} 
    
    {# See http://bugs.developers.facebook.net/show_bug.cgi?id=20168= #}
    {% fb_script 'my_first_fb_app' fix_20168=True %} 

##### fb_script_with_canvas

Renders the Facebook Javascript SDK script required for facebook connectivity and sets the Facebook Canvas size.
    
Example:
    
    {% load fb_script %}
    
    {% fb_script_with_canvas 'my_first_fb_app' canvas_height=2000 canvas_width=500 %} {# 500 is the recommended width for a Page Tab #}
    
    {% fb_script_with_canvas 'my_first_fb_app' canvas_height=2000 canvas_width=500 use_share=True %} {# 500 is the recommended width for a Page Tab #} {# Also loads FB.Share javascript #}
    
    {# See http://bugs.developers.facebook.net/show_bug.cgi?id=19042 #}
    {% fb_script_with_canvas 'my_first_fb_app' canvas_height=2000 canvas_width=500 fix_19042=True %} 
    
    {# See http://bugs.developers.facebook.net/show_bug.cgi?id=20168= #}
    {% fb_script_with_canvas 'my_first_fb_app' canvas_height=2000 canvas_width=500 fix_20168=True %} 
	
## Helpers
	
### Middleware

This package has middleware to help out your application.


#### IEIFrameApplicationMiddleware

It is not necessary to install this package as an app to use this middleware.

Sets response headers (P3P policy) to allow IE 7-8 to use cookies inside of an iframe.
This is useful for websites that are put in iframes on facebook, such as page tabs and facebook apps.

To use it, simply add ezfacebook.helpers.middleware.IEIFrameApplicationMiddleware to MIDDLEWARE_CLASSES in your settings file. 

## Lib

### adapter

#### parse_signed_request

#### parse_cookies

#### get_graph_from_cookies

#### FacebookGraphAPI

## User

This package is responsible for extracting user information from a request.
Currently this is done with the use of decorators.
In the future, some kind of middleware may be used.

### Decorators

These decorators are used on view functions, they will inject the results as the parameter after request.
Any other arguments or keyword arguments are still sent to the view.

#### parseSignedRequest

Injects a decrypted signed_request into your view function.
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
			
#### graphFromCookies

Injects a FacebookGraphAPI into your view function.
It can be None.
FacebookGraphAPI is great for making requests to facebook.com, those requests can be found at https://developers.facebook.com/docs/reference/api/

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

			
		
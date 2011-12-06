
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
        # Disable debugging by omitting the settings or by setting them to false

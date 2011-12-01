

TEMPLATE_CONTEXT_PROCESSORS = (
    'ezfacebook.context.context_processors.facebook', # Puts FACEBOOK_SETTINGS and FACEBOOK_CHANNEL_URL in template context
)

MIDDLEWARE_CLASSES = (
    'ezfacebook.helpers.middleware.IEIFrameApplicationMiddleware' # Required for IE in iframe environments (example Page Tab) if sessions are to work.
)

INSTALLED_APPS = (
    # Nothing special needs to be installed to use this package
)

class FACEBOOK_SETTINGS:

    class my_first_fb_app:
        app_id = '00000000000000',
        secret = 'abcdef0123456789',
        scope = 'email,publish_stream,offline_access'
        # Enable debug mode for ezfacebook.user.decorators.parse_signed_request
        debug_signed_request = {'id': 23840238402834}
        # Enable debug mode for ezfacebook.user.decorators.graph_from_cookies
        debug_guid = 23840238402834
        # Enable debug mode for ezfacebook.user.decorators.graph_from_cookies
        debug_token = 'AAAAAAAAAbbbbbbbbbbccccdefffffffffffffffffffetc'

    class my_second_fb_app:
        app_id = '11111111111111',
        secret = '9876543210abcdef',
        scope = ''
        # Disable debug mode for ezfacebook.user.decorators.parse_signed_request
        debug_signed_request = False
        # Disable debug mode for ezfacebook.user.decorators.graph_from_cookies
        debug_guid = False
        # Disable debug mode for ezfacebook.user.decorators.graph_from_cookies
        debug_token = False

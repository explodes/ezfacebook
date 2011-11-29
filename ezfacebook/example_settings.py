

TEMPLATE_CONTEXT_PROCESSORS = (
    'ezfacebook.context.context_processors.facebook', # Puts FACEBOOK_SETTINGS and FACEBOOK_CHANNEL_URL in template context
)

MIDDLEWARE_CLASSES = (
    'ezfacebook.helpers.middleware.IEIFrameApplicationMiddleware' # Required for IE in iframe environments (example Page Tab) if sessions are to work.
)

INSTALLED_APPS = (
    # Nothing special needs to be installed to use this package
)

FACEBOOK_SETTINGS = {
    'my_first_app' : {
        'app_id' : '00000000000000',
        'secret' : 'abcdef0123456789',
        'scope'  : 'email,publish_stream,offline_access'
    },
    'my_second_app' : {
        'app_id' : '11111111111111',
        'secret' : '9876543210abcdef',
        'scope'  : ''
    },
}

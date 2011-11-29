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
	
## Helpers

This 'app' has middleware to help out your application.

	MIDDLEWARE_CLASSES = (
		'ezfacebook.helpers.middleware.IEIFrameApplicationMiddleware'
	)
	
### IEIFrameApplicationMiddleware

Sets response headers (P3P policy) to allow IE 7-8 to use cookies inside of an iframe.
This is useful for websites that are put in iframes on facebook, such as page tabs and facebook apps.

## User

Under development, the idea here is to use decorators to pass extra variables into views, such as a facebook_user, whether or not they like an app, and their current access rights.

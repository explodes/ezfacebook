from django.conf import settings

def app_settings(app_name_or_settings):
    if isinstance(app_name_or_settings, (str, unicode)):
        return getattr(settings.FACEBOOK_SETTINGS, app_name_or_settings)
    else:
        return app_name_or_settings

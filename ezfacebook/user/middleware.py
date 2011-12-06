from django.conf import settings

from . import decorators

class FacebookRequestMiddleware(object):
    """
    Put signed_request and graph in the request for each facebook app.
    
    Example:
    
    def my_view(request):
        if request.ezfb.my_first_app.graph:
            ''' do something with graph, or graph.facebook_guid '''
        if request.ezfb.my_first_app.signed_request and request.ezfb.my_first_app.signed_request.get('page', {}).get('liked', False):
            ''' The user likes this page, do something special! (Note signed_request is only available on the index page. '''

    """
    def process_request(self, request):
        """
        Add 'ezfb' to the request.
        """
        request.ezfb = self._clone_settings(request)

    def _clone_settings(self, request):
        """
        For each FACEBOOK_SETTINGS, append signed_request and graph to a class with the settings name holding the information
        """
        class ezfb:
            pass

        for settings_class in self._iter_facebook_settings():
            class settings:
                signed_request = self._get_signed_request(request, settings_class)
                graph = self._get_graph_from_cookies(request, settings_class)
            setattr(ezfb, settings_class.__name__, settings)
        return ezfb

    def _iter_facebook_settings(self):
        """
        Generator that iterates through each FACEBOOK_SETTINGS class
        """
        fbsettings = settings.FACEBOOK_SETTINGS
        for prop_name in dir(fbsettings):
            settings_class = getattr(fbsettings, prop_name)
            if hasattr(settings_class, 'app_id'):
                yield settings_class

    def _get_signed_request(self, request, settings_class):
        """
        Get the signed request from the request using the given Facebook settings class.
        """
        return decorators._parse_signed_request_method(settings_class)(request, settings_class)

    def _get_graph_from_cookies(self, request, settings_class):
        """
        Get the graph api from the request using the given Facebook settings class.
        """
        return decorators._graph_from_cookies_method(settings_class)(request, settings_class)

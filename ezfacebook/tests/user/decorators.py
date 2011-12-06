import unittest

from ...user import decorators

class Decorators(unittest.TestCase):

    def test_parse_signed_request_debug_mode(self):
        ''' This tests parse_signed_request top to bottom, taking the debug path. '''
        foo_data = {'abc': 123}

        class settings:
            debug_signed_request = foo_data

        @decorators.parse_signed_request(settings)
        def f(request, signed_request, *args, **kwargs):
            return signed_request, args[0], kwargs.get('kwarg', None)

        signed_request, arg, kwarg = f(None, 'abc', kwarg=True)

        self.assertEqual(signed_request, foo_data, "Debug data not returned")
        self.assertEqual(arg, 'abc', "arg was faltered")
        self.assertEqual(kwarg, True, "kwarg was faltered")

    def test__parse_signed_request(self):
        class request:
            POST = {"signed_request" : "byoFrT28ZWEuGUI_leakGi4LOduB9xMVvldo_UYqt3A.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImV4cGlyZXMiOjEzMjI2ODMyMDAsImlzc3VlZF9hdCI6MTMyMjY3NjU5OCwib2F1dGhfdG9rZW4iOiJBQUFDYndFZ2pTcGtCQUpCVERHbjhRaExsU2Nrb0FvOVhWa0dxdXRxN3pkYXF2RFBaQmdwVUg3Qk5BN0tYZDl3M2t5V1ZGTFpBWkFsajhhZTVoUFBNdWsxSnNreUtpWGxUd2JoTVdQYjJ3WkRaRCIsInBhZ2UiOnsiaWQiOiI0NjMyNjU0MDI4NyIsImxpa2VkIjp0cnVlLCJhZG1pbiI6ZmFsc2V9LCJ1c2VyIjp7ImNvdW50cnkiOiJ1cyIsImxvY2FsZSI6ImVuX1VTIiwiYWdlIjp7Im1pbiI6MjF9fSwidXNlcl9pZCI6IjE5MTkwMDA5MSJ9"}

        class settings:
            secret = '49f7804b19a9a373dc77e2b4dedc733b'

        signed_request = decorators._parse_signed_request(request, settings)

        self.assertNotEqual(signed_request, None, "Expected a signed_request")
        self.assertEqual(signed_request.get('page', {}).get('id', None), u'46326540287', "Something went wrong when decrypting the signed_request")

    def test_graph_from_cookies_debug_mode(self):
        ''' This tests graph_from_cookies top to bottom, taking the debug path '''
        guid = 123
        token = 'abc'

        class settings:
            debug_guid = guid
            debug_token = token

        @decorators.graph_from_cookies(settings)
        def f(request, graph, *args, **kwargs):
            return graph, args[0], kwargs.get('kwarg', None)

        graph, arg, kwarg = f(None, 'abc', kwarg=True)

        self.assertNotEqual(graph, None, "Graph is None")
        self.assertEqual(graph.facebook_guid, guid, "Graph guid doesnt match expected value")
        self.assertEqual(graph.access_token, token, "Graph token doesnt match expected value")
        self.assertEqual(arg, 'abc', "arg was faltered")
        self.assertEqual(kwarg, True, "kwarg was faltered")

    def test_parse_signed_request_valid_this_test_will_fail_unless_you_fill_in_your_info(self):
        from django.conf import settings
        class fbsettings:
            class some_app:
                secret = '' # TODO: Fill this in with your secret
                debug_signed_request = False
        settings.FACEBOOK_SETTINGS = fbsettings
        @decorators.parse_signed_request('some_app')
        def my_view(request, signed_request):
            return signed_request
        class request:
            def __init__(self, signed_request):
                self.POST = dict(signed_request=signed_request)
        valid_signed_request = '' # TODO: Fill this in with a valid signed_request
        self.assertNotEqual(my_view(request(valid_signed_request)), None)

    def test_parse_signed_request_invalid(self):
        from django.conf import settings
        class fbsettings:
            class some_app:
                secret = ''
                debug_signed_request = False
        settings.FACEBOOK_SETTINGS = fbsettings
        @decorators.parse_signed_request('some_app')
        def my_view(request, signed_request):
            return signed_request
        class request:
            def __init__(self, signed_request):
                self.POST = dict(signed_request=signed_request)
        self.assertEqual(my_view(request('abc')), None)
        


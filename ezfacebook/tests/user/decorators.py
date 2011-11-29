import unittest

from ...user import decorators

class Decorators(unittest.TestCase):

    def test_parse_signed_request_debug_mode(self):
        foo_data = {'abc': 123}

        @decorators.parseSignedRequest('test', use_debug=True, debug_data=foo_data)
        def f(request, signed_request, *args, **kwargs):
            return signed_request

        self.assertEqual(f(None), foo_data, "Debug data not returned")

    def test_graph_from_cookies_debug_mode(self):
        guid = 123
        token = 'abc'

        @decorators.graphFromCookies('test', use_debug=True, debug_user_id=guid, debug_access_token=token)
        def f(request, graph, *args, **kwargs):
            return graph

        graph = f(None)

        self.assertNotEqual(graph, None, "Graph is None")
        self.assertEqual(graph.facebook_guid, guid, "Graph guid doesnt match expected value")
        self.assertEqual(graph.access_token, token, "Graph token doesnt match expected value")




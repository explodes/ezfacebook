import unittest

from ...lib import adapter

class TestGraphAPI(adapter.FacebookGraphAPI):
    pass

class Adapter(unittest.TestCase):

    def test__getFacebookGraphAPIClass(self):
        from django.conf import settings

        settings.FACEBOOK_GRAPH_API_CLASS = 'ezfacebook.tests.lib.adapter.TestGraphAPI'

        self.assertEqual(TestGraphAPI, adapter._getFacebookGraphAPIClass())

        delattr(settings, 'FACEBOOK_GRAPH_API_CLASS')



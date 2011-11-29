import unittest

from ...helpers import middleware

class Middleware(unittest.TestCase):

    def test_IEIFrameApplicationMiddleware(self):

        mw = middleware.IEIFrameApplicationMiddleware()

        request = {}
        response = {}

        response = mw.process_response(request, response)

        self.assertNotEqual(response.get('P3P', None), None, "P3P Header not set.")




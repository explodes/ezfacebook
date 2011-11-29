
class IEIFrameApplicationMiddleware(object):
    """
    Required for IE in iframe environments (example Page Tab) if sessions are to work.
    """
    def process_response(self, request, response):
        response = self._add_p3p_policy(response)
        return response

    def _add_p3p_policy(self, response):
        ''' This policy allows iframes to store cookies in IE 7 & 8 '''
        response['P3P'] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'
        return response

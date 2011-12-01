
class IEIFrameApplicationMiddleware(object):
    """
    Required for IE in iframe environments (example Page Tab) if sessions are to work.
    """
    def process_response(self, request, response):
        """
        Perform all processing to let this response save cookies in an IFrame
        """
        response = self._add_p3p_policy(response)
        return response

    def _add_p3p_policy(self, response):
        """
        This policy allows iframes to store cookies in some version of IE
        """
        response['P3P'] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'
        return response

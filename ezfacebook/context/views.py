from django import http

CHANNEL_HTML = '''<script type="text/javascript" src="//connect.facebook.net/en_US/all.js"></script>'''
EXPIRES_FOREVER = 'Sun, 17-Jan-2038 19:14:07 GMT'

def channel(request):
    """
    Renders out "channel.html" which is important for all.js to work in some browsers (IE...)
    """
    response = http.HttpResponse(CHANNEL_HTML)
    response['Expires'] = EXPIRES_FOREVER
    return response

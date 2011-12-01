from django import http

def channel(request):
    """
    Renders out "channel.html" which is important for all.js to work in some browsers (IE...)
    """
    return http.HttpResponse('<script type="text/javascript" src="//connect.facebook.net/en_US/all.js"></script>')

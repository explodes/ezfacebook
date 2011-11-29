from django import http

def channel(request):
    return http.HttpResponse('<script type="text/javascript" src="//connect.facebook.net/en_US/all.js"></script>')

from django import template
from django.contrib.sites.models import Site
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter
@stringfilter
def absolute_url(path, request=None, strip_protocol=False):
    """
    Builds an absolute URL for the given path.
    If request is provided, i.e.
    {{ obj.image.url|absolute_url:request }}
    The protocol (http or https) is determined from the request,
    otherwise http is used.
    
    If called as a function, i.e.
    absoulute_url(reverse('myview.view'), request=request, strip_protocol=True)
    you can specify to use //myhost.com/mypath/ by stripping the protocol.
    Good for javascript links, such as channel.html
    """
    if path:
        protocol = ''
        if not strip_protocol:
            protocol = 'http:'
            if request:
                protocol = 'https:' if request.is_secure() else 'http:'
        host = Site.objects.get_current().domain
        if path[0] != '/':
            path = '/%s' % path
        return '%s//%s%s' % (protocol, host, path)

absolute_url.is_safe = True

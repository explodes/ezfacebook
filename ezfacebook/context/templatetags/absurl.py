from django import template
from django.contrib.sites.models import Site
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def absolute_url(path, request=None):
    """
    Builds an absolute URL for the given path.
    If request is provided, i.e.
    {{ obj.image.url|absolute_url:request }}
    The protocol (http or https) is determined from the request,
    otherwise http is used.
    """
    if path:
        protocol = 'http:'
        if request:
            protocol = 'https:' if request.is_secure() else 'http:'
        host = Site.objects.get_current().domain
        if path[0] != '/':
            path = '/%s' % path
        return '%s//%s%s' % (protocol, host, path)

absolute_url.is_safe = True

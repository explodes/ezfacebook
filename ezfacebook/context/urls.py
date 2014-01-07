"""

URLs for the context "app":

facebook-channel-url: URL to "channel.html" i.e. //mysitedomain.com/facebookchannel/

"""

try:
    from django.conf.urls.defaults import patterns, url
except ImportError:
    # Django 1.6 removes the defaults module.
    # See https://docs.djangoproject.com/en/1.6/internals/deprecation/#id1
    from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url('^facebookchannel/$', views.channel, name="facebook-channel-url"),
)

"""

URLs for the context "app":

facebook-channel-url: URL to "channel.html" i.e. //mysitedomain.com/facebookchannel/

"""

from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url('^facebookchannel/$', views.channel, name="facebook-channel-url"),
)

from django.conf.urls.defaults import patterns, url

from . import views

urlpatterns = patterns('',
    url('^facebookchannel/$', views.channel, name='facebook-channel-url'),
)

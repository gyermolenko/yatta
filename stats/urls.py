from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.channel_list, name='channel_list'),
    url(r'^add/$', views.channel_add, name='channel_add'),
    url(r'^(?P<pk>[0-9]+)/videos/$', views.channel_videos, name='channel_videos'),
    url(r'^video/(?P<pk>[0-9]+)/$', views.video_info, name='video_info'),
]


from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.channel_list, name='channel_list'),
    url(r'^add/$', views.channel_add, name='channel_add'),
    url(r'^(?P<pk>[0-9]+)/info/$', views.channel_info, name='channel_info'),
]


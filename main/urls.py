from django.conf.urls import url, include
from django.contrib import admin

from . import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('channel.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/ajax_validate_username/$', views.ajax_validate_username, name='ajax_validate_username'),
]

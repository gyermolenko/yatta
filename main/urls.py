from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^menu/', views.main_menu, name='main_menu'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^', include('channel.urls')),
]

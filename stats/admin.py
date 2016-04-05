from django.contrib import admin
from .models import Channel, Video


class ChannelAdmin(admin.ModelAdmin):
    list_display = ('username', 'playlist_id')

admin.site.register(Channel)
admin.site.register(Video)

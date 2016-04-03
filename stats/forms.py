from django import forms

from .models import Channel


class ChannelForm(forms.ModelForm):

    class Meta:
        model = Channel
        fields = ('username', 'playlist_id')

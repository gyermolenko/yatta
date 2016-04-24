from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
# from django.core.validators import validate_slug

from .models import Channel


def validate_adding_multiple_channels(value):
    if value.startswith('<'):
        raise ValidationError(
            _("Can't start from '<'"),
        )
    if ' ' in value:
        raise ValidationError(
            _('No spaces'),
        )


class AddOneChannelForm(forms.ModelForm):

    class Meta:
        model = Channel
        fields = ('username',)


class AddMultipleChannelsForm(forms.Form):
    usernames = forms.CharField(label='',
                                widget=forms.Textarea,
                                initial='<channel one>\n<channel two>\n<...>',
                                validators=[validate_adding_multiple_channels])

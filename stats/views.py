from django.shortcuts import render, redirect
from .models import Channel
from .forms import ChannelForm

from .yatta import get_playlist_id


def channel_list(request):
    channels = Channel.objects.all()
    return render(request, 'stats/channel_list.html', {'channels': channels})


def channel_add(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            new_channel = form.save(commit=False)
            new_channel.playlist_id = get_playlist_id(new_channel.username)
            new_channel.save()
            return redirect('channel_list')
    else:
        form = ChannelForm()
    return render(request, 'stats/channel_add.html', {'form': form})


def channel_info(request, pk):
    return render(request, 'stats/channel_info.html', {'n': pk})


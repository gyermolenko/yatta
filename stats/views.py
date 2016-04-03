from django.shortcuts import render, redirect
from .models import Channel
from .forms import ChannelForm


def channel_list(request):
    channels = Channel.objects.all()
    return render(request, 'stats/channel_list.html', {'channels': channels})


def channel_add(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            new_channel = form.save()
            return redirect('channel_list')
    else:
        form = ChannelForm()
    return render(request, 'stats/channel_add.html', {'form': form})

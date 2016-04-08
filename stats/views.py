from django.shortcuts import render, redirect
from .models import Channel, Video
from .forms import ChannelForm

from .yatta import get_playlist_id, channel_statistics, \
                   get_videos_meta_info, get_video_views_and_likes


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
    videos = Video.objects.filter(channel_id=pk)

    if request.method == 'POST':
        playlist_id = Channel.objects.get(pk=pk).playlist_id
        channel_videos_meta = get_videos_meta_info(playlist_id)

        new_videos = []
        ids_from_db = [vid.video_id for vid in videos]
        for vid in channel_videos_meta:
            if vid['video_id'] not in ids_from_db:
                v = Video(video_id=vid['video_id'], title=vid['title'], channel_id=pk)
                new_videos.append(v)
        Video.objects.bulk_create(new_videos)

        return redirect('channel_info', pk=pk)

    return render(request, 'stats/channel_info.html', {'videos': videos})


from django.shortcuts import render, redirect
from django.db.models import Max

from .models import Channel, Video, ChannelStatistics, VideoStatistics
from .forms import ChannelForm

from .yatta import get_playlist_id, channel_statistics, \
                   get_videos_meta_info, get_video_views_and_likes


def channel_list(request):
    latest_stats_ids = Channel.objects.annotate(latest_stats_id=Max('statistics__id')) \
                                      .values_list('latest_stats_id', flat=True)
    statistics = ChannelStatistics.objects.filter(id__in=latest_stats_ids)

    if request.method == 'POST':
        channels = Channel.objects.all()
        new_stats = []
        for channel in channels:
            stats = channel_statistics(channel.username)

            cs = ChannelStatistics(
                total_view_count=stats['viewCount'],
                subscriber_count=stats['subscriberCount'],
                video_count=stats['videoCount'],
                channel_id=channel.id,
            )
            new_stats.append(cs)

        ChannelStatistics.objects.bulk_create(new_stats)

    return render(request,
                  'stats/channel_list.html',
                  {'statistics': statistics})


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
    return render(request,
                  'stats/channel_add.html',
                  {'form': form})


def channel_videos(request, pk):
    videos = Video.objects.filter(channel_id=pk).order_by('-published_at')
    channel = Channel.objects.get(pk=pk)

    if request.method == 'POST':
        playlist_id = Channel.objects.get(pk=pk).playlist_id
        channel_videos_meta = get_videos_meta_info(playlist_id)

        new_videos = []
        ids_from_db = [vid.video_id for vid in videos]
        for vid in channel_videos_meta:
            if vid['video_id'] not in ids_from_db:
                v = Video(
                    video_id=vid['video_id'],
                    title=vid['title'],
                    published_at=vid['published_at'],
                    channel_id=pk
                )
                new_videos.append(v)
        Video.objects.bulk_create(new_videos)

        return redirect('channel_videos', pk=pk)

    return render(request,
                  'stats/channel_videos.html',
                  {'videos': videos, 'channel': channel.username})


def video_info(request, pk):
    video = Video.objects.get(pk=pk)
    video_stats = VideoStatistics.objects.filter(video_id=pk)

    if request.method == 'POST':
        views, likes = get_video_views_and_likes(video.video_id)
        vs = VideoStatistics(view_count=views, like_count=likes, video=video)
        vs.save()

        return redirect('video_info', pk=pk)

    return render(request,
                  'stats/video_info.html',
                  {'video': video, 'video_stats': video_stats})

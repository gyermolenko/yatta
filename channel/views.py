from datetime import datetime as dt

from django.shortcuts import render, redirect
from django.db.models import Max

from .models import Channel, Video, ChannelStats, VideoStats
from .forms import AddOneChannelForm, AddMultipleChannelsForm

from .yatta import get_playlist_id, get_channel_statistics, \
                   get_videos_meta_info, get_video_views_and_likes


def channel_list(request):
    latest_stats_ids = Channel.objects.annotate(latest_stats_id=Max('statistics__id')) \
                                      .values_list('latest_stats_id', flat=True)
    statistics = ChannelStats.objects.filter(id__in=latest_stats_ids)

    if request.method == 'POST':
        channels = Channel.objects.all()
        new_stats = []
        for channel in channels:
            stats = get_channel_statistics(channel.username)

            cs = ChannelStats(
                total_view_count=stats['viewCount'],
                subscriber_count=stats['subscriberCount'],
                video_count=stats['videoCount'],
                channel_id=channel.id,
            )
            new_stats.append(cs)

        ChannelStats.objects.bulk_create(new_stats)

    return render(request,
                  'channel/channel_list.html',
                  {'statistics': statistics})


def channel_add(request):
    if request.method == 'POST':
        form = AddOneChannelForm(request.POST)
        if form.is_valid():
            new_channel = form.save(commit=False)
            new_channel.playlist_id = get_playlist_id(new_channel.username)
            new_channel.save()

            _gather_channel_statistics(new_channel)
            _gather_channel_videos_meta_info(new_channel)
            _gather_channel_videos_views_and_likes(new_channel)

            return redirect('channel_list')
    else:
        form = AddOneChannelForm()

    return render(request,
                  'channel/channel_add.html',
                  {'form': form})


def channel_add_multiple(request):
    if request.method == 'POST':
        form = AddMultipleChannelsForm(request.POST)
        present_channelnames = [cn.username for cn in Channel.objects.all()]

        if form.is_valid():
            cleaned_channelnames = form.cleaned_data['usernames']
            names_to_add = [cc for cc in cleaned_channelnames.split() if cc not in present_channelnames]
            channels_to_add = [Channel(username=name, playlist_id=get_playlist_id(name)) for name in names_to_add]
            # Channel.objects.bulk_create(channels_to_add)

            for new_channel in channels_to_add:
                new_channel.save()
                _gather_channel_statistics(new_channel)
                _gather_channel_videos_meta_info(new_channel)
                _gather_channel_videos_views_and_likes(new_channel)

            return redirect('channel_list')

    else:
        form = AddMultipleChannelsForm()

    return render(request,
                  'channel/channel_add_multiple.html',
                  {'form': form})


def channel_videos(request, pk):
    channel = Channel.objects.get(pk=pk)

    latest_stats_ids = Video.objects.filter(channel=pk).annotate(latest_stats_id=Max('statistics__id')) \
                                                       .values_list('latest_stats_id', flat=True)
    video_stats = VideoStats.objects.filter(id__in=latest_stats_ids).order_by('video__published_at')

    # highcharts
    series = []
    rec = {}
    rec["name"] = "Channel name"
    rec["data"] = []
    for stat in video_stats:
        published_at = dt.timestamp(stat.video.published_at) * 1000
        view_count = stat.view_count
        rec["data"].append([published_at, view_count])
    series.append(rec)

    # d3 charts
    d3data = []
    for stat in video_stats:
        published_at = dt.timestamp(stat.video.published_at) * 1000
        view_count = stat.view_count
        like_count = stat.like_count
        d3data.append([published_at, view_count, like_count])

    if request.method == 'POST':
        playlist_id = channel.playlist_id
        channel_videos_meta = get_videos_meta_info(playlist_id)

        # ids_from_db = [stat.video.video_id for stat in video_stats]
        videos = Video.objects.filter(channel_id=pk)
        ids_from_db = [vid.video_id for vid in videos]
        new_videos = []
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
                  'channel/channel_videos.html',
                  {
                      'channelname': channel.username,
                      'video_stats': video_stats,
                      'series': series,
                      'd3data': d3data,
                  })


def video_stats(request, pk):
    video = Video.objects.get(pk=pk)
    video_stats = VideoStats.objects.filter(video_id=pk)

    if request.method == 'POST':
        views, likes = get_video_views_and_likes(video.video_id)
        vs = VideoStats(
            view_count=views,
            like_count=likes,
            video=video,
            channel=video.channel
        )
        vs.save()

        return redirect('video_stats', pk=pk)

    return render(request,
                  'channel/video_stats.html',
                  {'video': video, 'video_stats': video_stats})


# def channel_chart(request, pk):
#     latest_stats_ids = Video.objects.filter(channel=pk).annotate(latest_stats_id=Max('statistics__id')) \
#                                                        .values_list('latest_stats_id', flat=True)
#     statistics = VideoStats.objects.filter(id__in=latest_stats_ids).order_by('video__published_at')

#     series = []
#     rec = {}
#     rec["name"] = "Channel name"
#     rec["data"] = []
#     for stat in statistics:
#         published_at = dt.timestamp(stat.video.published_at)*1000
#         view_count = stat.view_count
#         rec["data"].append([published_at, view_count])
#     series.append(rec)

#     return render(request,
#                   'channel/channel_chart.html',
#                   {'statistics': statistics, 'series': series})



def _gather_channel_statistics(new_channel):
    stats = get_channel_statistics(new_channel.username)
    cs = ChannelStats(
        total_view_count=stats['viewCount'],
        subscriber_count=stats['subscriberCount'],
        video_count=stats['videoCount'],
        channel_id=new_channel.id,
    )
    cs.save()


def _gather_channel_videos_meta_info(new_channel):
    channel_videos_meta = get_videos_meta_info(new_channel.playlist_id)
    new_videos = []
    for video_meta in channel_videos_meta:
        v = Video(
            video_id=video_meta['video_id'],
            title=video_meta['title'],
            published_at=video_meta['published_at'],
            channel_id=new_channel.id
        )
        new_videos.append(v)
    Video.objects.bulk_create(new_videos)


def _gather_channel_videos_views_and_likes(new_channel):
    videos = new_channel.videos.all()
    new_video_views_likes_info = []
    for video in videos:
        views, likes = get_video_views_and_likes(video.video_id)
        vs = VideoStats(
            view_count=views,
            like_count=likes,
            video=video,
            channel=video.channel
        )
        new_video_views_likes_info.append(vs)
    VideoStats.objects.bulk_create(new_video_views_likes_info)

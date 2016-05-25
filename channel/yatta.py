import requests
from main.secrets import API_KEY


BASE_URL = 'https://www.googleapis.com/youtube/'
api_version = 'v3'
username = 'McBacon1337'

# https://developers.google.com/youtube/v3/docs/channels/list#try-it
def get_playlist_id(username):
    part = 'contentDetails'
    URL = BASE_URL + api_version + '/channels?' \
        'part=%(part)s' \
        '&forUsername=%(username)s' \
        '&key=%(API_KEY)s'

    composed_url =  URL % {'part': part,
                           'username': username,
                           'API_KEY': API_KEY}

    resp = requests.get(composed_url)
    playlist_id = resp.json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    return playlist_id


def get_channel_statistics(username):
    part = 'statistics'
    URL = BASE_URL + api_version + '/channels?' \
        'part=%(part)s' \
        '&forUsername=%(username)s' \
        '&key=%(API_KEY)s'

    composed_url = URL % {'part': part,
                          'username': username,
                          'API_KEY': API_KEY}

    resp = requests.get(composed_url)
    stats = resp.json()['items'][0]['statistics']

    channel_stats = {}
    channel_stats['viewCount'] = stats['viewCount']
    channel_stats['subscriberCount'] = stats['subscriberCount']
    channel_stats['videoCount'] = stats['videoCount']

    return channel_stats


# https://developers.google.com/youtube/v3/docs/playlistItems/list
def get_videos_meta_info(playlistId):
    part = 'snippet'
    fields = 'items/snippet'
    URL = BASE_URL + api_version + '/playlistItems?' \
        'part=%(part)s' \
        '&fields=%(fields)s' \
        '&playlistId=%(playlistId)s' \
        '&key=%(API_KEY)s' \
        '&maxResults=50'

    composed_url = URL % {'part': part,
                          'fields': fields,
                          'playlistId': playlistId,
                          'API_KEY': API_KEY}

    resp = requests.get(composed_url)
    json_items = resp.json()['items']

    video_meta_info = []
    for item in json_items:
        v = {}
        v['title'] = item['snippet']['title']
        v['video_id'] = item['snippet']['resourceId']['videoId']
        v['published_at'] = item['snippet']['publishedAt']
        video_meta_info.append(v)

    return video_meta_info


# https://developers.google.com/youtube/v3/docs/videos/list#try-it
def get_video_views_and_likes(videoId):
    part = 'statistics'
    URL = BASE_URL + api_version + '/videos?' \
        'part=%(part)s' \
        '&id=%(videoId)s' \
        '&key=%(API_KEY)s'

    composed_url = URL % {'part': part,
                          'videoId': videoId,
                          'API_KEY': API_KEY}

    resp = requests.get(composed_url)
    json_items = resp.json()['items']
    stats = json_items[0]['statistics']

    return stats['viewCount'], stats['likeCount']


if __name__ == "__main__":
    playlistId = get_playlist_id(username)
    # playlistId = 'UUqJ-Xo29CKyLTjn6z2XwYAw'
    # his_last_vid_id = 'EFvbN3K6EA8'
    channel_stats = get_channel_statistics(username)

    # published_at '2016-03-09T13:21:32.000Z'
    # videos = get_videos_meta_info(playlistId)
    # for v in videos:
    #     v['views'], v['likes'] = get_video_views_and_likes(v['videoId'])


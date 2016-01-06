import requests
from collections import namedtuple
from secrets import API_KEY


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
    return resp.json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']


# https://developers.google.com/youtube/v3/docs/playlistItems/list
def get_video_title_and_id(playlistId):
    part = 'snippet'
    URL = BASE_URL + api_version + '/playlistItems?' \
        'part=%(part)s' \
        '&playlistId=%(playlistId)s' \
        '&key=%(API_KEY)s' \
        '&maxResults=50'

    composed_url = URL % {'part': part,
                          'playlistId': playlistId,
                          'API_KEY': API_KEY}

    resp = requests.get(composed_url)
    json_items = resp.json()['items']

    videos = []
    Vid = namedtuple('video', 'title videoId')
    for count, video in enumerate(json_items[::-1]):
        v = Vid(title=video['snippet']['title'],
                videoId=video['snippet']['resourceId']['videoId'])
        videos.append(v)
    #     videos.append((count,
    #                    video['snippet']['title'],
    #                    video['snippet']['resourceId']['videoId']))

    return videos


# https://developers.google.com/youtube/v3/docs/videos/list#try-it
def get_video_info(videoId):
    part = 'statistics'
    URL = BASE_URL + api_version + '/videos?' \
        'part=%(part)s' \
        '&id=%(videoId)s' \
        '&key=%(API_KEY)s'
    # viewcount
    # likeCount


def channel_statistics(username):
    part = 'statistics'
    URL = BASE_URL + api_version + '/channels?' \
        'part=%(part)s' \
        '&forUsername=%(username)s' \
        '&key=%(API_KEY)s'

    composed_url = URL % {'part': part,
                          'forUsername': username,
                          'API_KEY': API_KEY}

    resp = requests.get(composed_url)
    return resp.json()['items'][0]['statistics']

# viewCount
# subscriberCount
# videoCount

# what am i interested in?
#     number of videos overall
#     number of subscribers
#     viewcount for each video
#     likes for each vid

if __name__ == "__main__":
    playlistId = get_playlist_id(username)
    # video_attrs = get_video_title_and_id(playlistId)

    # for vid in video_attrs:

    # title, views, likes

import requests
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
def get_items_json(playlistId):
    part = 'snippet'
    URL = BASE_URL + api_version + '/playlistItems?' \
        'part=%(part)s' \
        '&playlistId=%(playlistId)s' \
        '&key=%(API_KEY)s'

    composed_url = URL % {'part': part,
                          'playlistId': playlistId,
                          'API_KEY': API_KEY}

    resp = requests.get(composed_url)
    return resp.json()['items']
    # r.json()['items'][1]['snippet']['title']
    # r.json()['items'][2]['snippet']['resourceId']['videoId']


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

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
def get_video_attrs(playlistId):
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
    items = resp.json()['items']

    videos = []
    for position, video in enumerate(items[::-1]):
        videos.append((position,
                       video['snippet']['title'],
                       video['snippet']['resourceId']['videoId']))

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
    video_attrs = get_video_attrs(playlistId)
    # for vid in video_attrs:

    # title, views, likes


# TODO: Get rid of maxresults=50 limit in get_video_attrs()
# To do that i probably need to use Oauth2.
# And i need "youtube" object, created with some YT library,
# something like this:
# youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
#                 http=credentials.authorize(httplib2.Http()))
# Example code could be found here:
# https://developers.google.com/youtube/v3/docs/playlistItems/list
# This it to get to youtube.playlistItems().list_next() method

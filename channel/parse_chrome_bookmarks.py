# This parser operates on Chrome bookmarks with <!DOCTYPE NETSCAPE-Bookmark-file-1>

# folder_name           - target folder with bookmarks within Chrome
# chrome_bookmark_file  - just the name of a .html file
#                (if it is located in the same folder)
#                Received by Bookmarks-Organize-Export to html
# Limitations:
# - Each bookmark should be of user/videos page
# - Also yatta script will not work with 'channel', only with 'user'. So I
#                'fail' such bookmarks
# In case of erroneous bookmark - parsed record will contain ERROR_MSG

# TODO: Subject of change
# parsed_bookmarks      - .txt file with parsed hrefs from target folder
# parsed_usernames      -

from bs4 import BeautifulSoup


folder_name = 'Unsubscribed_yt'
chrome_bookmark_file = 'bookmarks_4_17_16.html'
parsed_bookmarks = 'parsed_bookmarks.txt'
parsed_usernames = 'usernames.txt'

soup = BeautifulSoup(open(chrome_bookmark_file), "lxml")

DT = soup.find('h3', text=folder_name).parent
DL = DT.find_next_sibling()
a_all = DL.find_all('a')

urls = [a.attrs['href'] for a in a_all]

# TODO: decided to use DB. Probably sqlite3
# with open(parsed_bookmarks, 'w+') as f:
#     for url in urls:
#         f.write(url+'\n')

usernames = []
ERROR_MSG = '-- INVALID URL --'
for url in urls:
    if '/channel/' not in url and url.split('/')[-1] == 'videos':
        usernames.append(url.split('/')[-2])
    else:
        usernames.append(ERROR_MSG+url)

with open(parsed_usernames, 'w+') as f:
    for name in usernames:
        f.write(name+'\n')

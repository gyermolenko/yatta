# This parser operates on Chrome bookmarks with <!DOCTYPE NETSCAPE-Bookmark-file-1>

# folder_name           - target folder
# chrome_bookmark_file  - just the name of a .html file
#                         (if it is locates in the same folder
# parsed_bookmarks      - .txt file with parsed hrefs from target folder

from bs4 import BeautifulSoup


folder_name = 'Unsubscribed_yt'
chrome_bookmark_file = 'bookmarks_1_9_16.html'
parsed_bookmarks = 'parsed_bookmarks.txt'

soup = BeautifulSoup(open(chrome_bookmark_file))

DT = soup.find('h3', text=folder_name).parent
DL = DT.find_next_sibling()
a_all = DL.find_all('a')

urls = []
for a in a_all:
    urls.append(a.attrs['href'])

with open(parsed_bookmarks, 'w+') as f:
    for el in urls:
        f.write(el+'\n')

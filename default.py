import sys
import urlparse
import urllib
import urllib2

from bs4 import BeautifulSoup
from resources.lib import resolvers

import xbmcgui
import xbmcplugin
import xbmcaddon

########################################################
## VARS
########################################################

addon_id = xbmcaddon.Addon('plugin.video.pygccx')
base_url = 'http://www.gamingcx.com/p/gccx-videos.html'

plugin_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)

########################################################
## FUNCTIONS
########################################################

def build_url(query):
    return plugin_url + '?' + urllib.urlencode(query)

def add_sort_methods():
    xbmcplugin.addSortMethod(addon_handle, 1)

# def add_directory(title, image_url, url):
#     li = xbmcgui.ListItem(title, iconImage=image_url)
#     xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

def add_video_item(title, file_url):
    li = xbmcgui.ListItem(title)
    li.setInfo('video', {'title': title})
    li.setProperty('mimetype', 'video/flv')
    li.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=file_url, listitem=li)

# def play_video():
#     li = xbmcgui.ListItem(path=url)
#     xbmcplugin.setResolvedUrl( handle=addon_handle, succeeded=True, listitem=li)

def retrieve_play_url(episodeurl):
    url = urllib2.urlopen(episodeurl)
    if url:
        index = url.read()
        soup = BeautifulSoup(index, 'html.parser')
        for element in soup.find_all('iframe'):
            if 'vidbull' in element.attrs['src']:
                li = xbmcgui.ListItem(path=resolvers.request(element.attrs['src']))
                xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=li)
                break

########################################################
## BODY
########################################################

if mode is None:
    url = urllib2.urlopen(base_url)
    # add_sort_methods()
    xbmcplugin.setContent(addon_handle, 'movies')

    if url:
        index = url.read()
        # print(index)
        soup = BeautifulSoup(index, 'html.parser')
        # print(soup.prettify(encoding='utf-8'))
        soup = BeautifulSoup(str(soup.select('[class~=post-outer]')[0]), 'html.parser')
        # print(soup)
        for element in soup.find_all('a'):
            if 'href' in element.attrs:
                if 'gamingcx.com' in element.attrs['href']:
                    # print(unicode(element.attrs['href']))
                    # print(element.string)
                    add_video_item(element.string, sys.argv[0] + urllib.quote(unicode(element.attrs['href'])) + '?mode=play_video')

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'play_video':
    retrieve_play_url(urllib.unquote(urlparse.urlparse(sys.argv[0])[2][1:]))

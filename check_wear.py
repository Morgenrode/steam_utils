'''This is a poorly written script for spitting out quality data for 
CS:GO weapons for trading purposes. Functionality may be added as I 
learn what I'm doing'''

from sys import argv
from urllib.request import Request, urlopen
import xml.etree.ElementTree as etree

# this needs re-written with argparse
try:
    url = argv[1]
except:
    print('''\n
    -----USAGE-----\n
    python3 check_wear.py  steam_item_url\n
    ---------------''')

HEADERS = {'User-Agent': 'Mozilla/5.0'} # spoof useragent
STEAM_API_KEY = 'BD30CBB6AEDB0F64B7A879174B115CDA' #from dev api key

def get_steamid64(url):
    '''Gets steam_id64 either from the url directly, or from xml if the user has
    set a vanity url'''

    vanity_name = ''
    steam_id64 = ''

    try:
        item_id = url.split('/')[-1][-10:]

        if url.split('/')[3] == 'id': 
            vanity_name = url.split('/')[3]
        else:
            try:
                steam_id64 = int(url.split('/')[4])
                return steam_id64, item_id
            except ValueError as v:
                print(v, '\nInvalid steamcommunity inventory url')
    except:
        print('Imporperly formed url')

    req = Request('http://steamcommunity.com/id/{0}/?xml=1'.format(vanity_name), headers = HEADERS)
    steamxml = etree.parse(urlopen(req))
    try:
        steam_id64 = steamxml.find('steamID64').text
        return steam_id64, item_id
    except:
        pass

def parse(page):
    #parse out the wear value
    pass

def get_inventory(api=STEAM_API_KEY, user_id='76561198020353514'):
    '''Download the specified user's CS:GO inventory page using urllib'''

    req = Request('http://api.steampowered.com/IEconItems_730/GetPlayerItems/v0001/?key={0}&SteamID={1}&format=xml'.format(steam_api_key, 
    user_id), headers = HEADERS)
    webpage = etree.parse(urlopen(req))

        
get_steamid64(url) 

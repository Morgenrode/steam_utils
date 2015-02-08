'''This is a poorly written script for spitting out quality data from 
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
    python3 check_wear.py steam_item_url\n
    ---------------''')

HEADERS = {'User-Agent': 'Mozilla/5.0'} # spoof useragent
STEAM_API_KEY = 'BD30CBB6AEDB0F64B7A879174B115CDA' #from dev api key

def get_steamid64(target_url):
    '''Gets steam_id64 either from the url directly, or from xml if the user has
    set a vanity url'''

    vanity_name = ''
    steam_id64 = ''

    try:
        item_id = url.split('/')[-1][-10:].strip('_') # for 9 and 10 digit item ids

        if url.split('/')[3] == 'id': # only in links where the user has set a vanity name
            vanity_name = url.split('/')[4]
        else:
            try:
                steam_id64 = int(url.split('/')[4]) # steam 64 ids are digits only
                return steam_id64, item_id
            except ValueError as v:
                print(v, '\nInvalid steamcommunity inventory url')
    except:
        print('Improperly formed url')

    req = Request('http://steamcommunity.com/id/{0}/?xml=1'.format(vanity_name), headers = HEADERS)
    steamxml = etree.parse(urlopen(req))
    try:
        steam_id64 = steamxml.find('steamID64').text # steam 64 id is stored right near the beginning of the xml
        return steam_id64, item_id
    except:
        pass # need to add an informative error thing here


def get_inventory(api_key, user_id):
    '''Download the specified user's CS:GO inventory page using urllib'''

    req = Request('http://api.steampowered.com/IEconItems_730/GetPlayerItems/v0001/?key={0}&SteamID={1}&format=xml'.format(STEAM_API_KEY, 
    user_id), headers = HEADERS)
    webpage = etree.parse(urlopen(req))
    return webpage
    
def parse(url):
    steam_id64, item_id = get_steamid64(url)
    page = get_inventory(api_key=STEAM_API_KEY, user_id=steam_id64).getroot()
    for child in page.findall('./items/'):
        if child.find('id').text == item_id:
            for index in child.findall('.attributes/attribute'):
                if index.find('defindex').text == '8':
                    print(index.find('float_value').text)


# ------------------ #
if __name__ == '__main__':
    print('Fetching item wear data...')
    parse(url)

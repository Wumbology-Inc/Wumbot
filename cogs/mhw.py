import asyncio
import json
import typing
from datetime import datetime
from pathlib import Path

import aiohttp
import discord
from yarl import URL


class SteamNewsPost:
    def __init__(self, gid: str=None, title: str=None, url: str=None, is_external_url: bool=None, 
                 author: str=None, contents: str=None, feedlabel: str=None, date: int=None, 
                 feedname: str=None, feed_type: int=None, appid: int=None
                 ):
        
        self.gid = gid
        self.title = title
        self.url = URL(url)
        self.is_external_url = is_external_url
        self.author = author
        self.contents = contents
        self.feedlabel = feedlabel
        self.date = datetime.fromtimestamp(date)
        self.feedname = feedname
        self.feed_type = feed_type
        self.appid = appid
        
    def __repr__(self):
        return f"<SteamNews> \"{self.title}\" Posted {datetime.strftime(self.date, '%Y-%m-%d')} by {self.author}"
        
    @staticmethod
    def getnewsforapp(appID: int=582010, count: int=10, maxlength: int=300, 
                      format: str='json', **kwargs) -> typing.List[SteamNewsPost]:
        apiURL = URL("https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/")
        
        paramdict = {'appID': appID, 'count': count, 'maxlength': maxlength, 'format': format}
        r = requests.get(apiURL.with_query(paramdict))
        rawdict = r.json()
        
        if rawdict['appnews'] and rawdict['appnews']['newsitems']:
            return [SteamNewsPost(**item) for item in rawdict['appnews']['newsitems']]
        else:
            return None
        
    @staticmethod
    async def asyncgetnewsforapp(appID: int=582010, count: int=10, maxlength: int=300, 
                                 format: str='json', **kwargs) -> typing.List[SteamNewsPost]:
        apiURL = URL("https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/")
        
        paramdict = {'appID': appID, 'count': count, 'maxlength': maxlength, 'format': format}
        async with aiohttp.ClientSession() as session:
            async with session.get(apiURL.with_query(paramdict)) as resp:
                rawdict = await resp.json()
        
        if rawdict['appnews'] and rawdict['appnews']['newsitems']:
            return [SteamNewsPost(**item) for item in rawdict['appnews']['newsitems']]
        else:
            return None


def setup(bot):
    pass
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
                      format: str='json', **kwargs) -> typing.List:
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
                                 format: str='json', **kwargs) -> typing.List:
        apiURL = URL("https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/")
        
        paramdict = {'appID': appID, 'count': count, 'maxlength': maxlength, 'format': format}
        async with aiohttp.ClientSession() as session:
            async with session.get(apiURL.with_query(paramdict)) as resp:
                rawdict = await resp.json()
        
        if rawdict['appnews'] and rawdict['appnews']['newsitems']:
            return [SteamNewsPost(**item) for item in rawdict['appnews']['newsitems']]
        else:
            return None

class MHWNewsParser:
    def __init__(self, bot):
        self.bot = bot
        self.postchannelID = 478568995767713793
        self.logJSONpath = Path('./log/postedMHWnews.JSON')
        self.postedMHWnews = []
        self.appID = 582010
        self.officialaccount = "MHW_CAPCOM"

    async def getofficialnews(self, appID: int=None) -> typing.List:
        """
        Return a list of SteamNewsPost objects containing official Capcom announcements

        Posts with "Status Update" in the title are excluded
        """
        appID = appID if appID is not None else self.appID

        news = await SteamNewsPost.asyncgetnewsforapp(appID=appID, count=15, maxlength=500)
        officialnews = [item for item in news if self.MHWnewsfilter(item, self.officialaccount)]

        return officialnews

    async def postpatchnotes(self, postobj: SteamNewsPost=None, channelID: int=None):
        channelID = channelID if channelID is not None else self.postchannelID
        if postobj is None or not isinstance(postobj, SteamNewsPost):
            raise ValueError

        postchannel = self.bot.get_channel(channelID)

        postembed = discord.Embed(title=postobj.title, color=discord.Color(0x9c4af7),
                                  description=f"```{postobj.contents}```\n[View full patch notes]({postobj.url})\n"
                                  )
        postembed.set_author(name='Capcom', url=URL('https://steamcommunity.com/app/582010/announcements/'), 
                             icon_url=URL('https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Capcom_logo.svg/320px-Capcom_logo.svg')
                             )
        postembed.set_thumbnail(url=URL('https://steamcdn-a.akamaihd.net/steam/apps/582010/header.jpg'))
        postembed.set_footer(text="Brought to you by Palico power!", 
                             icon_url=URL("https://cdn.discordapp.com/attachments/417527786614554638/487788870193381387/s-l300.png")
                             )
        await postchannel.send('A new MHW news post has been released!', embed=postembed)

    def loadposted(self, logJSONpath: Path=None):
        logJSONpath = logJSONpath if logJSONpath is not None else self.logJSONpath
        
        if logJSONpath.exists():
            with logJSONpath.open(mode='r') as fID:
                self.postedMHWnews = [URL(urlstr) for urlstr in json.load(fID)]

    def saveposted(self, logJSONpath: Path=None):
        logJSONpath = logJSONpath if logJSONpath is not None else self.logJSONpath
        
        if self.postedMHWnews:
            with logJSONpath.open(mode='w') as fID:
                json.dump([str(url) for url in self.postedMHWnews], fID)

    async def patchcheck(self):
        self.loadposted()

        posts = await self.getofficialnews()
        newposts = [post for post in posts if post.url not in self.postedMHWnews]
        for post in reversed(newposts):  # Attempt to get close to posting in chronological order
            await self.postpatchnotes(post)
            self.postedMHWnews.append(post.url)
        
        self.saveposted()

    @staticmethod
    def MHWnewsfilter(item: SteamNewsPost=None, officialaccount: str=None) -> bool:
        if not item or not officialaccount:
            raise ValueError

        if item.author != officialaccount:
            return False

        return "status update" not in item.title.lower()

async def patchchecktimer(client, sleepseconds=3600):
    await client.wait_until_ready()
    parsers = (MHWNewsParser(client),)
    while not client.is_closed():
        for p in parsers:
            await p.patchcheck()
            
        await asyncio.sleep(sleepseconds)

def setup(bot):
    pass

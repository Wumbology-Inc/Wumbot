import asyncio
import json
import typing
from datetime import datetime
from pathlib import Path

import aiohttp
import discord
from yarl import URL

from reddit import RedditPost

class PatchGifParser:
    def __init__(self, bot):
        self.bot = bot
        self.postjsonURL = "https://www.reddit.com/user/itsjieyang/submitted.json"
        self.postchannelID = 477916849879908386
        self.logJSONpath = Path('./log/postedGIFs.JSON')
        self.postedGIFs = []

    async def getpatchgifs(self, jsonURL: str=None):
        """
        Return a list of RedditPost objects generated from Patch Notes submissions by /u/itsjieyang to /r/Overwatch
        """
        jsonURL = jsonURL if jsonURL is not None else self.postjsonURL
        async with aiohttp.ClientSession() as session:
            async with session.get(jsonURL) as resp:
                rawdict = await resp.json()
                submissions = rawdict['data']['children']

        patchposts = []
        for postjson in submissions:
            postobj = RedditPost(postjson)

            # So far, patch notes GIFs we want are from /r/Overwatch and start with "patch"
            if postobj.subreddit == 'Overwatch' and postobj.title.lower().startswith('patch'):
                patchposts.append(postobj)

        return patchposts

    async def postpatchgif(self, postobj: RedditPost=None, channelID: int=None):
        channelID = channelID if channelID is not None else self.postchannelID

        if postobj is None or not isinstance(postobj, RedditPost):
            raise ValueError

        postchannel = self.bot.get_channel(channelID)

        postembed = discord.Embed(title=postobj.title, color=discord.Color(0x9c4af7),
                                  description=f'[View Full Resolution]({postobj.contentURL})\n\n[View Reddit Post]({postobj.permalink})'
                                  )
        postembed.set_author(name='/u/itsjieyang', url='https://www.reddit.com/user/itsjieyang')
        postembed.set_thumbnail(url='https://gear.blizzard.com/media/wysiwyg/default/logos/ow-logo-white-nds.png')
        postembed.set_image(url=self.gfygif(postobj.contentURL))
        postembed.set_footer(text="Overwatch, it's Ameizing!")
        await postchannel.send('A new patch gif has been posted!', embed=postembed)

    def loadposted(self, logJSONpath: Path=None):
        logJSONpath = logJSONpath if logJSONpath is not None else self.logJSONpath
        
        if logJSONpath.exists():
            with logJSONpath.open(mode='r') as fID:
                self.postedGIFs = json.load(fID)

    def saveposted(self, logJSONpath: Path=None):
        logJSONpath = logJSONpath if logJSONpath is not None else self.logJSONpath
        
        if self.postedGIFs:
            with logJSONpath.open(mode='w') as fID:
                json.dump(self.postedGIFs, fID)

    async def patchcheck(self):
        self.loadposted()

        posts = await self.getpatchgifs()
        newposts = [post for post in posts if post.contentURL not in self.postedGIFs]
        for post in newposts:
            await self.postpatchgif(post)
            self.postedGIFs.append(post.contentURL)
        
        self.saveposted()

    @staticmethod
    def gfygif(inURL: str):
        """
        Build a direct gif link from a gfycat URL

        e.g. https://gfycat.com/flippantvariablediplodocus -> https://giant.gfycat.com/FlippantVariableDiplodocus.gif

        Returns a string
        """
        gfyID = URL(inURL).path.replace('/', '')
        return URL.build(scheme="https", host="giant.gfycat.com", path=f"{gfyID}.gif").human_repr()

async def patchchecktimer(client, sleepseconds=3600):
    await client.wait_until_ready()
    p = PatchGifParser(client)
    while not client.is_closed():
        await p.patchcheck()
        await asyncio.sleep(sleepseconds)


class OWPatch():
    def __init__(self, patchref: str=None, ver: str=None, patchdate: datetime=None, 
                 patchURL: URL=None, 
                 bannerURL: URL=None
                 ):
        defaultpatchURL = URL('https://playoverwatch.com/en-us/news/patch-notes/pc')
        defaultbannerURL = URL('https://gear.blizzard.com/media/wysiwyg/default/logos/ow-logo-white-nds.png')
        
        self.patchref = patchref
        self.ver = ver
        self.patchdate = patchdate
        self.patchURL = patchURL if patchURL is not None else defaultpatchURL
        self.bannerURL = bannerURL if bannerURL is not None else defaultbannerURL
        
    def __repr__(self):
        return f"<OWPatch: v{self.ver}, Released: {datetime.strftime(self.patchdate, '%Y-%m-%d')}>"

def setup(bot):
    pass

import asyncio
import json
import logging
import re
import typing
from datetime import datetime
from pathlib import Path

import aiohttp
import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from yarl import URL

from .bot import Helpers
from .reddit import RedditPost, RedditPRAW, RedditJSON


class PatchGifParser:
    def __init__(self, bot):
        self.bot = bot
        self.postjsonURL = URL("https://www.reddit.com/user/itsjieyang/submitted.json")
        self.postchannelID = 477916849879908386
        self.logJSONpath = Path('./log/postedGIFs.JSON')
        self.postedGIFs = []

    async def getpatchgifs(self, jsonURL: URL=None):
        """
        Return a list of RedditPost objects generated from Patch Notes submissions by /u/itsjieyang to /r/Overwatch
        """
        jsonURL = jsonURL if jsonURL is not None else self.postjsonURL

        prawinstance = RedditPRAW()
        if prawinstance.isauthenticated:
            postobjs = [RedditPost.fromPRAW(submission) for submission in prawinstance.getnewusersubmissions('itsjieyang')]
        else:
            postobjs = await RedditJSON.asyncfromJSON(jsonURL)

        logging.info(f"Found {len(postobjs)} submission(s) by /u/itsjieyang")

        patchposts = []
        for postobj in postobjs:
            # So far, patch notes GIFs we want are from /r/Overwatch and start with "patch"
            if postobj.subreddit == 'Overwatch' and 'patch' in postobj.title.lower():
                patchposts.append(postobj)

        logging.info(f"Found {len(patchposts)} OW Patch GIF post(s)")
        return patchposts

    async def postpatchgif(self, postobj: RedditPost=None, channelID: int=None):
        channelID = channelID if channelID is not None else self.postchannelID

        if postobj is None:
            raise ValueError("No post object provided")
        if not isinstance(postobj, RedditPost):
            raise TypeError(f"Invalid post type provided: '{type(postobj)}', input must be RedditPost")

        postchannel = self.bot.get_channel(channelID)

        postembed = discord.Embed(title=postobj.title, color=discord.Color(0x9c4af7),
                                  description=f'[View Full Resolution]({postobj.contentURL})\n\n[View Reddit Post]({postobj.permalink})'
                                  )
        postembed.set_author(name='/u/itsjieyang', url=URL('https://www.reddit.com/user/itsjieyang'))
        postembed.set_thumbnail(url=URL('https://gear.blizzard.com/media/wysiwyg/default/logos/ow-logo-white-nds.png'))
        postembed.set_image(url=self.gfygif(postobj.contentURL))
        postembed.set_footer(text="Overwatch, it's Ameizing!")
        await postchannel.send('A new patch gif has been posted!', embed=postembed)

    def loadposted(self, logJSONpath: Path=None):
        logJSONpath = logJSONpath if logJSONpath is not None else self.logJSONpath
        
        if logJSONpath.exists():
            with logJSONpath.open(mode='r') as fID:
                savedGIFs = json.load(fID)
            
            if savedGIFs:
                self.postedGIFs = savedGIFs
                logging.info(f"Loaded {len(self.postedGIFs)} OW GIF(s) from '{logJSONpath}'")
            else:
                logging.info(f"No posted OW GIFs found in JSON log")
        else:
            logging.info(f"OW GIF log JSON does not yet exist")

    def saveposted(self, logJSONpath: Path=None):
        logJSONpath = logJSONpath if logJSONpath is not None else self.logJSONpath
        
        if self.postedGIFs:
            with logJSONpath.open(mode='w') as fID:
                json.dump(self.postedGIFs, fID)
            logging.info(f"Saved {len(self.postedGIFs)} OW GIF URL(s)")
        else:
            logging.info("No OW GIFs to save")

    async def patchcheck(self):
        logging.info("OW patch GIF check coroutine invoked")
        self.loadposted()

        posts = await self.getpatchgifs()
        newposts = [post for post in posts if post.contentURL not in self.postedGIFs]
        logging.info(f"Found {len(newposts)} new GIF(s) to post")
        for post in reversed(newposts):  # Attempt to get close to posting in chronological order
            await self.postpatchgif(post)
            self.postedGIFs.append(post.contentURL.human_repr())
        
        self.saveposted()

    @staticmethod
    def gfygif(inURL: typing.Union[str, URL]) -> URL:
        """
        Build a direct gif link from a gfycat URL

        e.g. https://gfycat.com/flippantvariablediplodocus -> https://giant.gfycat.com/FlippantVariableDiplodocus.gif

        Returns a string
        """
        gfyID = URL(inURL).path.replace('/', '')
        return URL.build(scheme="https", host="giant.gfycat.com", path=f"{gfyID}.gif")


class OWPatch():
    def __init__(self, patchref: str=None, ver: str=None, patchdate: datetime=None, 
                 patchURL: URL=None, bannerURL: URL=None
                 ):
        defaultpatchURL = URL('https://playoverwatch.com/en-us/news/patch-notes/pc')
        defaultbannerURL = URL('https://gear.blizzard.com/media/wysiwyg/default/logos/ow-logo-white-nds.png')
        
        self.patchref = patchref
        self.ver = ver
        self.patchdate = patchdate
        self.patchURL = patchURL if patchURL is not None else defaultpatchURL
        self.bannerURL = bannerURL if bannerURL is not None else defaultbannerURL
        
    def __repr__(self):
        return f"OWPatch: v{self.ver}, Released: {datetime.strftime(self.patchdate, '%Y-%m-%d')}"

    @staticmethod
    def fromURL(inURL: typing.Union[str, URL]=URL('https://playoverwatch.com/en-us/news/patch-notes/pc')) -> typing.List:
        """
        Return a list of OWPatch objects from Blizzard's Patch Notes
        """
        if not inURL:
            raise ValueError("No URL provided")
        inURL = URL(inURL)

        r = requests.get(inURL).text
        
        return OWPatch._parseOWpatchHTML(r)

    @staticmethod
    async def asyncfromURL(inURL: typing.Union[str, URL]=URL('https://playoverwatch.com/en-us/news/patch-notes/pc')) -> typing.List:
        """
        This function is a coroutine

        Return a list of OWPatch objects from Blizzard's Patch Notes
        """
        if not inURL:
            raise ValueError("No URL provided")
        inURL = URL(inURL)

        async with aiohttp.ClientSession() as session:
            async with session.get(inURL) as resp:
                r = await resp.text()
        
        return OWPatch._parseOWpatchHTML(r)

    @staticmethod
    def _parseOWpatchHTML(inHTML: str) -> typing.List:
        soup = BeautifulSoup(inHTML, 'html.parser')
        
        # Iterate over patches
        patches = soup.find_all('div', class_='patch-notes-patch')
        
        patchobjs = []
        for patch in patches:
            # Get patch reference ID
            patchref = patch.get('id')
            patchref_num = patchref.split('-')[-1]   # Get numeric reference to build BlizzTrack link later

            # Get version number from sidebar using patch reference ID
            sidebaritem = soup.select_one(f"a[href=#{patchref}]").parent
            ver = sidebaritem.find('h3').get_text().split()[-1]

            # Get date
            dateheader = patch.find('h2', class_='HeadingBanner-header')
            if dateheader:
                patchdate = datetime.strptime(dateheader.get_text(), '%B %d, %Y')
            else:
                # In the event there is no banner, the date is instead embedded in <h1>Overwatch Patch Notes – June 5, 2018</h1>
                # Since we already have the sidebar entry, it's slightly simpler to get the date from that instead
                patchdate = datetime.strptime(sidebaritem.find('p').get_text(), '%m/%d/%Y')
                
            # Get patch banner
            # If there is a banner for the patch, it's embedded in the 'style' portion of the '.HeadingBanner' div
            # e.g. <div class="HeadingBanner" style="background-image: url(https://link/to.jpg);">
            patchbannerdiv = patch.select_one('.HeadingBanner')
            if patchbannerdiv:
                expr = r"url\(\"?([^\"]+)\"?\)"
                m = re.search(expr, patchbannerdiv['style'])
                if m:
                    patchbanner = URL(m.group(1))
                else:
                    patchbanner = None
            else:
                patchbanner = None

            patchobjs.append(OWPatch(patchref, ver, patchdate, OWPatch.getblizztrack(patchref_num), patchbanner))
        
        return patchobjs

    @staticmethod
    def getblizztrack(patchref: str=None) -> URL:
        """
        Return BlizzTrack URL to patch notes, built using Blizzard's patchref
        
        e.g. https://blizztrack.com/patch_notes/overwatch/50148
        """
        if not patchref:
            raise ValueError('No patch reference provided')

        baseURL = URL('https://blizztrack.com/patch_notes/overwatch/')
        return baseURL / patchref


class PatchNotesParser:
    def __init__(self, bot):
        self.bot = bot
        self.patchesURL = URL('https://playoverwatch.com/en-us/news/patch-notes/pc')
        self.postchannelID = 477916849879908386
        self.logJSONpath = Path('./log/postedpatches.JSON')
        self.postedpatches = []

    async def postpatchnotes(self, postobj: OWPatch=None, channelID: int=None):
        channelID = channelID if channelID is not None else self.postchannelID
        if postobj is None:
            raise ValueError("No post object provided")
        if not isinstance(postobj, OWPatch):
            raise TypeError(f"Invalid object type provided: '{type(postobj)}', input must be OWPatch")

        postchannel = self.bot.get_channel(channelID)

        postembed = discord.Embed(title=str(postobj), color=discord.Color(0x9c4af7),
                                  description=f"[View full patch notes]({postobj.patchURL})"
                                  )
        postembed.set_author(name='Blizzard', url=URL('https://playoverwatch.com/en-us/news/patch-notes/pc'), 
                             icon_url=URL('http://us.blizzard.com/static/_images/logos/blizzard.jpg')
                             )
        postembed.set_thumbnail(url=URL('https://gear.blizzard.com/media/wysiwyg/default/logos/ow-logo-white-nds.png'))
        postembed.set_image(url=postobj.bannerURL)
        postembed.set_footer(text="Patch Notes Provided by BlizzTrack")
        await postchannel.send('A new Overwatch Patch has been released!', embed=postembed)

    def loadposted(self, logJSONpath: Path=None):
        logJSONpath = logJSONpath if logJSONpath is not None else self.logJSONpath

        if logJSONpath.exists():
            with logJSONpath.open(mode='r') as fID:
                savedpatches = json.load(fID)
            
            if savedpatchess:
                self.postedpatches = savedpatches
                logging.info(f"Loaded {len(self.postedpatches)} OW patch(es) from '{logJSONpath}'")
            else:
                logging.info(f"No posted OW patch(es) found in JSON log")
        else:
            logging.info(f"OW patch log JSON does not yet exist")

    def saveposted(self, logJSONpath: Path=None):
        logJSONpath = logJSONpath if logJSONpath is not None else self.logJSONpath
        
        if self.postedpatches:
            with logJSONpath.open(mode='w') as fID:
                json.dump(self.postedpatches, fID)
                logging.info(f"Saved {len(self.postedpatches)} OW patch(es)")
        else:
            logging.info("No OW patches to save")

    async def patchcheck(self):
        logging.info("OW Patch check coroutine invoked")
        self.loadposted()

        patches = await OWPatch.asyncfromURL(self.patchesURL)
        newpatches = [patch for patch in patches if patch.ver not in self.postedpatches]
        logging.info(f"Found {len(newpatches)} new OW patch(es) to post")
        for patch in reversed(newpatches):  # Attempt to get close to posting in chronological order
            await self.postpatchnotes(patch)
            self.postedpatches.append(patch.ver)
        
        self.saveposted()


async def patchchecktimer(client, sleepseconds: int=3600):
    await client.wait_until_ready()
    parsers = (PatchGifParser(client), PatchNotesParser(client))
    while not client.is_closed():
        for p in parsers:
            await p.patchcheck()
            
        await asyncio.sleep(sleepseconds)


class OverwatchCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def checkOWgif(self, ctx: commands.Context):
        if Helpers.isDM(ctx.message.channel) and Helpers.isOwner(ctx.message.author):
            logging.info(f'Manual OW patch GIF check initiated by {ctx.message.author}')
            await ctx.send("Manual OW patch GIF parsing starting now...")
            await PatchGifParser(self.bot).patchcheck()
        elif Helpers.isOwner(ctx.message.author) and not Helpers.isDM(ctx.message.channel):
            await ctx.send(f'{ctx.message.author.mention}, this command only works in a DM')
        else:
            logging.info(f'Manual OW patch GIF check attempted by {ctx.message.author}')
            await ctx.send(f'{ctx.message.author.mention}, you are not authorized to perform this operation')

    @commands.command()
    async def checkOWpatch(self, ctx: commands.Context):
        if Helpers.isDM(ctx.message.channel) and Helpers.isOwner(ctx.message.author):
            logging.info(f'Manual OW patch check initiated by {ctx.message.author}')
            await ctx.send("Manual OW patch notes parsing starting now...")
            await PatchNotesParser(self.bot).patchcheck()
        elif Helpers.isOwner(ctx.message.author) and not Helpers.isDM(ctx.message.channel):
            await ctx.send(f'{ctx.message.author.mention}, this command only works in a DM')
        else:
            logging.info(f'Manual OW patch check attempted by {ctx.message.author}')
            await ctx.send(f'{ctx.message.author.mention}, you are not authorized to perform this operation')

def setup(bot):
    bot.add_cog(OverwatchCommands(bot))

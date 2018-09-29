import asyncio
import json
import logging
import re
import typing
from pathlib import Path

import discord
from discord.ext import commands
from yarl import URL

from bot.models.Overwatch import OWPatch
from bot.models.Reddit import RedditJSON, RedditPost, RedditPRAW
from bot.utils import Helpers


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
                savedGIFs = [URL(gfyurl) for gfyurl in json.load(fID)]
            
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
                json.dump([str(url) for url in self.postedGIFs], fID)
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

            if savedpatches:
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

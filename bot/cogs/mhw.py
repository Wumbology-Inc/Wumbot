import asyncio
import json
import logging
import typing
from datetime import datetime
from pathlib import Path

import aiohttp
import discord
from discord.ext import commands
from yarl import URL

from bot.models.Steam import SteamNewsPost
from bot.utils import Helpers


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
        """
        appID = appID if appID is not None else self.appID

        news = await SteamNewsPost.asyncgetnewsforapp(appID=appID, count=15, maxlength=600)
        logging.info(f"{len(news)} MHW news posts returned by Steam's API")
        officialnews = [item for item in news if self.MHWnewsfilter(item, self.officialaccount)]

        logging.info(f"Found {len(officialnews)} official MHW news posts")
        return officialnews

    async def postpatchnotes(self, postobj: SteamNewsPost=None, channelID: int=None):
        channelID = channelID if channelID is not None else self.postchannelID
        if postobj is None:
            raise ValueError("No postobj provided")
        if not isinstance(postobj, SteamNewsPost):
            raise TypeError(f"Invalid post object type provided: '{type(postobj)}', input must be SteamNewsPost")

        postchannel = self.bot.get_channel(channelID)

        postembed = discord.Embed(title=postobj.title, color=discord.Color(0x9c4af7),
                                  description=f"```{postobj.contents}```\n[View full news post]({postobj.url})\n"
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
                savednewsposts = [URL(urlstr) for urlstr in json.load(fID)]
            
            if savednewsposts:
                self.postedMHWnews = savednewsposts
                logging.info(f"Loaded {len(self.postedMHWnews)} MHW news post(s) from '{logJSONpath}'")
            else:
                logging.info(f"No posted MHW news posts found in JSON log")
        else:
            logging.info(f"MHW news post JSON log does not yet exist")

    def saveposted(self, logJSONpath: Path=None):
        logJSONpath = logJSONpath if logJSONpath is not None else self.logJSONpath
        
        if self.postedMHWnews:
            with logJSONpath.open(mode='w') as fID:
                json.dump([str(url) for url in self.postedMHWnews], fID)
                logging.info(f"Saved {len(self.postedMHWnews)} MHW news post(s)")
        else:
            logging.info("No MHW news posts to save")

    async def patchcheck(self):
        logging.info("MHW News check coroutine invoked")
        self.loadposted()

        posts = await self.getofficialnews()
        newposts = [post for post in posts if post.url not in self.postedMHWnews]
        logging.info(f"Found {len(newposts)} unposted MHW news posts")
        for post in reversed(newposts):  # Attempt to get close to posting in chronological order
            await self.postpatchnotes(post)
            self.postedMHWnews.append(post.url)
        
        self.saveposted()

    @staticmethod
    def MHWnewsfilter(item: SteamNewsPost=None, officialaccount: str=None) -> bool:
        if not item:
            raise ValueError("No post object provided")
        if not officialaccount:
            raise ValueError("No account name provided")

        if item.author != officialaccount:
            return False
        else:
            return True


class MHWCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def checkMHWpatch(self, ctx: commands.Context):
        if Helpers.isDM(ctx.message.channel) and Helpers.isOwner(ctx.message.author):
            logging.info(f'Manual MHW news check initiated by {ctx.message.author}')
            await ctx.send("Manual MHW news parsing starting now...")
            await MHWNewsParser(self.bot).patchcheck()
        elif Helpers.isOwner(ctx.message.author) and not Helpers.isDM(ctx.message.channel):
            await ctx.send(f'{ctx.message.author.mention}, this command only works in a DM')
        else:
            logging.info(f'Manual MHW news check attempted by {ctx.message.author}')
            await ctx.send(f'{ctx.message.author.mention}, you are not authorized to perform this operation')

def setup(bot):
    bot.add_cog(MHWCommands(bot))

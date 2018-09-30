import json
import logging
import typing
from datetime import datetime
from pathlib import Path

import aiohttp
import discord
from discord.ext import commands
from yarl import URL

from bot.models.ManualCheck import ManualCheck
from bot.models.NewsParser import NewsParser
from bot.models.Steam import SteamNewsPost


class MHWNewsParser(NewsParser):
    def __init__(self, bot):
        super().__init__(bot)
        self.parsername = "MHW News"
        self.postchannelID = 478568995767713793
        self.logJSONpath = Path('./log/postedMHWnews.JSON')
        self.appID = 582010
        self.officialaccount = "MHW_CAPCOM"

    async def getofficialnews(self, appID: int=None) -> typing.List:
        """
        Return a list of SteamNewsPost objects containing official Capcom announcements
        """
        appID = appID if appID is not None else self.appID

        news = await SteamNewsPost.asyncgetnewsforapp(appID=appID, count=15, maxlength=600)
        logging.info(f"{len(news)} {self.parsername} post(s) returned by Steam's API")
        officialnews = [item for item in news if self.MHWnewsfilter(item, self.officialaccount)]

        logging.info(f"Found {len(officialnews)} official {self.parsername} post(s)")
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
        await postchannel.send(f"A new {self.parsername} post has been released!", embed=postembed)

    async def patchcheck(self):
        logging.info(f"{self.parsername} check coroutine invoked")
        self.loadposted(converter=URL)

        posts = await self.getofficialnews()
        newposts = [post for post in posts if post.url not in self.postednews]
        logging.info(f"Found {len(newposts)} unposted {self.parsername} posts")

        if newposts:
            for post in reversed(newposts):  # Attempt to get close to posting in chronological order
                await self.postpatchnotes(post)
                self.postednews.append(post.url)

            self.saveposted(converter=str)

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
        await ManualCheck.check(ctx=ctx, toinvoke=MHWNewsParser(self.bot).patchcheck, commandstr='MHW news')


def setup(bot):
    bot.add_cog(MHWCommands(bot))

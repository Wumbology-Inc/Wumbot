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
from bot.utils.Constants import Channels


class MHWNewsParser(NewsParser):
    def __init__(self, bot):
        super().__init__(bot)
        self.postchannelID = Channels.mhw
        self.logJSONpath = Path("./log/postedMHWnews.JSON")
        self.appID = 582010
        self.officialaccount = "MHW_CAPCOM"

        self._parsername = "MHW News"
        self._loadconverter = URL
        self._saveconverter = str
        self._comparator = "url"

    async def getofficialnews(self, appID: int = None) -> typing.List:
        """
        Return a list of SteamNewsPost objects containing official Capcom announcements
        """
        appID = appID if appID is not None else self.appID

        news = await SteamNewsPost.asyncgetnewsforapp(
            appID=appID, count=15, maxlength=600
        )
        logging.info(f"{len(news)} {self._parsername} post(s) returned by Steam's API")
        officialnews = [
            item for item in news if self.MHWnewsfilter(item, self.officialaccount)
        ]

        logging.info(f"Found {len(officialnews)} official {self._parsername} post(s)")
        return officialnews

    async def postembed(self, postobj: SteamNewsPost = None, channelID: int = None):
        channelID = channelID if channelID is not None else self.postchannelID
        if postobj is None:
            raise ValueError("No postobj provided")
        if not isinstance(postobj, SteamNewsPost):
            raise TypeError(
                f"Invalid post object type provided: '{type(postobj)}', input must be SteamNewsPost"
            )

        postchannel = self.bot.get_channel(channelID)

        postembed = discord.Embed(
            title=postobj.title,
            color=discord.Color(0x9C4AF7),
            description=f"```{postobj.contents}```\n[View full news post]({postobj.url})\n",
        )
        postembed.set_author(
            name="Capcom",
            url=URL("https://steamcommunity.com/app/582010/announcements/"),
            icon_url=URL(
                "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Capcom_logo.svg/320px-Capcom_logo.svg"
            ),
        )
        postembed.set_thumbnail(
            url=URL("https://steamcdn-a.akamaihd.net/steam/apps/582010/header.jpg")
        )
        postembed.set_footer(
            text="Brought to you by Palico power!",
            icon_url=URL(
                "https://cdn.discordapp.com/attachments/417527786614554638/487788870193381387/s-l300.png"
            ),
        )
        await postchannel.send(
            f"A new {self._parsername} post has been released!", embed=postembed
        )

    async def patchcheck(self):
        posts = await self.getofficialnews()
        await super().patchcheck(posts)

    @staticmethod
    def MHWnewsfilter(item: SteamNewsPost = None, officialaccount: str = None) -> bool:
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
        await ManualCheck.check(
            ctx=ctx, toinvoke=MHWNewsParser(self.bot).patchcheck, commandstr="MHW news"
        )


def setup(bot):
    bot.add_cog(MHWCommands(bot))

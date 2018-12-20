import logging
import typing
from pathlib import Path

import discord
from discord.ext import commands
from yarl import URL

from bot.models.ManualCheck import ManualCheck
from bot.models.NewsParser import NewsParser
from bot.models.Steam import SteamNewsPost
from bot.utils.Constants import Channels


class RLNewsParser(NewsParser):
    def __init__(self, bot):
        super().__init__(bot)
        self.postchannelID = Channels.rl
        self.logJSONpath = Path("./log/postedRLnews.JSON")
        self.appID = 252950
        self.psyonixstaff = ("dirkened", "psyonix devin")

        self._parsername = "RL News"
        self._loadconverter = URL
        self._saveconverter = str
        self._comparator = "url"

    async def getofficialnews(self, appID: int = None) -> typing.List:
        """
        Return a list of SteamNewsPost objects containing official Rocket League announcements
        """
        appID = appID if appID is not None else self.appID

        news = await SteamNewsPost.asyncgetnewsforapp(
            appID=appID, count=15, maxlength=600
        )
        logging.info(f"{len(news)} {self._parsername} post(s) returned by Steam's API")
        officialnews = [
            item for item in news if self.RLnewsfilter(item, self.psyonixstaff)
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
            name=postobj.author,
            url=URL("https://steamcommunity.com/app/252950/announcements/"),
            icon_url=URL(
                "https://cdn.discordapp.com/attachments/417527786614554638/494692091453112320/unknown.png"
            ),
        )
        postembed.set_thumbnail(
            url=URL(
                "https://media.discordapp.net/attachments/417527786614554638/494691204248764416/timthumb.png"
            )
        )
        postembed.set_footer(
            text="What a save! What a save! What a save!",
            icon_url=URL(
                "https://cdn.discordapp.com/attachments/417527786614554638/494690857379692564/unknown.png"
            ),
        )
        await postchannel.send(
            f"A new {self._parsername} post has been released!", embed=postembed
        )

    async def patchcheck(self):
        posts = await self.getofficialnews()
        await super().patchcheck(posts)

    @staticmethod
    def RLnewsfilter(
        item: SteamNewsPost = None, psyonixstaff: typing.Tuple = None
    ) -> bool:
        if not item:
            raise ValueError("No post object provided")
        if not psyonixstaff:
            raise ValueError("No account name provided")

        if item.author.lower() not in psyonixstaff:
            return False
        else:
            return True


class RocketLeagueCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def checkRLpatch(self, ctx: commands.Context):
        await ManualCheck.check(
            ctx=ctx, toinvoke=RLNewsParser(self.bot).patchcheck, commandstr="RL news"
        )


def setup(bot):
    bot.add_cog(RocketLeagueCommands(bot))

import json
import logging
import typing
from pathlib import Path

import discord
from discord.ext import commands
from yarl import URL

from bot.models.ManualCheck import ManualCheck
from bot.models.NewsParser import NewsParser
from bot.models.Steam import SteamNewsPost


class RLNewsParser(NewsParser):
    def __init__(self, bot):
        super().__init__(bot)
        self.parsername = "RL News"
        self.postchannelID = 494682432688226316
        self.logJSONpath = Path('./log/postedRLnews.JSON')
        self.appID = 252950
        self.psyonixstaff = ('dirkened', 'psyonix devin')

    async def getofficialnews(self, appID: int=None) -> typing.List:
        """
        Return a list of SteamNewsPost objects containing official Rocket League announcements
        """
        appID = appID if appID is not None else self.appID

        news = await SteamNewsPost.asyncgetnewsforapp(appID=appID, count=15, maxlength=600)
        logging.info(f"{len(news)} {self.parsername} post(s) returned by Steam's API")
        officialnews = [item for item in news if self.RLnewsfilter(item, self.psyonixstaff)]

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
        postembed.set_author(name=postobj.author, url=URL('https://steamcommunity.com/app/252950/announcements/'), 
                             icon_url=URL('https://cdn.discordapp.com/attachments/417527786614554638/494692091453112320/unknown.png')
                             )
        postembed.set_thumbnail(url=URL('https://media.discordapp.net/attachments/417527786614554638/494691204248764416/timthumb.png'))
        postembed.set_footer(text="What a save! What a save! What a save!", 
                             icon_url=URL("https://cdn.discordapp.com/attachments/417527786614554638/494690857379692564/unknown.png")
                             )
        await postchannel.send(f"A new {self.parsername} post has been released!", embed=postembed)

    async def patchcheck(self):
        logging.info(f"{self.parsername} check coroutine invoked")
        self.loadposted(converter=URL)

        posts = await self.getofficialnews()
        newposts = [post for post in posts if post.url not in self.postednews]
        logging.info(f"Found {len(newposts)} unposted {self.parsername} post(s)")

        if newposts:
            for post in reversed(newposts):  # Attempt to get close to posting in chronological order
                await self.postpatchnotes(post)
                self.postednews.append(post.url)
            
            self.saveposted(converter=str)

    @staticmethod
    def RLnewsfilter(item: SteamNewsPost=None, psyonixstaff: typing.Tuple=None) -> bool:
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
        await ManualCheck.check(ctx=ctx, toinvoke=RLNewsParser(self.bot).patchcheck, commandstr='RL news')


def setup(bot):
    bot.add_cog(RocketLeagueCommands(bot))

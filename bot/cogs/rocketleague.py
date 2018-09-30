import asyncio
import json
import logging
import typing
from pathlib import Path

import discord
from discord.ext import commands
from yarl import URL

from bot.models.Steam import SteamNewsPost
from bot.utils import Helpers


class RLNewsParser:
    def __init__(self, bot):
        self.bot = bot
        self.postchannelID = 494682432688226316
        self.logJSONpath = Path('./log/postedRLnews.JSON')
        self.postedRLnews = []
        self.appID = 252950
        self.psyonixstaff = ('dirkened', 'psyonix devin')

    async def getofficialnews(self, appID: int=None) -> typing.List:
        """
        Return a list of SteamNewsPost objects containing official Rocket League announcements
        """
        appID = appID if appID is not None else self.appID

        news = await SteamNewsPost.asyncgetnewsforapp(appID=appID, count=15, maxlength=600)
        logging.info(f"{len(news)} RL news post(s) returned by Steam's API")
        officialnews = [item for item in news if self.RLnewsfilter(item, self.psyonixstaff)]

        logging.info(f"Found {len(officialnews)} official RL news posts")
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
        await postchannel.send('A new RL news post has been released!', embed=postembed)

    def loadposted(self, logJSONpath: Path=None):
        logJSONpath = logJSONpath if logJSONpath is not None else self.logJSONpath

        if logJSONpath.exists():
            with logJSONpath.open(mode='r') as fID:
                savednewsposts = [URL(urlstr) for urlstr in json.load(fID)]
            
            if savednewsposts:
                self.postedRLnews = savednewsposts
                logging.info(f"Loaded {len(self.postedRLnews)} RL news post(s) from '{logJSONpath}'")
            else:
                logging.info(f"No posted RL news posts found in JSON log")
        else:
            logging.info(f"RL news post JSON log does not yet exist")

    def saveposted(self, logJSONpath: Path=None):
        logJSONpath = logJSONpath if logJSONpath is not None else self.logJSONpath
        
        if self.postedRLnews:
            with logJSONpath.open(mode='w') as fID:
                json.dump([str(url) for url in self.postedRLnews], fID)
                logging.info(f"Saved {len(self.postedRLnews)} RL news post(s)")
        else:
            logging.info("No RL news posts to save")

    async def patchcheck(self):
        logging.info("RL News check coroutine invoked")
        self.loadposted()

        posts = await self.getofficialnews()
        newposts = [post for post in posts if post.url not in self.postedRLnews]
        logging.info(f"Found {len(newposts)} unposted RL news posts")
        for post in reversed(newposts):  # Attempt to get close to posting in chronological order
            await self.postpatchnotes(post)
            self.postedRLnews.append(post.url)
        
        self.saveposted()

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
        if Helpers.isDM(ctx.message.channel) and Helpers.isOwner(ctx.message.author):
            logging.info(f'Manual RL news check initiated by {ctx.message.author}')
            await ctx.send("Manual RL news parsing starting now...")
            await RLNewsParser(self.bot).patchcheck()
        elif Helpers.isOwner(ctx.message.author) and not Helpers.isDM(ctx.message.channel):
            await ctx.send(f'{ctx.message.author.mention}, this command only works in a DM')
        else:
            logging.info(f'Manual RL news check attempted by {ctx.message.author}')
            await ctx.send(f'{ctx.message.author.mention}, you are not authorized to perform this operation')

def setup(bot):
    bot.add_cog(RocketLeagueCommands(bot))

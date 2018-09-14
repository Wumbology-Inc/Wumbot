import logging
from datetime import datetime

import discord
import git
from discord.ext import commands


class MainCommands():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ver(self, ctx: commands.Context):
        """
        Reply with current Wumbot version number from the git master branch tag
        """
        currRepo = git.Repo('.')
        repoGit = currRepo.git
        try:
            await ctx.message.channel.send(f'Current Version: {repoGit.describe()}')
        except git.GitCommandError as err:
            await ctx.send('No tags found on current branch')

    @commands.command()
    async def uptime(self, ctx: commands.Context):
        """
        Reply with current uptime
        """
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"Wumbot has been up for: {days}d {hours}h {minutes}m {seconds}s")

    @commands.command()
    async def kill(self, ctx: commands.Context):
        """
        Disconnect bot from Discord

        Only valid if bot owner invokes the command in a DM
        """
        if Helpers.isDM(ctx.message.channel) and Helpers.isOwner(ctx.message.author):
            logging.info('Bot session killed by Owner')
            await ctx.send('Shutting down... :wave:')
            await self.bot.close()
        elif Helpers.isOwner(ctx.message.author) and not Helpers.isDM(ctx.message.channel):
            await ctx.send(f'{ctx.message.author.mention}, this command only works in a DM')
        else:
            logging.info(f'Unauthorized kill attempt by {ctx.message.author}')
            await ctx.send(f'{ctx.message.author.mention}, you are not authorized to perform this operation')

class Helpers:
    @staticmethod
    def isOwner(user: discord.User):
        """
        Check to see if the input User's ID matches the Owner ID
        """
        ownerID = 129606635545952258
        return user.id == ownerID
    
    @staticmethod
    def isDM(channel: discord.TextChannel):
        """
        Check to see if a channel is a DM

        A DM is either an instance of DMChannel or GroupChannel
        """
        return isinstance(channel, (discord.DMChannel, discord.GroupChannel))


def setup(bot):
    bot.add_cog(MainCommands(bot))

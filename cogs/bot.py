import asyncio
import logging
import string
from datetime import datetime

import discord
import git
from discord.ext import commands


class MainCommands():
    def __init__(self, bot):
        self.bot = bot

        self._lettermap = self._buildletterunicode()

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

    @commands.command()
    async def reactmessage(self, ctx: commands.Context, *args, selfdestructdelay: int=10):
        """
        Add reaction message to a message ID

        e.g. ~reactmessage 492366085232787467 Hype

        Command and any feedback are deleted after selfdestructdelay seconds
        """
        # Assume last entry in args is the message ID and concatenate everything else into the message
        continueflag = False
        try:
            messageID = int(args[0])
        except ValueError:
            pass
        reactmessage = ''.join(args[1::]).replace(' ', '').upper()  # Remove spaces & normalize to lowercase

        if not Helpers.isWumbologist(ctx.message.author):
            feedbackmsg = await ctx.send(f'{ctx.message.author.mention}, you are not authorized to perform this operation')
        elif len(reactmessage) == 0:
            feedbackmsg = await ctx.send("Command must be invoked with both a message and a message ID")
        elif not reactmessage.isalpha():
            feedbackmsg = await ctx.send("Reaction message must only contain alphabetic characters")
        elif len(reactmessage) != len(set(reactmessage.lower())):
            feedbackmsg = await ctx.send("Reaction message cannot contain duplicate letters")
        else:
            continueflag = True

        if not continueflag:
            await asyncio.sleep(selfdestructdelay)
            await ctx.message.delete()
            await feedbackmsg.delete()
            return

        continueflag = False
        messageObj = None
        for channel in self.bot.get_all_channels():
            if isinstance(channel, discord.TextChannel):
                try:
                    foundchannel = channel
                    messageObj = await channel.get_message(messageID)
                    continueflag = True
                except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                    continue
                finally:
                    if not messageObj:
                        feedbackmsg = await ctx.send(f"Message ID '{messageID}' could not be obtained")
        
        if continueflag:
            async with foundchannel.typing():
                for letter in reactmessage:
                    await messageObj.add_reaction(self._lettermap[letter])
                    await asyncio.sleep(selfdestructdelay)
        else:
            await asyncio.sleep(selfdestructdelay)
            await ctx.message.delete()
            await feedbackmsg.delete()

        await ctx.message.delete()


    @staticmethod
    def _buildletterunicode():
        """
        Return a dictionary mapping of alphabetical characters to their
        Unicode Regional Indicator Symbol Equivalent (1F1E6..1F1FF)

        See: 
            https://en.wikipedia.org/wiki/Regional_Indicator_Symbol
            https://www.unicode.org/charts/PDF/U1F100.pdf
        """
        # # Offset alphabetic letter index & convert to base 16
        # a = [(n + 5) % 16 for n in range(1, 27)]
        # hexes = [hex(n)[2::].upper() for n in a]

        # suffix = ['E']*10 + ['F']*16
        # unicodez = [f"\\u1F1{x}{y}" for x,y in zip(suffix, hexes)]

        # return {letter:unicode for letter, unicode in zip(string.ascii_uppercase, unicodez)}

        # Map using ord and the unicode code point rather than the above
        return {letter:chr(ID) for letter, ID in zip(string.ascii_uppercase, range(127462, 127488))}


class Helpers:
    @staticmethod
    def isOwner(user: discord.User) -> bool:
        """
        Check to see if the input User's ID matches the Owner ID
        """
        ownerID = 129606635545952258
        return user.id == ownerID
    
    @staticmethod
    def isDM(channel: discord.TextChannel) -> bool:
        """
        Check to see if a channel is a DM

        A DM is either an instance of DMChannel or GroupChannel
        """
        return isinstance(channel, (discord.DMChannel, discord.GroupChannel))

    def isWumbologist(member: discord.Member) -> bool:
        """
        Check to see if a discord.Member has the 'Wumbologists' role
        """
        return 'Wumbologists' in [str(role) for role in member.roles]


def setup(bot):
    bot.add_cog(MainCommands(bot))

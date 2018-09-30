import logging
import typing

from discord.ext import commands

from bot.utils import Helpers


class ManualCheck:
    @staticmethod
    async def check(ctx: commands.Context, toinvoke: typing.Callable, commandstr: str):
        if Helpers.isDM(ctx.message.channel) and Helpers.isOwner(ctx.message.author):
            logging.info(f"Manual {commandstr} check initiated by {ctx.message.author}")
            await ctx.send(f"Manual {commandstr} parsing starting now...")
            await toinvoke()
        elif Helpers.isOwner(ctx.message.author) and not Helpers.isDM(ctx.message.channel):
            await ctx.send(f'{ctx.message.author.mention}, this command only works in a DM')
        else:
            logging.info(f'Manual {commandstr} check attempted by {ctx.message.author}')
            await ctx.send(f'{ctx.message.author.mention}, you are not authorized to perform this operation')

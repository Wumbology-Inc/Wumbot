import json
import random
import logging
from pathlib import Path

from discord import Game
from discord.ext import commands, tasks


class WumboPresence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.wumbo_JSON = Path("./bot/wumbolist.JSON")
        self.randWumboTimer.start()

    def cog_unload(self):
        self.randWumboTimer.cancel()

    @tasks.loop(hours=1)
    async def randWumboTimer(self):
        """Task loop to automatically update the bot's Now Playing status."""
        wumbogame = Game(name=f"{self.randWumbo(self.wumbo_JSON)}")
        logging.info(f"Changing game to: '{wumbogame.name}'")
        await self.bot.change_presence(activity=wumbogame)

    @randWumboTimer.before_loop
    async def before_rand_wumbo(self):
        await self.bot.wait_until_ready()

    @staticmethod
    def randWumbo(wumbo_JSON: Path = None) -> str:
        """
        Load list of Wumboisms from input JSON file & return a random string from the list.

        If no JSON is input, defaults to 'The Game of Wumbo'
        """
        if wumbo_JSON:
            with wumbo_JSON.open("r") as fID:
                wumbolist = json.load(fID)
                return random.choice(wumbolist)
        else:
            return "The Game of Wumbo"


def setup(bot):
    bot.add_cog(WumboPresence(bot))
    logging.info("WumboPresence Cog loaded")

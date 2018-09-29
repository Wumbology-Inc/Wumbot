import logging
import re

import discord
from discord.ext import commands    


class Amazon():
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        # Avoid self-replies
        if message.author.id == self.bot.user.id:
            return

        # Check for "regular" Amazon link, capture full link & ASIN
        testAmazonASIN = re.search(r'https?.*\/\/.+\.amazon\..+\/([A-Z0-9]{10})\/\S*', message.content, flags=re.IGNORECASE)
        # Check for shortened Amazon link (https://a.co/*), capture full link
        testAmazonShort = re.search(r'https?:\/\/a\.co\S*', message.content, flags=re.IGNORECASE)

def setup(bot):
    bot.add_cog(Amazon(bot))
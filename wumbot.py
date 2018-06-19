import logging
import re
from datetime import datetime

import discord
import git
from discord.ext import commands


class WumbotClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super(WumbotClient, self).__init__(*args, **kwargs)
        self.add_command(self.ver)
        self.add_command(self.uptime)

    async def on_ready(self):
        self.launch_time = datetime.now()
        logging.info(f'Logged in as {self.user}')
        print(f'Logged in as {self.user}')  # Keep print statement for dev debugging

    async def on_message(self, message):
        # Avoid self-replies
        if message.author.id == self.user.id:
            return

        # Hardcode a 'kill' command in a DM to the bot from me
        if isDM(message.channel) and isELA(message.author):
            if message.content == 'kill':
                logging.info('Bot session killed by ELA')
                await message.channel.send('Shutting down... :wave:')
                await self.close()

        if message.content.startswith(self.command_prefix):
            await self.process_commands(message)

        # Check to see if /r/_subreddit (e.g. /r/python) has been typed & add a Reddit embed
        # Ignores regular reddit links (e.g. http://www.reddit.com/r/Python)
        testSubreddit = re.search(r'(?:^|\s)\/?[rR]\/(\w+)', message.content)
        if testSubreddit:
            logging.debug(f"Subreddit detected: '{testSubreddit.group(1)}'")
            logging.debug(f"Message author: {message.author}")
            logging.debug(f"Original message: '{message.content}'")
            SubredditEmbed = buildSubredditEmbed(testSubreddit)
            await message.channel.send(embed=SubredditEmbed)
  
        # Check to see if Reddit's stupid image/video hosting has added 'DashPlaylist.mpd'
        # to the end of the URL, which links to a direct download (of nothing) rather
        # than the web content
        testVreddit = re.search(r'(https?:\/\/v.redd.it\/.*)(DASHPlaylist.*$)', message.content)
        if testVreddit:
            newURL = testVreddit.group(1)
            logging.debug(f"VReddit MPD detected: '{testVreddit.group(0)}'")
            logging.debug(f"Link converted to: {newURL}")
            await message.channel.send(f"Here {message.author.name}, let me fix that v.redd.it link for you: {newURL}")

        # Check for "regular" Amazon link, capture full link & ASIN
        testAmazonASIN = re.search(r'https?.*\/\/.+\.amazon\..+\/([A-Z0-9]{10})\/\S*', message.content, flags=re.IGNORECASE)
        # Check for shortened Amazon link (https://a.co/*), capture full link
        testAmazonShort = re.search(r'https?:\/\/a\.co\S*', message.content, flags=re.IGNORECASE)

    @commands.command()
    async def ver(self, ctx):
        logging.debug('ver command entered')
        currRepo = git.Repo('.')
        repoGit = currRepo.git
        try:
            await ctx.message.channel.send(f'Current Version: {repoGit.describe()}')
        except git.GitCommandError as err:
            await ctx.send('No tags found on current branch')

    @commands.command()
    async def uptime(self, ctx):
        logging.debug('uptime command entered')
        delta_uptime = datetime.utcnow() - self.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"Wumbot has been up for: {days}d {hours}h {minutes}m {seconds}s")

def isELA(user):
    """
    Check to see if the input User's ID matches my ID
    """
    ELAid = 129606635545952258
    return user.id == ELAid

def isDM(channel):
    """
    Check to see if a channel is a DM

    A DM is either an instance of DMChannel or GroupChannel
    """
    return not isinstance(channel, discord.TextChannel)

def buildSubredditEmbed(matchObj):
    """
    Builds a message embed from the input regex match object

    Subreddit string is without /r/

    For now, only utilizes the first match
    """
    subreddit = matchObj.group(1)

    embed = discord.Embed(title=f"/r/{subreddit}", color=discord.Color(0x9c4af7), url=f"https://www.reddit.com/r/{subreddit}")
    embed.set_thumbnail(url="https://b.thumbs.redditmedia.com/5-IE6cGJg-F8IBh3x81hFSJRbfPFDg4FU4Y-RbuNO0Q.png")
    embed.set_author(name="Reddit")

    return embed

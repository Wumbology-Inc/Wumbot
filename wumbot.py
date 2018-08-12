import logging
import re
from datetime import datetime

import discord
from discord.ext import commands


class WumbotClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super(WumbotClient, self).__init__(*args, **kwargs)

    async def on_ready(self):
        self.launch_time = datetime.utcnow()
        logging.info(f'Logged in as {self.user}')
<<<<<<< HEAD
        print(f'Logged in as {self.user}')  # Keep print statement for dev debugging

    async def on_message(self, message):
        # Avoid self-replies
        if message.author.id == self.user.id:
            return

        # Short circuit the rest of the parsing if a command is passed
        if message.content.startswith(self.command_prefix):
            await self.process_commands(message)
            return

        # Check to see if /r/_subreddit (e.g. /r/python) has been typed & add a Reddit embed
        # Ignores regular reddit links (e.g. http://www.reddit.com/r/Python)
        testSubreddit = re.findall(r'(?:^|\s)\/?[rR]\/(\w+)', message.content)
        if testSubreddit:
            logging.info(f"Subreddit(s) detected: '{testSubreddit}'")
            logging.info(f"Original message: '{message.content}'")
            SubredditEmbed = buildSubredditEmbed(testSubreddit)
            await message.channel.send(embed=SubredditEmbed)
  
        # Check to see if Reddit's stupid image/video hosting has added 'DashPlaylist.mpd'
        # to the end of the URL, which links to a direct download (of nothing) rather
        # than the web content
        testVreddit = re.search(r'(https?:\/\/v.redd.it\/.*)(DASHPlaylist.*$)', message.content)
        if testVreddit:
            newURL = testVreddit.group(1)
            logging.info(f"VReddit MPD detected: '{testVreddit.group(0)}'")
            logging.info(f"Link converted to: {newURL}")
            await message.channel.send(f"Here {message.author.name}, let me fix that v.redd.it link for you: {newURL}")

        # Check to see if Reddit's stupid image/video hosting has added 'DashPlaylist.mpd'
        # to the end of the URL, which links to a direct download (of nothing) rather
        # than the web content
        testVreddit = re.search(r'(https?:\/\/v.redd.it\/.*)(DASHPlaylist.*$)', message.content)
        if testVreddit:
            newURL = testVreddit.group(1)
            await message.channel.send(f"Here {message.author.name}, let me fix that v.redd.it link for you: {newURL}")

        # Check for "regular" Amazon link, capture full link & ASIN
        testAmazonASIN = re.search(r'https?.*\/\/.+\.amazon\..+\/([A-Z0-9]{10})\/\S*', message.content, flags=re.IGNORECASE)
        # Check for shortened Amazon link (https://a.co/*), capture full link
        testAmazonShort = re.search(r'https?:\/\/a\.co\S*', message.content, flags=re.IGNORECASE)

    @commands.command()
    async def ver(self, ctx):
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
    async def uptime(self, ctx):
        """
        Reply with current uptime
        """
        delta_uptime = datetime.utcnow() - self.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"Wumbot has been up for: {days}d {hours}h {minutes}m {seconds}s")

    @commands.command()
    async def kill(self, ctx):
        """
        Disconnect bot from Discord

        Only valid if bot owner invokes the command in a DM
        """
        if isDM(ctx.message.channel) and isOwner(ctx.message.author):
            logging.info('Bot session killed by Owner')
            await ctx.send('Shutting down... :wave:')
            await self.close()
        if isOwner(ctx.message.author) and not isDM(ctx.message.channel):
            await ctx.send(f'{ctx.message.author}, this command only works in a DM')
        else:
            logging.info(f'Unauthorized kill attempt by {ctx.message.author}')
            await ctx.send(f'{ctx.message.author}, you are not authorized to perform this operation')

def isOwner(user):
    """
    Check to see if the input User's ID matches the Owner ID
    """
    ownerID = 129606635545952258
    return user.id == ownerID

def isDM(channel):
    """
    Check to see if a channel is a DM

    A DM is either an instance of DMChannel or GroupChannel

    Returns a bool
    """
    return not isinstance(channel, discord.TextChannel)

def buildSubredditEmbed(subredditlist, embedlimit=3):
    """
    Build a message embed from a list of subreddit strings (sans '/r/')

    Limit to embedlimit number of subreddits per embed, for brevity. Default is 3
    """
    snooURL = "https://images-eu.ssl-images-amazon.com/images/I/418PuxYS63L.png"

    embed = discord.Embed(color=discord.Color(0x9c4af7))
    embed.set_thumbnail(url=snooURL)
    embed.set_author(name='Subreddit Embedder 9000')
    embed.set_footer(text='Reddit', icon_url=snooURL)

    if len(subredditlist) == 1:
        embed.description = "Subreddit detected!"
        subreddit = subredditlist[0]
        embed.add_field(name=f"/r/{subreddit}", value=f"https://www.reddit.com/r/{subreddit}", inline=False)
    else:
        embed.description = "Subreddits detected!"
        for subreddit in subredditlist[0:fieldlimit]:
            embed.add_field(name=f"/r/{subreddit}", value=f"https://www.reddit.com/r/{subreddit}", inline=False)
        
        if len(subredditlist) > embedlimit:
            embed.add_field(name="Note:", value=f"For brevity, only {embedlimit} subreddits have been embedded. You linked {len(subredditlist)}")

    return embed
=======
        print(f'Logged in as {self.user}')  # Keep print statement for dev debugging
>>>>>>> develop

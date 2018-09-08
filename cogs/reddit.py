import logging
import re
import typing
from datetime import datetime

import discord
from discord.ext import commands


class RedditPost:
    def __init__(self, inJSON:typing.Dict):
        # Submission type prefixes, per Reddit's API: https://www.reddit.com/dev/api/
        _types = {'t1':'comment', 't2': 'account', 't3': 'link', 
                  't4': 'message', 't5': 'subreddit', 't6': 'award'}
        self._kind = inJSON['kind']  # Retain original
        self.kind = _types[self._kind]

        # Pull global post ID, tx_yyyy, where tx is the post type and yyyy is Base36 encoded ID
        self._fullid = inJSON['data']['name']  # Retain original
        self.id = self._fullid.split('_')[1]

        self.subreddit = inJSON['data']['subreddit']
        self.title = inJSON['data']['title']
        self.createdUTC = datetime.utcfromtimestamp(inJSON['data']['created_utc'])
        self.contentURL = inJSON['data']['url']
        self.permalink = f"https://www.reddit.com{inJSON['data']['permalink']}"
        
    def __repr__(self):
        return f"{self.title}: {self.permalink}"


class Reddit():
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def buildSubredditEmbed(subredditlist: typing.List[str], embedlimit: int=3):
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
            for subreddit in subredditlist[0:embedlimit]:
                embed.add_field(name=f"/r/{subreddit}", value=f"https://www.reddit.com/r/{subreddit}", inline=False)
            
            if len(subredditlist) > embedlimit:
                embed.add_field(name="Note:", value=f"For brevity, only {embedlimit} subreddits have been embedded. You linked {len(subredditlist)}")

        return embed

    async def on_message(self, message: discord.Message):
        # Avoid self-replies
        if message.author.id == self.bot.user.id:
            return

        # Check to see if /r/_subreddit (e.g. /r/python) has been typed & add a Reddit embed
        # Ignores regular reddit links (e.g. http://www.reddit.com/r/Python)
        testSubreddit = re.findall(r'(?:^|\s)\/?[rR]\/(\w+)', message.content)
        if testSubreddit:
            logging.info(f"Subreddit(s) detected: '{testSubreddit}'")
            logging.info(f"Original message: '{message.content}'")
            SubredditEmbed = self.buildSubredditEmbed(testSubreddit)
            await message.channel.send(embed=SubredditEmbed)
  
        # Check to see if Reddit's stupid image/video hosting has added 'DashPlaylist.mpd'
        # to the end of the URL, which links to a direct download (of nothing) rather
        # than the web content
        testVreddit = re.search(r'(https?:\/\/v.redd.it\/.*)(DASHPlaylist.*$)', message.content)
        if testVreddit:
            newURL = testVreddit.group(1)
            logging.info(f"VReddit MPD detected: '{testVreddit.group(0)}'")
            logging.info(f"Link converted to: {newURL}")
            await message.channel.send(f"Here {message.author.mention}, let me fix that v.redd.it link for you: {newURL}")


def setup(bot):
    bot.add_cog(Reddit(bot))
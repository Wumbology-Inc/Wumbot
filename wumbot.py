import re

import discord

class WumbotClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        # Avoid self-replies
        if message.author.id == self.user.id:
            return

        # Hardcode a 'kill' command in a DM to the bot from me
        if isDM(message.channel) and isELA(message.author):
            if message.content == 'kill':
                print('ELA killed me')
                await message.channel.send('Shutting down... :wave:')
                await self.close()

        # Check to see if /r/_subreddit (e.g. /r/python) has been typed & add a Reddit embed
        # Ignores regular reddit links (e.g. http://www.reddit.com/r/Python)
        testSubreddit = re.search(r'\B\/?[rR]\/(\w+)', message.content)
        if testSubreddit:
            SubredditEmbed = buildSubredditEmbed(testSubreddit)
            await message.channel.send(embed=SubredditEmbed)

        # Check for "regular" Amazon link, capture full link & ASIN
        testAmazonASIN = re.search(r'https?.*\/\/.+\.amazon\..+\/([A-Z0-9]{10})\/\S*', message.content, flags=re.IGNORECASE)
        # Check for shortened Amazon link (https://a.co/*), capture full link
        testAmazonShort = re.search(r'https?:\/\/a\.co\S*', message.content, flags=re.IGNORECASE)
        

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

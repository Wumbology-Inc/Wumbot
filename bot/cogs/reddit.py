import logging
import re
import typing

import discord
import requests
from yarl import URL


class Reddit:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def buildSubredditEmbed(subredditlist: typing.List[str], embedlimit: int = 3):
        """
        Build a message embed from a list of subreddit strings (sans '/r/')

        Limit to embedlimit number of subreddits per embed, for brevity. Default is 3
        """
        snooURL = "https://images-eu.ssl-images-amazon.com/images/I/418PuxYS63L.png"

        embed = discord.Embed(color=discord.Color(0x9C4AF7))
        embed.set_thumbnail(url=snooURL)
        embed.set_author(name="Subreddit Embedder 9000")
        embed.set_footer(text="Reddit", icon_url=snooURL)

        if len(subredditlist) == 1:
            embed.description = "Subreddit detected!"
            subreddit = subredditlist[0]
            embed.add_field(
                name=f"/r/{subreddit}",
                value=f"https://www.reddit.com/r/{subreddit}",
                inline=False,
            )
        else:
            embed.description = "Subreddits detected!"
            for subreddit in subredditlist[0:embedlimit]:
                embed.add_field(
                    name=f"/r/{subreddit}",
                    value=f"https://www.reddit.com/r/{subreddit}",
                    inline=False,
                )

            if len(subredditlist) > embedlimit:
                embed.add_field(
                    name="Note:",
                    value=(
                        f"For brevity, only {embedlimit} subreddits have been embedded. "
                        f"You linked {len(subredditlist)}"
                    ),
                )

        return embed

    async def on_message(self, message: discord.Message):
        """
        Check messages for:

           1. Subreddit reference (/r/subreddit) and reply with a link embed
              Invalid subreddits are ignored
           2. Reddit's image/video hosting adding 'DashPlaylist.mpd' to the end of the file, which
              links to nothing. Reply with a link embed to the media without the suffix
        """
        # Avoid self-replies
        if message.author.id == self.bot.user.id:
            return

        # Check to see if /r/_subreddit (e.g. /r/python) has been typed & add a Reddit embed
        # Ignores regular reddit links (e.g. http://www.reddit.com/r/Python)
        testSubreddit = re.findall(r"(?:^|\s)\/?[rR]\/(\w+)", message.content)
        if testSubreddit:
            logging.info(f"Subreddit(s) detected: '{testSubreddit}'")
            logging.info(f"Original message: '{message.content}'")
            subreddits = [
                subreddit
                for subreddit in testSubreddit
                if self._isvalidsubreddit(subreddit)
            ]
            if subreddits:
                SubredditEmbed = self.buildSubredditEmbed(testSubreddit)
                await message.channel.send(embed=SubredditEmbed)

        # Check to see if Reddit's stupid image/video hosting has added 'DashPlaylist.mpd'
        # to the end of the URL, which links to a direct download (of nothing) rather
        # than the web content
        testVreddit = re.search(
            r"(https?:\/\/v.redd.it\/.*)(DASHPlaylist.*$)", message.content
        )
        if testVreddit:
            newURL = testVreddit.group(1)
            logging.info(f"VReddit MPD detected: '{testVreddit.group(0)}'")
            logging.info(f"Link converted to: {newURL}")
            await message.channel.send(
                f"Here {message.author.mention}, let me fix that v.redd.it link for you: {newURL}"
            )

    @staticmethod
    def _isvalidsubreddit(subreddit: str) -> bool:
        """
        Return True if subreddit resolves to a valid Reddit subreddit, else return False

        If the JSON request times out or is API throttled, True is returned as a fallback
        """
        baseURL = URL("https://old.reddit.com/")
        testURL = baseURL.with_path(f"/r/{subreddit}.json")

        headers = {"user-agent": "Wumbot JSON Fallback"}
        r = requests.get(testURL, headers=headers).json()
        try:
            msg = r["message"]
            if msg.lower() == "not found":
                logging.info(f"Invalid subreddit detected: '{subreddit}'")
                return False
            else:
                logging.info(f"Unhandled Reddit response: '{msg}'")
                return True
        except KeyError:
            return True


def setup(bot):
    bot.add_cog(Reddit(bot))

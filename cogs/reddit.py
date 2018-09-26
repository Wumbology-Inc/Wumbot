from __future__ import annotations

import json
import logging
import re
import typing
from datetime import datetime
from pathlib import Path

import aiohttp
import discord
import praw
import requests
from discord.ext import commands
from yarl import URL


class RedditPost:
    def __init__(self, subreddit: str=None, id: str=None, created_utc: float=None, title: str=None, 
                 url: str=None, permalink: str=None, author: str=None, **kwargs
                 ):
        """
        Helper object to represent a Reddit Submission
        """
        self.subreddit = subreddit
        self.id = id
        self.created_utc = datetime.utcfromtimestamp(created_utc)
        self.title = title
        self.contentURL = URL(url)
        self.permalink = URL('https://old.reddit.com').with_path(permalink)
        self.author = author

    def __repr__(self):
        return f"{self.title}: {self.permalink}"

    @staticmethod
    def fromJSON(inJSON: dict) -> RedditPost:
        """
        Generate RedditPost from a Reddit submission JSON (as dict)
        """
        return RedditPost(**inJSON['data'])

    @staticmethod
    def fromPRAW(inSub: praw.Submission) -> RedditPost:
        """
        Generate RedditPost from a PRAW Submission
        """
        # Because PRAW does lazy objects, only pull the desired attributes
        submissiondict = {'subreddit': inSub.subreddit, 'id': inSub.id,
                          'created_utc': inSub.created_utc, 'title': inSub.title,
                          'url': inSub.url, 'permalink': inSub.permalink,
                          'author': inSub.author
                          }
        return RedditPost(**submissiondict)


class RedditPRAW:
    def __init__(self, credentialJSON: Path=Path('./credentials.JSON')):
        credentials = RedditPRAW._loadCredentials(credentialJSON)
        self.session = praw.Reddit(client_id=credentials[0], client_secret=credentials[1],
                                user_agent='Wumbot PRAW Agent')
        
        # Try to get some submissions to check for correct authentication
        self.isauthenticated = True
        try:
            _ = self.session.subreddit('python').hot(limit=1)
        except praw.exceptions.ResponseException as e:
            self.isauthenticated = False

        if self.isauthenticated:
            logging.info("Successful PRAW authentication")
        else:
            logging.info(f"PRAW received invalid credentials from '{credentialJSON}'")

    @staticmethod
    def _loadCredentials(credentialJSON: Path) -> str:
        """
        Load login credentials from the input JSON file
        """
        with open(credentialJSON, mode='r') as fID:
            credentials = json.load(fID)

        return credentials['RedditOAuth']


class RedditJSON():
    """
    Helper class for Reddit JSON methods
    """
    @staticmethod
    async def asyncfromJSON(jsonURL: typing.Union[str, URL]=None, skipvalidation: bool=False) -> typing.List:
        """
        This function is a coroutine

        Return a list of RedditPost from an input Reddit JSON URL

        Supported URL schemas are:
            https://old.reddit.com/u(ser)/username/submitted(/).json
            https://old.reddit.com/r/subreddit(/).json
            https://old.reddit.com/r/subreddit/comments/*(/).json

        Other input URL formats are not supported

        The skipvalidation flag allows you to skip the URL validation if it has already
        been validated
        """
        if not skipvalidation:
            jsonURL = RedditJSON._validateURL(jsonURL, checkJSON=True)

        headers = {'user-agent': 'Wumbot JSON Fallback'}
        async with aiohttp.ClientSession() as session:
            async with session.get(jsonURL, headers=headers) as resp:
                jsonresponse = await resp.json()
    
        if isinstance(jsonresponse, list):
            # Reddit Post JSON contains a list of 2 dicts, one for the post and one for the comments
            # Comments are ignored for now
            postlist = jsonresponse[0]['data']['children']
        else:
            # Everything else should just be a bare dictionary
            postlist = jsonresponse['data']['children']
            
        return [RedditPost.fromJSON(post) for post in postlist]

    @staticmethod
    async def asyncfromURL(inURL: str=None) -> typing.List:
        """
        This function is a coroutine

        Return a list of RedditPost objects from an input Reddit URL

        Supported URL schemas are:
            https://old.reddit.com/u(ser)/username/submitted(/)
            https://old.reddit.com/r/subreddit(/)
            https://old.reddit.com/r/subreddit/comments/*

        Other input URL formats are not supported

        The skipvalidation flag allows you to skip the URL validation if it has already
        been validated
        """
        inURL = RedditJSON._validateURL(inURL, checkJSON=False)
        if RedditJSON._isredditJSON(inURL):
            return await RedditJSON.asyncfromJSON(inURL, skipvalidation=True)
        else:
            return await RedditJSON.asyncfromJSON(URL(inURL.human_repr() + '.json'), skipvalidation=True)

    @staticmethod
    def fromJSON(jsonURL: typing.Union[str, URL]=None, skipvalidation: bool=False) -> typing.List:
        """
        Return a list of RedditPost from an input Reddit JSON URL

        Supported URL schemas are:
            https://old.reddit.com/u(ser)/username/submitted(/).json
            https://old.reddit.com/r/subreddit(/).json
            https://old.reddit.com/r/subreddit/comments/*(/).json

        Other input URL formats are not supported
        """
        if not skipvalidation:
            jsonURL = RedditJSON._validateURL(jsonURL, checkJSON=True)

        headers = {'user-agent': 'Wumbot JSON Fallback'}
        jsonresponse = requests.get(jsonURL, headers=headers).json()
        if isinstance(jsonresponse, list):
            # Reddit Post JSON contains a list of 2 dicts, one for the post and one for the comments
            # Comments are ignored for now
            postlist = jsonresponse[0]['data']['children']
        else:
            # Everything else should just be a bare dictionary
            postlist = jsonresponse['data']['children']
            
        return [RedditPost.fromJSON(post) for post in postlist]
    
    @staticmethod
    def fromURL(inURL: typing.Union[str, URL]=None) -> typing.List:
        """
        Return a list of RedditPost objects from an input Reddit URL

        Supported URL schemas are:
            https://old.reddit.com/u(ser)/username/submitted(/)
            https://old.reddit.com/r/subreddit(/)
            https://old.reddit.com/r/subreddit/comments/*

        Other input URL formats are not supported
        """
        inURL = RedditJSON._validateURL(inURL, checkJSON=False)

        if RedditJSON._isredditJSON(inURL):
            return RedditJSON.fromJSON(inURL, skipvalidation=True)
        else:
            return RedditJSON.fromJSON(URL(inURL.human_repr() + '.json'), skipvalidation=True)
    
    @staticmethod
    def _validateURL(inURL: typing.Union[URL, str], checkJSON: bool=True) -> URL:
        """
        Perform some rudimentary Reddit URL validation for the class' methods

        Raises a ValueError if a URL is not provided or if a Reddit user link is provided that
        is not the user's submissions. The checkJSON flag can be set to check whether the URL 
        suffix is .json

        Returns a yarl.URL if the checks pass
        """
        if not inURL:
            raise ValueError("No URL provided")

        inURL = URL(inURL)

        if RedditJSON._isusernonsubmission(inURL):
            raise ValueError(f"Unsupported Reddit User link: '{inURL}'\nOnly user submissions are supported")

        if checkJSON:
            if not RedditJSON._isredditJSON(inURL):
                raise ValueError(f"Invalid Reddit JSON URL provided: '{inURL}'\nURLs must end with '.json'")

        return inURL

    @staticmethod
    def _isredditJSON(inURL: URL=None) -> bool:
        if not inURL:
            raise ValueError("No URL provided")
        if not isinstance(inURL, URL):
            raise TypeError(f"Invalid URL type: '{type(inURL)}', input must be yarl.URL")
        
        # Check to see if '.json' is already appended
        return '.json' in inURL.parts[-1].lower()

    @staticmethod
    def _isusernonsubmission(inURL: URL=None) -> bool:
        """
        Test Reddit URL for valid User link construction

        Return True if the URL is a Reddit user URL that is not their submissions
        e.g. https://old.reddit.com/user/username/comments/ or https://old.reddit.com/u/username/

        Otherwise, return False
        """
        if not inURL:
            raise ValueError("No URL provided")
        if not isinstance(inURL, URL):
            raise TypeError(f"Invalid URL type: '{type(inURL)}', input must be yarl.URL")

        expr = r'/u(?:ser)?/\w+'
        urlparts = inURL.path.lower()
        if re.search(expr, urlparts):
            return 'submitted' not in urlparts
        else:
            return False


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

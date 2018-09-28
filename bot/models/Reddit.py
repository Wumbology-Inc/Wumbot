from __future__ import annotations

import json
import logging
import re
import typing
from datetime import datetime
from pathlib import Path

import aiohttp
import praw
import requests
from yarl import URL


class RedditPost:
    def __init__(self, subreddit: str=None, id: str=None, created_utc: float=None, title: str=None, 
                 url: str=None, permalink: str=None, author: str=None, **kwargs
                 ):
        """
        Helper object to represent a Reddit Submission

        To simplify construction from Reddit's JSON return, additional keyword arguments
        are accepted but discarded
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
        Generate RedditPost from a PRAW Submission object
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
        """
        Helper class for PRAW instance

        On instantiation, an attempt is made to authenticate using the input credential JSON
        Credential JSON should contain a 'RedditOAuth' key with a (ID, secret) tuple

        The isauthenticated attribute can be queried to determine authentication status
        """
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

    def getnewusersubmissions(self, username: str, limit: int=25) -> praw.models.ListingGenerator:
        """
        Return a praw.ListingGenerator of username's newest Reddit submissions

        API call can be limited to a number of submissions, as specified by limit
        """
        # Strip out /u/ or u/ from the username
        exp = r"/?u/"
        username = re.sub(exp, '', username)

        return self.session.redditor(username).submissions.new(limit=limit)

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
        """
        Check to see if link ends with .json
        """
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

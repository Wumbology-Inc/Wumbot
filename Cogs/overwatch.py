import typing
from datetime import datetime
from pathlib import Path

import aiohttp


class PatchParser:
    def __init__(self):
        self.postjsonURL = "https://www.reddit.com/user/itsjieyang/submitted.json"
        self.localpostedgifJSON = Path('./postedOWpatchgifs')

    async def getpatchgifs(self, jsonURL: str=None):
        """
        Return a list of RedditPost objects generated from Patch Notes submissions by /u/itsjieyang to /r/Overwatch
        """
        jsonURL = jsonURL if jsonURL is not None else self.postjsonURL
        async with aiohttp.ClientSession() as session:
            async with session.get(jsonURL) as resp:
                rawdict = await resp.json()
                submissions = rawdict['data']['children']

        patchposts = []
        for postjson in submissions:
            postobj = RedditPost(postjson)

            # So far, patch notes GIFs we want are from /r/Overwatch and start with "patch"
            if postobj.subreddit == 'Overwatch' and postobj.title.lower().startswith('patch'):
                patchposts.append(postobj)

        return patchposts

    async def loadposted(self, filepath: Path=None):
        # TODO: Link to Postgres DB
        filepath = filepath if filepath is not None else self.localpostedgifJSON
        raise NotImplementedError

    async def saveposted(self, filepath: Path=None):
        # TODO: Link to Postgres DB
        filepath = filepath if filepath is not None else self.localpostedgifJSON
        raise NotImplementedError
        
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

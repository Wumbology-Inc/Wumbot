import json
import typing
from datetime import datetime

import aiohttp


class PatchParser:
    async def getpatchgifs(self, jsonURL: str="https://www.reddit.com/user/itsjieyang/submitted.json"):
        async with aiohttp.ClientSession() as session:
            async with session.get(jsonURL) as resp:
                rawdict = await resp.json()
                submissions = rawdict['data']['children']

        for postjson in submissions:
            postobj = RedditPost(postjson)

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
        self.permalink = inJSON['data']['permalink']

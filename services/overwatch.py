import json
import typing
from datetime import datetime
from pathlib import Path

import aiohttp
import discord


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

class PatchParser:
    def __init__(self, bot):
        self.bot = bot
        self.postjsonURL = "https://www.reddit.com/user/itsjieyang/submitted.json"
        self.postchannelID = 477916849879908386
        self.logJSONpath = Path('./log/postedGIFs.JSON')
        self.postedGIFs = None

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

    async def postpatchgif(self, channelID: int=None, postobj: RedditPost=None):
        channelID = channelID if channelID is not None else self.postchannelID

        if postobj is None or not isinstance(postobj, RedditPost):
            raise ValueError

        postchannel = self.bot.get_channel(channelID)
        # TODO: Add more verbose message (embed?)
        await postchannel.send(discord.Message())

    def loadposted(self, logJSONpath: Path=None):
        logJSONpath = logJSONpath if logJSONpath is not None else self.logJSONpath
        
        if logJSONpath.exists():
            with logJSONpath.open(mode='r') as fID:
                self.postedGIFs = json.load(fID)

    def saveposted(selfself, logJSONpath: Path=None):
        logJSONpath = logJSONpath if logJSONpath is not None else self.logJSONpath
        
        if self.postedGIFs:
            with logJSONpath.open(mode='w') as fID:
                json.dump([post[contentURL] for post in self.postedlogs], fID)

    async def patchcheck(self):
        self.loadposted()

        posts = await self.getpatchgifs()
        newposts = [post for post in posts if post not in self.postedGIFs]
        for post in newposts:
            await self.postpatchgif(post)
            self.postedGIFs.append(post)
        
        self.saveposted()


def patchchecktimer(client, sleepseconds=3600):
    await self.bot.wait_until_ready()

    p = PatchParser(client)
    while not self.bot.is_closed():
        await p.patchcheck()

        await asyncio.sleep(sleepseconds)

def setup(bot):
    bot.add_cog(PatchParser(bot))
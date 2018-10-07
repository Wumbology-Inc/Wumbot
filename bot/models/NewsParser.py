import asyncio
import json
import logging
import typing
from pathlib import Path


class NewsParser:
    def __init__(self, bot):
        self.bot = bot
        self.postednews = []

        self._parsername = None
        self._loadconverter = None
        self._saveconverter = None

    def loadposted(self):
        if self.logJSONpath.exists():
            with self.logJSONpath.open(mode="r") as fID:
                savednews = [self._loadconverter(post) for post in json.load(fID)]

            if savednews:
                self.postednews = savednews
                logging.info(
                    f"Loaded {len(self.postednews)} {self._parsername} from '{self.logJSONpath}'"
                )
            else:
                logging.info(f"No posted {self._parsername} found in JSON log")
        else:
            logging.info(f"{self._parsername} log JSON does not yet exist")

    def saveposted(self):
        if self.postednews:
            with self.logJSONpath.open(mode="w") as fID:
                json.dump([self._saveconverter(post) for post in self.postednews], fID)
            logging.info(f"Saved {len(self.postednews)} {self._parsername} post(s)")
        else:
            logging.info(f"No {self._parsername} to save")

    async def patchcheck(self, posts):
        logging.info(f"{self._parsername} check coroutine invoked")
        self.loadposted()

        newposts = [
            post
            for post in posts
            if getattr(post, self._comparator) not in self.postednews
        ]
        logging.info(f"Found {len(newposts)} new {self._parsername} to post")

        if newposts:
            for post in reversed(
                newposts
            ):  # Attempt to get close to posting in chronological order
                await self.postembed(post)
                self.postednews.append(
                    self._loadconverter(getattr(post, self._comparator))
                )

            self.saveposted()


async def patchchecktimer(client, parsers: typing.Tuple = (), sleepseconds: int = 3600):
    await client.wait_until_ready()
    while not client.is_closed():
        for p in parsers:
            await p.patchcheck()

        await asyncio.sleep(sleepseconds)

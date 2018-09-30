import asyncio
import json
import logging
import typing
from pathlib import Path


class NewsParser:
    def __init__(self, bot):
        self.bot = bot
        self.postednews = []

    def loadposted(self, logJSONpath: Path=None, converter: typing.Callable=str):
        logJSONpath = logJSONpath if logJSONpath is not None else self.logJSONpath
        
        if logJSONpath.exists():
            with logJSONpath.open(mode='r') as fID:
                savednews = [converter(post) for post in json.load(fID)]
            
            if savednews:
                self.postednews = savednews
                logging.info(f"Loaded {len(self.postednews)} {self.parsername} from '{logJSONpath}'")
            else:
                logging.info(f"No posted {self.parsername} found in JSON log")
        else:
            logging.info(f"{self.parsername} log JSON does not yet exist")

    def saveposted(self, logJSONpath: Path=None, converter: typing.Callable=str):
        logJSONpath = logJSONpath if logJSONpath is not None else self.logJSONpath
        
        if self.postednews:
            with logJSONpath.open(mode='w') as fID:
                json.dump([converter(post) for post in self.postednews], fID)
            logging.info(f"Saved {len(self.postednews)} {self.parsername} post(s)")
        else:
            logging.info(f"No {self.parsername} to save")

async def patchchecktimer(client, parsers: typing.Tuple=(), sleepseconds: int=3600):
    await client.wait_until_ready()
    while not client.is_closed():
        for p in parsers:
            await p.patchcheck()
            
        await asyncio.sleep(sleepseconds)

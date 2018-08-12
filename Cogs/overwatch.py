import json

import aiohttp


class PatchParser:
    async def getpatchgifs(self, jsonURL="https://www.reddit.com/user/itsjieyang/submitted.json":str):
        async with aiohttp.ClientSession() as session:
            async with session.get(jsonURL) as resp:
                rawdict = await resp.json()
                submissions = rawdict['data']['children']


import asyncio
import typing

class NewsParser:
    def __init__():
        raise NotImplementedError

async def patchchecktimer(client, parsers: typing.Tuple=(), sleepseconds: int=3600):
    await client.wait_until_ready()
    while not client.is_closed():
        for p in parsers:
            await p.patchcheck()
            
        await asyncio.sleep(sleepseconds)
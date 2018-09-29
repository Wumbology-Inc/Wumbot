import asyncio
import json
import random
import logging

from discord import Game

def randWumbo(wumboJSON=None) -> str:
    """
    Load list of Wumboisms from input JSON file & return a random string from the list

    If no JSON is input, defaults to 'The Game of Wumbo'
    """
    if wumboJSON:
        with open(wumboJSON, mode='r') as fID:
            wumbolist = json.load(fID)
            return random.choice(wumbolist)
    else:
        return 'The Game of Wumbo'

async def randWumboTimer(client, sleepseconds=3600, wumboJSON=None):
    """
    Async sleep timer to automatically update the bot's Now Playing status
    """
    await client.wait_until_ready()
    while not client.is_closed():
        wumbogame = Game(name=f"{randWumbo(wumboJSON)}")

        logging.debug(f"Changing game to: '{wumbogame.name}'")
        await client.change_presence(activity=wumbogame)
        await asyncio.sleep(sleepseconds)
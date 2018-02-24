import asyncio
import random
import json

from wumbot import WumbotClient
from discord import Game

client = WumbotClient()

def randWumbo(wumboJSON=None):
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

async def randWumboTimer(sleepseconds=3600, wumboJSON=None):
    """
    Async sleep timer to automatically update the bot's Now Playing status
    """
    await client.wait_until_ready()
    while not client.is_closed():
        wumbogame = Game(name=f"{randWumbo(wumboJSON)}")

        await client.change_presence(game=wumbogame)
        await asyncio.sleep(sleepseconds)

def loadCredentials(credentialJSON):
    """
    Load login credentials from the input JSON file
    """
    with open(credentialJSON, mode='r') as fID:
        credentials = json.load(fID)

    return credentials

credentials = loadCredentials('credentials.JSON')
if credentials:
    client.loop.create_task(randWumboTimer(wumboJSON='wumbolist.JSON'))
    client.run(credentials['TOKEN'])
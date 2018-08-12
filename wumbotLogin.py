import asyncio
import json
import logging
import random
import time

from discord import Game

from wumbot import WumbotClient


# Force UTC Timestamps
# From the logging cookbook: https://docs.python.org/3/howto/logging-cookbook.html
class UTCFormatter(logging.Formatter):
    converter = time.gmtime

logformat = '%(asctime)s %(levelname)s:%(module)s:%(message)s'
dateformat = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(filename='./log/wumbot.log', filemode='a', level=logging.INFO, 
                    format=logformat, datefmt=dateformat
                    )

client = WumbotClient(command_prefix='~')

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

        logging.debug(f"Changing game to: '{wumbogame.name}'")
        await client.change_presence(activity=wumbogame)
        await asyncio.sleep(sleepseconds)

def loadCredentials(credentialJSON):
    """
    Load login credentials from the input JSON file
    """
    with open(credentialJSON, mode='r') as fID:
        credentials = json.load(fID)

    return credentials

credentialpath = './credentials.JSON'
credentials = loadCredentials(credentialpath)
if credentials:
    # Load cogs
    client.load_extension("cogs.overwatch")
    client.load_extension("cogs.bot")
    client.load_extension("cogs.reddit")

    # Setup event loops
    client.loop.create_task(randWumboTimer(wumboJSON='wumbolist.JSON'))

    client.run(credentials['TOKEN'])
else:
    logging.info(f"Credential file empty: {credentialpath}")
    raise EnvironmentError
import json
import logging
import time
from datetime import datetime

from discord.ext import commands

from .cogs import mhw, overwatch, rocketleague, wumbopresence


class WumbotClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super(WumbotClient, self).__init__(*args, **kwargs)

    async def on_ready(self):
        self.launch_time = datetime.utcnow()
        logging.info(f'Logged in as {self.user}')
        print(f'Logged in as {self.user}')  # Keep print statement for dev debugging

def loadCredentials(credentialJSON) -> str:
    """
    Load login credentials from the input JSON file
    """
    with open(credentialJSON, mode='r') as fID:
        credentials = json.load(fID)

    return credentials['DiscordToken']

credentialpath = './credentials.JSON'
credentials = loadCredentials(credentialpath)
if credentials:
    client = WumbotClient(command_prefix='~')
    
    # Load cogs
    client.load_extension("bot.cogs.bot")
    client.load_extension("bot.cogs.reddit")
    client.load_extension("bot.cogs.overwatch")
    client.load_extension("bot.cogs.mhw")
    client.load_extension("bot.cogs.rocketleague")

    # Setup event loops
    client.loop.create_task(wumbopresence.randWumboTimer(client, wumboJSON='./bot/wumbolist.JSON'))
    client.loop.create_task(overwatch.patchchecktimer(client))
    client.loop.create_task(mhw.patchchecktimer(client))
    client.loop.create_task(rocketleague.patchchecktimer(client))

    # Finally, try to log in
    client.run(credentials)
else:
    logging.info(f"Credential file empty: {credentialpath}")
    raise EnvironmentError

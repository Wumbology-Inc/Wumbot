import json
import logging
import time
from datetime import datetime

from discord.ext import commands

from services import overwatch, wumbopresence


# Force UTC Timestamps
# From the logging cookbook: https://docs.python.org/3/howto/logging-cookbook.html
class UTCFormatter(logging.Formatter):
    converter = time.gmtime

logformat = '%(asctime)s %(levelname)s:%(module)s:%(message)s'
dateformat = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(filename='./log/wumbot.log', filemode='a', level=logging.INFO, 
                    format=logformat, datefmt=dateformat
                    )
class WumbotClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super(WumbotClient, self).__init__(*args, **kwargs)

    async def on_ready(self):
        self.launch_time = datetime.utcnow()
        logging.info(f'Logged in as {self.user}')
        print(f'Logged in as {self.user}')  # Keep print statement for dev debugging

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
    client = WumbotClient(command_prefix='~')
    
    # Load cogs
    client.load_extension("cogs.bot")
    client.load_extension("cogs.reddit")

    # Setup event loops
    client.loop.create_task(wumbopresence.randWumboTimer(client, wumboJSON='wumbolist.JSON'))
    
    p = overwatch.PatchParser(client)
    client.loop.create_task(p.patchcheckloop())

    # Finally, try to log in
    client.run(credentials['TOKEN'])
else:
    logging.info(f"Credential file empty: {credentialpath}")
    raise EnvironmentError

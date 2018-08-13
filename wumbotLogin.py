import json
import logging
import time

from services import overwatch, wumbopresence
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
    client.load_extension("cogs.bot")
    client.load_extension("cogs.reddit")

    # Setup event loops
    client.loop.create_task(wumbopresence.randWumboTimer(client, wumboJSON='wumbolist.JSON'))
    
    p = overwatch.PatchParser(client)
    client.loop.create_task(p.patchcheckloop())

    client.run(credentials['TOKEN'])
else:
    logging.info(f"Credential file empty: {credentialpath}")
    raise EnvironmentError

import json
import logging
from datetime import datetime

from discord.ext import commands


class WumbotClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super(WumbotClient, self).__init__(*args, **kwargs)

    async def on_ready(self):
        self.launch_time = datetime.utcnow()
        logging.info(f"Logged in as {self.user}")
        print(f"Logged in as {self.user}")  # Keep print statement for dev debugging


def loadCredentials(credentialJSON) -> str:
    """
    Load login credentials from the input JSON file
    """
    with open(credentialJSON, mode="r") as fID:
        credentials = json.load(fID)

    return credentials["DiscordToken"]


credentialpath = "./credentials.JSON"
credentials = loadCredentials(credentialpath)
if credentials:
    client = WumbotClient(
        command_prefix=commands.when_mentioned_or("~"), case_insensitive=True
    )

    # Load cogs
    client.load_extension("bot.cogs.bot")
    client.load_extension("bot.cogs.reddit")
    client.load_extension("bot.cogs.overwatch")
    client.load_extension("bot.cogs.wumbopresence")

    # Finally, try to log in
    client.run(credentials)
else:
    logging.info(f"Credential file empty: {credentialpath}")
    raise EnvironmentError

import json

import discord


class WumbotClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        # Avoid self-replies
        if message.author.id == self.user.id:
            return

        # Hardcode a 'kill' command in a DM to the bot from me
        if isDM(message.channel) and isELA(message.author):
            if message.content == 'kill':
                print('ELA killed me')
                await self.close()

def isELA(user):
    """
    Check to see if the input User's ID matches my ID
    """
    ELAid = 129606635545952258
    if user.id == ELAid:
        return True
    else:
        return False


def isDM(channel):
    """
    Check to see if a channel is a DM

    A DM is either an instance of DMChannel or GroupChannel
    """
    if isinstance(channel, discord.TextChannel):
        return False
    else:
        return True

def loadCredentials(sourceJSON):
    """
    Load login credentials from the input JSON file
    """
    with open(sourceJSON, mode='r') as fID:
        credentials = json.load(fID)

    return credentials

credentials = loadCredentials('credentials.JSON')
if credentials:
    wumbogame = discord.Game(name='The Game of Wumbo')
    client = WumbotClient(game=wumbogame)
    client.run(credentials['TOKEN'])

import json
import discord

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


with open('credentials.JSON', mode='r') as fID:
    credentials = json.load(fID)

client.run(credentials['TOKEN'])
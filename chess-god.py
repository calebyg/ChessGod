from dotenv import load_dotenv

import discord
import os

load_dotenv() # import variables from .env
token = os.environ.get("api-token")

intents = discord.Intents.all()
client = discord.Client(command_prefix = '!', intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('hi'):
        await message.channel.send('Hello!')

client.run(token)
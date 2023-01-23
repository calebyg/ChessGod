import os

from discord.ext import commands
from dotenv import load_dotenv
from chessdotcom import get_player_profile

load_dotenv() # import variables from .env
token = os.environ.get("api-token")
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    message.content = message.content.lower() # makes all messages lowercase
    if message.author == bot.user:
        return
    if "hi" in message.content:
        await message.channel.send('Hello!') # response

    await bot.process_commands(message) # necessary to accept commands from users

# Commands

# Returns the full name of the chess username argument
# ex: $name fabianocaruana - Fabiano Caruana
@bot.command(aliases=['username'])
async def name(ctx, arg):
    response = get_player_profile(arg)
    await ctx.send(f'Name: {response.player.name}')

bot.run(token)

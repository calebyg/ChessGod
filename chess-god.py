import os
import json

from discord.ext import commands
from dotenv import load_dotenv
from chessdotcom import get_player_profile, get_player_stats

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

# Returns the full name of a chess.com account
# ex: $name fabianocaruana - Fabiano Caruana
@bot.command(aliases=['username'])
async def name(ctx, name_input):
    try:
        response = get_player_profile(name_input)
        player_name = response.player.name
    except:
        await ctx.send(f'Error! Name for {name_input} not found in chess.com database.')
    else:
        await ctx.send(f'Full name: {player_name}')

# Returns the stats of any chess.com user
# ex: $stats magnuscarlsen
@bot.command()
async def stats(ctx, name_input):
    try:
        get_player_profile(name_input) # determine if account exists
    except:
        await ctx.send(f'Error! No information for {name_input} found!')
    else:
        await ctx.send(chess_response_ratings(name_input)) # success - returns a string of all player ratings

# Converts ChessDotComResponse to Python dict
# Then displays chess mode and rating pairs as a single string
async def chess_response_ratings(name):
    str = ""
    # JSON object as dict
    response = get_player_stats(name).json

    # for printing the key-value pair of
    # nested "stats" dictionary
    for mode in response["stats"]:
        str += mode + " rating: " + mode[0]['rating'] + "\n"

    return str

bot.run(token)

import os
import berserk
import discord
from pymongo import MongoClient
from discord.ext import commands
from dotenv import load_dotenv
from chessdotcom import get_player_profile, get_player_stats
from datetime import datetime

load_dotenv() # import variables from .env
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # message came from private dm
    if isinstance(message.channel, discord.DMChannel) and message.content.startswith("register"):
        content_split = message.content.split()
        if len(content_split) > 1:
            token = content_split.pop(1)
            await register(message, token)
        else:
            await message.channel.send(":bangbang: Invalid request!")
    await bot.process_commands(message) # necessary to accept commands from users

# displays all ratings for a chess.com account
def chess_response_ratings(name):
    chess_play_modes = ["chess_rapid", "chess_bullet", "chess_blitz"]

    result = "Ratings for player " + name + ":\n"

    # JSON object as dict
    response = get_player_stats(name).json

    for mode in response["stats"]:
        if mode != 'fide' and len(response["stats"][mode]) < 1: # to avoid accessing null properties of a chess mode
            result += mode + ": No data to display.\n"
        else:
            if mode in chess_play_modes:
                result += mode + ": " + str(response["stats"][mode]["last"]["rating"]) + "\n"
            elif mode == 'tactics':
                result += mode + ": " + str(response["stats"][mode]["highest"]["rating"]) + "\n"
            elif mode == 'fide':
                result += mode + ": " + str(response["stats"][mode]) + "\n"
            elif mode == 'puzzle_rush':
                result += mode + ": " + str(response["stats"][mode]["best"]["score"]) + "\n"
            else:
                result += mode + ": Unknown details at this time. Our devs are working on the problem!\n"
    return result

# Commands

# Returns user's stats for a given mode
# ex: $mode_rating magnuscarlsen puzzle_rush
@bot.command()
async def mode_rating(ctx, name_input: str, mode: str):
    try:
        get_player_profile(name_input) # determine if account exists
    except:
        await ctx.send(f':bangbang: Error! No information for {name_input} found!')
        return # no need to check for invalid account details

    player_stats = get_player_stats(name_input).json["stats"]
    print(player_stats)

    if mode not in player_stats:
        await ctx.send(f':bangbang: Error! Mode **{mode}** does not exist')    

    mode_stats = player_stats[mode]
    print(mode_stats)

    if mode == 'fide':
        await ctx.send(f':crown: **{name_input}** has a rating of **{mode_stats}** in mode **{mode}**:chess_pawn:')
        return
    # Empty stats
    if not mode_stats or len(mode_stats) == 0:
        await ctx.send(f':bangbang: Error! User **{name_input}** does not have a rating for mode **{mode}**')
    else:
        rating = 'N/A'
        if 'rating' in mode_stats:
            rating = mode_stats['rating']
        elif 'last' in mode_stats:
            rating = mode_stats['last']['rating']
        elif 'highest' in mode_stats:
            rating = mode_stats['highest']['rating']
        elif 'best' in mode_stats:
            rating = mode_stats['best']['score']

        await ctx.send(f':crown: **{name_input}** has a rating of **{rating}** in mode **{mode}**:chess_pawn:')

# Returns the stats of any chess.com user
@bot.command()
async def stats(ctx, name_input: str):
    try:
        get_player_profile(name_input) # determine if account exists
    except:
        await ctx.send(f'Error! No information for {name_input} found!')
    else:
       await ctx.send(chess_response_ratings(name_input)) # success - returns a string of all player ratings

# registers or updates a user's lichess api token
async def register(message: discord.Message, token: str):
    discord_id = message.author.id
    ctx = message.channel
    collection = {}

    # mongodb connection
    try:
        cluster = MongoClient(os.environ.get("MONGO_URL"))
        db = cluster["ChessGodDB"]
        collection = db["lichess_accounts"]
    except:
        print(f'MongoDB connection unsuccessful!\n')
    else:
        print(f'MongoDB connection successful!\n')

    # account registration
    session = berserk.TokenSession(token)
    client = berserk.Client(session=session)
    try:
        user = client.account.get()['id']  # lichess username
    except:
        await ctx.send(f':bangbang: Lichess API access token is invalid!')
    else:
        # check if discord id exists in db
        find_user = collection.find_one({'discord_id': discord_id})

        # register new account
        if find_user == None:
            # db query
            post = {"discord_id": discord_id, "lichess_token": token,
                    "lichess_user": user, "date_created": datetime.now()}
            collection.insert_one(post)

            # confirm user added to database
            await ctx.send(f'Played profile created for ' + user + '\n')
            await ctx.send(client.account.get())
        else:
            if token == find_user['lichess_token']:
                await ctx.send(f'Account ' + user + " is already in our database!")
            else:
                await ctx.send(f'Registering new account to our database!')
                # db query
                post = {"discord_id": discord_id, "lichess_token": token,
                        "lichess_user": user, "date_created": datetime.now()}
                collection.insert_one(post)

                # confirm user added to database
                await ctx.send(f'Player profile created for ' + user + '\n')
                await ctx.send(client.account.get())


bot.run(os.environ.get("DISCORD_API_TOKEN"))

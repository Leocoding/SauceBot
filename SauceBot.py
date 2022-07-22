import discord
from discord.ext import commands
import urllib.request as urllib2
import json
from dotenv import load_dotenv
import os
import string

# CONSTANTS
SYS_CHAN = 609918100602748929
MEMBER_ID = 177514021992398849

# Bot intents (to detect some events)
default_intents = discord.Intents.default()
default_intents.members = True

# The bot's client with intents
bot = commands.Bot(command_prefix="!", intents=default_intents)

# Token setup
load_dotenv(dotenv_path="config")


# Get the bitcoin's curency in EUR & USD with coindesk's API
def getBitcoinCurrency():
    print("start function crypto")
    done = False
    while done is not True:
        try:
            print("try")
            url = "https://api.coindesk.com/v1/bpi/currentprice.json"
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            data = response.read()
            done = True

        except:
            print("except")
            done = False
    print("data get")
    ex_data = json.loads(data)
    bitcoin_p_eur = ex_data['bpi']['EUR']['rate_float']
    bitcoin_p_usd = ex_data['bpi']['USD']['rate_float']
    print("function crypto OK")
    return bitcoin_p_eur, bitcoin_p_usd


# ----------- EVENTS -----------


# After the bot was started
@bot.event
async def on_ready():
    game = discord.Game("Dans la Sauce")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("bot ready")
    print("Discord version : " + discord.__version__)


# -------- /!\ Not tested /!\ --------

# When a member join the server
@bot.event
async def on_member_join(member):
    Channel = bot.get_channel(SYS_CHAN)
    await Channel.send("Bienvenue à toi " + member.name + " !")


# When a member leave the server
@bot.event
async def on_member_leave(member):
    Channel = bot.get_channel(SYS_CHAN)
    await Channel.send(member.name + "est parti(e) pour un monde meilleur :)")

# -------- /!\ Not tested /!\ --------


# When i connect to a voice channel
@bot.event
async def on_voice_state_update(member, before, after):
    if not before.channel and after.channel and member.id == MEMBER_ID:
        await member.send("Welcome back sir !")


# When a message is posted by a member
#@bot.event
#async def on_message(message):
#    if message.content.lower() == "ping":
#        await message.channel.send("pong")
#        await message.author.send("Tu aimes le ping-pong ?")
#    else:
#        return


# ----------- COMMANDS (not working for now) -----------

@bot.command()
async def bitcoin(ctx):
    (a, b) = getBitcoinCurrency()
    await ctx.send("Le bitcoin vaut actuellement " + str(a) + " euros et " + str(b) +  " dollars americain.")


@bot.command()
async def aide(ctx):
    print("help command : called")
    await ctx.send("Test")


# Start the bot with secret token
bot.run(os.getenv("TOKEN"))

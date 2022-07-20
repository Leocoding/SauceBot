import discord
from discord.ext import commands
import urllib.request as urllib2
import json
import string
from dotenv import load_dotenv
import os

# CONSTANTS
SYS_CHAN = 609918100602748929
MEMBER_ID = 177514021992398849

# Bot intents (to detect some events)
default_intents = discord.Intents.default()
default_intents.members = True

# The bot's client with intents
bot = commands.Bot(command_prefix='!')

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


# ----------- COMMANDS (not working for now) -----------

@bot.command()
async def bitcoin(ctx, devise: string):
    print("bitcoin command : command called")
    d = devise.lower()
    a = 0
    b = 0
    (a, b) = getBitcoinCurrency(d)
    print("bitcoin command : data receveid")
    if d == "eur":
        print("bitcoin command : eur")
        await ctx.send("Le bitcoin vaut actuellement " + a + " euros.")
    if d == "usd":
        print("bitcoin command : usd")
        await ctx.send("Le bitcoin vaut actuellement " + b + " dollars americain.")
    else:
        print("bitcoin command : other choice")
        await ctx.send("Veillez spécifier la devise. (eur = euro / usd = dollard américain)")


@bot.command()
async def aide(ctx):
    print("help command : called")
    await ctx.send("Test")


@bot.command()
async def foo(ctx, arg):
    await ctx.send(arg)

# ----------- EVENTS -----------


# After the bot was started
@bot.event
async def on_ready():
    game = discord.Game("Dans la Sauce")
    await bot.change_presence(status=discord.Status.idle, activity=game)
    print("bot ready")


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
@bot.event
async def on_message(message):
    if message.content.lower() == "ping":
        await message.channel.send("pong")
        await message.author.send("Tu aimes le ping-pong ?")
    else:
        return


# Start the bot with secret token
bot.run(os.getenv("TOKEN"))

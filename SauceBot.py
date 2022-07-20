import string

import discord
from discord.ext import commands
import urllib.request as urllib2
import json

# CONSTANTS
TOKEN = "OTk4OTg5MDAyNTIwNjc0Mzc2.GJ6ls_.rIG-0Cal988m8hjuqo_ICvViYMRTNS-Y5BBY1A"
SYS_CHAN = 609918100602748929
MEMBER_ID = 177514021992398849

# Bot intents (to detect some events)
default_intents = discord.Intents.default()
default_intents.members = True

# The bot's client with intents
bot = commands.Bot(command_prefix="!", intents=default_intents)


# Get the bitcoin's curency in EUR & USD with coindesk's API
def getBitcoinCurrency():
    done = False
    while done is not True:
        try:
            url = "https://api.coindesk.com/v1/bpi/currentprice.json"
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            data = response.read()
            done = True
        except:
            done = False
    ex_data = json.loads(data)
    bitcoin_p_eur = ex_data['bpi']['EUR']['rate_float']
    bitcoin_p_usd = ex_data['bpi']['USD']['rate_float']
    return bitcoin_p_eur, bitcoin_p_usd


# ----------- COMMANDS -----------

@bot.commands(name="bitcoin")
async def bitcoinCurrency(ctx, devise: string):
    d = devise.lower
    (a, b) = getBitcoinCurrency()
    if (d == "eur"):
        ctx.channel.send("Le bitcoin vaut actuellement " + a + " euros.")
    if (d == "usd"):
        ctx.channel.send("Le bitcoin vaut actuellement " + a + " dollars americain.")
    else:
        ctx.channel.send("Veillez spécifier la devise. (eur = euro / usd = dollard américain)")

# ----------- EVENTS -----------

# After the bot was started
@bot.event
async def on_ready():
    game = discord.Game("Dans la Sauce")
    await bot.change_presence(status=discord.Status.idle, activity=game)
    a = 0
    b = 0
    (a, b) = getBitcoinCurrency()


# -------- /!\ Not working /!\ --------

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



# When a member connect / disconnect or move to a voice channel
@bot.event
async def on_voice_state_update(member, before, after):
    if not before.channel and after.channel and member.id == MEMBER_ID:
        user = await bot.get_member(MEMBER_ID)
        await user.send("Salut gros chien")

# -------- /!\ Not working /!\ --------


# When a message is posted by a member
@bot.event
async def on_message(message):
    if message.content.lower() == "ping":
        await message.channel.send("pong")
        await message.author.send("bonjour")
    else:
        return


# Start the bot with secret token
bot.run(TOKEN)

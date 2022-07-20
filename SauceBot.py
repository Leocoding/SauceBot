import discord
from discord.ext import commands

# CONSTANTS
TOKEN = "OTk4OTg5MDAyNTIwNjc0Mzc2.GJ6ls_.rIG-0Cal988m8hjuqo_ICvViYMRTNS-Y5BBY1A"
SYS_CHAN = 609918100602748929
MEMBER_ID = 177514021992398849

# Bot intents (to detect some events)
default_intents = discord.Intents.default()
default_intents.members = True

# The bot's client with intents
client = discord.Client(intents=default_intents)
bot = commands.Bot(command_prefix="!")

# After the bot was started
@bot.event
async def on_ready():
    print("Bot ready")
    game = discord.Game("Dans la Sauce")
    await bot.change_presence(status=discord.Status.idle, activity=game)


# When a member join the server
@bot.event
async def on_member_join(member):
    Channel = client.get_channel(SYS_CHAN)
    await Channel.send("Bienvenue à toi " + member.name + " !")


# When a member leave the server
@bot.event
async def on_member_leave(member):
    Channel = client.get_channel(SYS_CHAN)
    await Channel.send(member.name + "est parti(e) pour un monde meilleur :)")


# When a member connect / disconnect or move to a voice channel
@bot.event
async def on_voice_state_update(member, before, after):
    if not before.channel and after.channel and member.id == MEMBER_ID:
        user = await client.get_member(MEMBER_ID)
        await user.send("Salut gros chien")


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
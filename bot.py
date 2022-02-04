import discord
from discord import client
from discord import activity
from discord.ext import commands

import os
import keep_alive

# add other event here for further uses

# setting import
import json
with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

# intents setup
intents = discord.Intents.default()
intents.members = True
intents.messages = True

# help command
class help(commands.HelpCommand):
    def __init__(self):
        super().__init__()

# nbot = N.Ben
nbot = commands.Bot(
        command_prefix='&',
        intents=intents, 
        fetch_offline_members=True,
        case_insensitive = True)

# startup with status
# startup notification on background console
@nbot.event
async def on_ready():
    await nbot.change_presence(
        status=discord.Status.online, 
        activity=discord.Game('波台@LIHKG'),
        afk=False)
    print('Ready! N.Ben get his backpack ready!')

@nbot.command()
async def load(ctx, ext):
    nbot.load_extension(f'cogs.{ext}')

@nbot.command()
async def unload(ctx, ext):
    nbot.unload_extension(f'cogs.{ext}')

for loadfile in os.listdir('./cogs'):
    if loadfile.endswith('.py'):
        nbot.load_extension(f'cogs.{loadfile[:-3]}')

keep_alive.keep_alive()
nbot.run(jdata['TOKEN'])
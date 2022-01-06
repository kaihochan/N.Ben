import discord
from discord import client
from discord import activity
from discord.ext import commands

import os

# music bot usage
# using youtube-dl
# import asyncio
#import music

# nben bot usage
#import nben

# setting import
import json
with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

# intents setup
intents = discord.Intents.all()
intents.members = True
intents.messages = True

# nbot = N.Ben
nbot = commands.Bot(
        command_prefix='*',
        intents=intents, 
        fetch_offline_members=True)

# cogs initialization
#cogs = [nben, music]

#for i in range(len(cogs)):
    #cogs[i].setup(nbot)

# startup with status
# startup notification on background console
@nbot.event
async def on_ready():
    await nbot.change_presence(
        status=discord.Status.online, 
        activity=discord.Game('波台@LIHKG'),
        afk=False)
    print('Ready! N.Ben get his backpack ready!')

# command &&echo, repeat wordings
@nbot.event
async def on_message(message):
    if (message.author != nbot.user):
        if message.content.startswith("&&echo "):
            await message.channel.send(message.content[7:].format(message))

@nbot.command
async def load(ctx, ext):
    nbot.load_extension(f'cogs.{ext}')

@nbot.command
async def unload(ctx, ext):
    nbot.unload_extension(f'cogs.{ext}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        nbot.load_extension(f'cogs.{filename[:-3]}')

nbot.run(jdata['TOKEN'])
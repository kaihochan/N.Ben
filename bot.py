import discord
from discord.ext import commands

import os

# setting import
import json
with open('settings/setting.json', mode='r', encoding='utf8') as dcfile:
    dcdata = json.load(dcfile)
    dcfile.close()

# intents setup
intents = discord.Intents.default()
intents.members = True

# help command
class help(commands.HelpCommand):
    def __init__(self):
        super().__init__()

# nbot = N.Ben
nbot = commands.Bot(
        command_prefix='&',
        intents=intents, 
        fetch_offline_members=True,
        case_insensitive = True,
        owner_ids=set(dcdata["OWNER"]))

# startup with status
# startup notification on background console
@nbot.event
async def on_ready():
    await nbot.change_presence(
        status=discord.Status.online, 
        activity=discord.Game('波台@LIHKG'),
        afk=False)
    print('Ready! N.Ben get his backpack ready!')

# load function set in cogs folders
# command hided, only available for owners
@nbot.command(hidden=True)
@commands.is_owner()
async def load(ctx, ext):
    nbot.load_extension(f'cogs.{ext}')
    embed = discord.Embed(description=f'✔️ {ext} loaded. Related functions available now.')
    await ctx.send(embed=embed)

# unload function set in cogs folders
# command hided, only available for owners
@nbot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, ext):
    nbot.unload_extension(f'cogs.{ext}')
    embed = discord.Embed(description=f'❌ {ext} unloaded. Related functions unavailable now.')
    await ctx.send(embed=embed)

# reload function set in cogs folers
# command hided, only available for owners
@nbot.command(hidden=True)
@commands.is_owner()
async def reload(ctx, ext):
    nbot.reload_extension(f'cogs.{ext}')
    embed = discord.Embed(description=f'♻️ {ext} reloaded.')
    await ctx.send(embed=embed)

for loadfile in os.listdir('./cogs'):
    if loadfile.endswith('.py'):
        nbot.load_extension(f'cogs.{loadfile[:-3]}')

nbot.run(dcdata['TOKEN'])
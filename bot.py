import discord
from discord.ext import commands

import json
with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.default()
intents.typing = True
intents.members = True

nbot = commands.Bot(command_prefix='&&', intents=intents)

@nbot.event
async def on_ready():
    print('Ready! N.Ben get his backpack ready!')


'''@nbot.event
async def on_member_join(member):
    channel = nbot.get_channel(928382794265141249)
    await channel.send('???')'''

@nbot.command()
async def dllm(ctx):
    await ctx.send('屌你老母')

nbot.run(jdata['TOKEN'])
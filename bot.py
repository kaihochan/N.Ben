import discord
import asyncio
import os
import json
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.listening, name="Aimer - Monochrome Syndrome")
client = commands.Bot(
    command_prefix='&',
    activity=discord.Game('J'),
    intents=intents, 
    fetch_offline_members=True,
    case_insensitive = True,
    owner_ids=set(json.loads(os.getenv('DISCORD_OWNER'))))

@client.event
async def on_ready():
    print(f'[{client.user}] Logged in and running normally')

async def load_cogs():
    for loadfile in os.listdir('./cogs'):
        if loadfile.endswith('.py'):
            await client.load_extension(f'cogs.{loadfile[:-3]}')

async def main():
    async with client:
        await load_cogs()
        await client.start(os.getenv('DISCORD_TOKEN'))

asyncio.run(main())
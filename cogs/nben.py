import discord
from discord import client
from discord import activity
from discord.ext import commands
from youtube_dl.downloader import external

import json
with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class nben(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # command &&dllm, response fuck your mother in Cantonese
    @commands.command()
    async def dllm(self, ctx):
        await ctx.send('屌你老母')

    # command &&smile, response his smile
    @commands.command()
    async def smile(self, ctx):
        await ctx.send(jdata['NBENGIF'])
        
    # comment &&backpack, response his backpack
    @commands.command()
    async def backpack(self, ctx):
        await ctx.send(jdata['NBENBACKPACK'])
        
    # comment &&nteam, response his backpack
    @commands.command()
    async def nteam(self, ctx):
        await ctx.send(jdata['TEAMNBEN'])

def setup(bot):
    bot.add_cog(nben(bot))

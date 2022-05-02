import discord
from discord.ext import commands
import os

# import json file
import json
with open('settings/pictures.json', mode='r', encoding='utf8') as pfile:
    pdata = json.load(pfile)
    pfile.close()

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
        await ctx.send(pdata['NBENGIF'])
        
    # command &&backpack, response his backpack
    @commands.command()
    async def backpack(self, ctx):
        await ctx.send(pdata['NBENBACKPACK'])
        
    # command &&nteam, response his backpack
    @commands.command()
    async def nteam(self, ctx):
        await ctx.send(pdata['TEAMNBEN'])

    # command &&echo, reserved, now do nothing
    @commands.command()
    async def echo(self, ctx):
        pass

def setup(bot):
    bot.add_cog(nben(bot))

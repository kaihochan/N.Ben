import discord
from discord.ext import commands

class NBen(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.command()
    async def smile(self, ctx: commands.Context) -> None:
        """Send N.Ben's smiling GIF."""
        await ctx.send("https://i.imgur.com/8jXHikK.gif")
        await ctx.message.delete()
    
    @commands.command()
    async def backpack(self, ctx: commands.Context) -> None:
        """Send N.Ben's backpack picture."""
        await ctx.send("https://i.imgur.com/wX26U8W.png")
        await ctx.message.delete()
    
    @commands.command()
    async def nteam(self, ctx: commands.Context) -> None:
        """Send a lot of N.Bens."""
        await ctx.send("https://na.cx/i/DYhaPCZ.jpg")
        await ctx.message.delete()

async def setup(client: commands.Bot) -> None:
    await client.add_cog(NBen(client))
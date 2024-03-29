import discord
from discord.ext import commands
import json

class Nword(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        with open('settings/nword.json', mode='r', encoding='utf8') as nfile:
            self.client.ndata = json.load(nfile)
            nfile.close()
    
    @commands.command()
    async def count(self, ctx: commands.Context, user: discord.User = None) -> None:
        """Count how many N words that user have said."""
        embed = discord.Embed()
        if user is None:
            user = ctx.author
        elif user == self.client.user:
            embed.description = "No, I don't say n-word."
            return await ctx.send(embed=embed)
        elif user.bot:
            embed.description = "I don't check n-word said by bot."
            return await ctx.send(embed=embed)
        if str(user.id) not in self.client.ndata:
            embed.description = f"{user.mention} hasn't said any n-word yet."
            return await ctx.send(embed=embed)
        else:
            since_last = self.client.ndata[str(user.id)]['total']-self.client.ndata[str(user.id)]['last']
            embed.title = "N-word Report"
            embed.description = f"User:\t\t{user.mention}\n"
            embed.add_field(
                name="N-word", 
                value=f"{self.client.ndata[str(user.id)]['total']} time{'' if self.client.ndata[str(user.id)]['total'] < 2 else 's'}", 
                inline=False)
            embed.add_field(
                name="N-word with hard-R", 
                value=f"{self.client.ndata[str(user.id)]['hard_r']} time{'' if self.client.ndata[str(user.id)]['hard_r'] < 2 else 's'}", 
                inline=False)
            embed.add_field(
                name="N-word said since last check", 
                value=f"{since_last} time{'' if since_last < 2 else 's'}",
                inline=False)
            embed.set_thumbnail(url=user.avatar)
            embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            self.client.ndata[str(user.id)]['last'] = self.client.ndata[str(user.id)]['total']
            with open('settings/nword.json', mode='w', encoding='utf8') as nfile:
                json.dump(self.client.ndata, nfile, ensure_ascii=False, indent=4)
                nfile.close()

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Nword(client))
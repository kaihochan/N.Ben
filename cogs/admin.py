import discord
from discord.ext import commands
from discord.utils import get
import json

class admin(commands.Cog):
    def __init__(self, nbot):
        self.client = nbot
        with open('settings/kick.json', mode='r', encoding='utf8') as kfile:
            self.client.kdata = json.load(kfile)
            kfile.close()
    
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def kick(self, ctx:commands.Context, user:discord.User=None, times=5):
        embed = discord.Embed()
        if user is None:
            user = ctx.author
        elif user.bot:
            embed.description = "I don't auto kick BOT."
            return await ctx.send(embed=embed)
        if str(user.id) not in self.client.kdata:
            self.client.kdata[str(user.id)] = times
        else:
            self.client.kdata[str(user.id)] += times
        embed.title = "Auto-kick counter"
        embed.description = f"User:\t\t{user.mention}\n"
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='Added kick count', value=times, inline=False)
        embed.add_field(name='Total kick count', value=self.client.kdata[str(user.id)], inline=False)
        await ctx.send(embed=embed)
        with open('settings/kick.json', mode='w', encoding='utf8') as kfile:
            json.dump(self.client.kdata, kfile, ensure_ascii=False, indent=4)
            kfile.close()
        for guild in self.client.guilds:
            for voice_ch in guild.voice_channels:
                if user in voice_ch.members:
                    member = get(voice_ch.members, id=user.id)
                    await member.move_to(None)
                    self.client.kdata[str(user.id)] -= 1
                    with open('settings/kick.json', mode='w', encoding='utf8') as kfile:
                        json.dump(self.client.kdata, kfile, ensure_ascii=False, indent=4)
                        kfile.close()
                    return
        return
    
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def rkick(self, ctx:commands.Context, user:discord.User=None):
        if user is None:
            user = ctx.auther
        if str(user.id) in self.client.kdata:
            self.client.kdata.pop(str(user.id))
        embed = discord.Embed(
            title="Auto-kick counter",
            description=f"Removed auto-kick count of {user.mention}",
            thumbnail=user.avatar_url)
        with open('settings/kick.json', mode='w', encoding='utf8') as kfile:
            json.dump(self.client.kdata, kfile, ensure_ascii=False, indent=4)
            kfile.close()
        return await ctx.send(embed=embed)

def setup(nbot):
    nbot.add_cog(admin(nbot))
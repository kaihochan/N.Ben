import discord
from discord.ext import commands
from discord.utils import get
import json

class Admin(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        with open("settings/kick.json", mode="r", encoding="utf8") as kfile:
            self.client.kdata = json.load(kfile)
            kfile.close()

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx: commands.Context) -> None:
        """
        Shutdown the BOT service.\n
        Command hided, only available for owners.
        """
        await self.client.close()
        print(f"[{self.client.user}] Closed service.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx: commands.Context, ext: str) -> None:
        """
        Load function set in Cogs folers.\n
        Command hided, only available for owners.
        """
        self.client.load_extension(f"cogs.{ext}")
        embed = discord.Embed(description=f"✔️ {ext} loaded. Related functions available now.")
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, ext: str) -> None:
        """
        Unload function set in Cogs folers.\n
        Command hided, only available for owners.
        """
        self.client.unload_extension(f"cogs.{ext}")
        embed = discord.Embed(description=f"❌ {ext} unloaded. Related functions unavailable now.")
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, ext: str) -> None:
        """
        Reload function set in Cogs folers.\n
        Command hided, only available for owners.
        """
        self.client.reload_extension(f"cogs.{ext}")
        embed = discord.Embed(description=f"♻️ {ext} reloaded.")
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def kick(self, ctx: commands.Context, user: discord.User = None, times: int = 5) -> None:
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
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name="Added kick count", value=times, inline=False)
        embed.add_field(name="Total kick count", value=self.client.kdata[str(user.id)], inline=False)
        await ctx.send(embed=embed)
        with open("settings/kick.json", mode="w", encoding="utf8") as kfile:
            json.dump(self.client.kdata, kfile, ensure_ascii=False, indent=4)
            kfile.close()
        for guild in self.client.guilds:
            for voice_ch in guild.voice_channels:
                if user in voice_ch.members:
                    member = get(voice_ch.members, id=user.id)
                    await member.move_to(None)
                    self.client.kdata[str(user.id)] -= 1
                    with open("settings/kick.json", mode="w", encoding="utf8") as kfile:
                        json.dump(self.client.kdata, kfile, ensure_ascii=False, indent=4)
                        kfile.close()
                    return
    
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def rkick(self, ctx: commands.Context, user: discord.User = None) -> None:
        if user is None:
            user = ctx.auther
        if str(user.id) in self.client.kdata:
            self.client.kdata.pop(str(user.id))
        embed = discord.Embed(
            title="Auto-kick counter",
            description=f"Removed auto-kick count of {user.mention}",
            thumbnail=user.avatar,)
        with open("settings/kick.json", mode="w", encoding="utf8") as kfile:
            json.dump(self.client.kdata, kfile, ensure_ascii=False, indent=4)
            kfile.close()
        await ctx.send(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Admin(client))
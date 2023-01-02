import discord
from discord.ext import commands
import numpy as np

class Team(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
    
    @commands.command()
    async def team(self, ctx: commands.Context, *ignore_users: discord.Member) -> None:
        """Random users into the 2 teams, can specify ignored users."""
        full_users_list = ctx.author.voice.channel.members
        if (ctx.guild.get_member(392575005340467201) in full_users_list) & (ctx.guild.get_member(481066909840965633) in full_users_list):
            full_users_list.remove(ctx.guild.get_member(481066909840965633))
        if (self.client.user in full_users_list):
            full_users_list.remove(self.client.user)
        for user in ignore_users:
            if user in full_users_list:
                full_users_list.remove(user)
        users_list = np.array(full_users_list)
        np.random.shuffle(users_list)
        teams_list = np.array_split(users_list, 2)
        for index, team in enumerate(teams_list):
            team_message = f"Team {index + 1}\n"
            for user in team:
                team_message += f"{user.mention}\n"
            await ctx.send(team_message)

    @commands.command()
    async def echo(self, ctx: commands.Context, *, message: str) -> None:
        """Repeat the message in the command, and delete message sent by user."""
        await ctx.send(message)
        await ctx.message.delete()

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Team(client))
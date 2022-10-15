import discord
from discord.ext import commands
import numpy as np

class Team(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
    
    @commands.command()
    async def team(self, ctx: commands.Context, number_of_teams: int = 2) -> None:
        """Random users into the number of teams specifed."""
        users_list = np.array(ctx.author.voice.channel.members)
        np.random.shuffle(users_list)
        teams_list = np.array_split(users_list, number_of_teams)
        for index, team in enumerate(teams_list):
            team_message = f"Team {index + 1}\n"
            for user in team:
                team_message += f"{user.mention}\n"
            await ctx.send(team_message)

    @commands.command()
    async def userlink(self, ctx: commands.Context, user1: discord.Member, user2: discord.Member) -> None:
        pass


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Team(client))
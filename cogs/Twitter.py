import discord
from discord.ext import tasks, commands
import tweepy
import os
import json
import datetime
import asyncio

class Twitter(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.pause = False

    async def cog_load(self) -> None:
        with open('settings/twitter_watchlist.json', mode='r', encoding='utf8') as watchfile:
            self.watchlist = json.load(watchfile)
            watchfile.close()
        self.twitter_client = tweepy.Client(
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_KEY_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))
        self.post_liked_tweets.start()
        print("[Twitter] Twitter module is running normally")
    
    async def cog_unload(self) -> None:
        self.post_liked_tweets.cancel()

    def seconds_until(self, hours: int, minutes: int) -> float:
        """Calculate senconds to be waited."""
        given_time = datetime.time(hours, minutes)
        now = datetime.datetime.now()
        future_exec = datetime.datetime.combine(now, given_time)
        if (future_exec - now).days < 0:
            future_exec = datetime.datetime.combine(now + datetime.timedelta(days=1), given_time)
        return (future_exec - now).total_seconds()

    @tasks.loop(hours=8.0)
    async def post_liked_tweets(self) -> None:
        """
        Post subscribed users' liked tweets in 02:30, 10:30, 18:30 everyday.\n
        Auto start when the class is being loaded, auto cancel when the class is being unloaded
        """
        next_update = [
            self.seconds_until(2, 30),
            self.seconds_until(10, 30),
            self.seconds_until(18, 30),
        ]
        await asyncio.sleep(min(next_update))
        if not self.pause:
            print("[Twitter] Update send.")
            for id in self.watchlist:
                name = self.twitter_client.get_user(id=int(id)).data.name
                username = self.twitter_client.get_user(id=int(id)).data.username
                response = self.twitter_client.get_liked_tweets(id=int(id), max_results=100, expansions=['author_id'], user_auth=True)
                for tweet in reversed(response.data):
                    auther_username = self.twitter_client.get_user(id=tweet.author_id).data.username
                    tweet_id = tweet.id
                    if not(tweet_id in self.watchlist[id]['liked_post']):
                        self.watchlist[id]['liked_post'].append(tweet_id)
                        for text_ch in self.watchlist[id]['bonded_ch']:
                            await self.client.get_channel(int(text_ch)).send(f'{name} (@{username}) liked this tweet.\nhttps://twitter.com/{auther_username}/status/{tweet_id}')
        with open('settings/twitter_watchlist.json', mode='w', encoding='utf8') as watchfile:
            json.dump(self.watchlist, watchfile, ensure_ascii=False, indent=4)
            watchfile.close()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def subscribe(self, ctx: commands.Context, username: str) -> None:
        """
        Add given username into Twitter watchlist and save into json.\n
        Command hided, only available for owners.
        """
        name = self.twitter_client.get_user(username=username).data.name
        id = self.twitter_client.get_user(username=username).data.id
        embed = discord.Embed()
        if str(id) in self.watchlist:
            if ctx.channel.id in self.watchlist[str(id)]['bonded_ch']:
                embed.title = f'Add to Twitter Watch List'
                embed.description = f'You have already bonded {name} (@{username}) liked tweets to {ctx.channel.name}.'
                embed.url = f'https://twitter.com/{username}'
                await ctx.send(embed=embed)
            elif not(ctx.channel.id in self.watchlist[str(id)]['bonded_ch']):
                self.watchlist[str(id)]['bonded_ch'].append(ctx.channel.id)
                embed.title = f'Add to Twitter Watch List'
                embed.description = f'{name} (@{username}) liked tweets will be posted in {ctx.channel.name}.'
                embed.url = f'https://twitter.com/{username}'
                await ctx.send(embed=embed)
        else:
            self.watchlist[str(id)] = {'bonded_ch': [],
                                'liked_post': []}
            self.watchlist[str(id)]['bonded_ch'].append(ctx.channel.id)
            embed.title = f'Add to Twitter Watch List'
            embed.description = f'{name} (@{username}) liked tweets will be posted in {ctx.channel.name}.'
            embed.url = f'https://twitter.com/{username}'
            await ctx.send(embed=embed)
        with open('settings/twitter_watchlist.json', mode='w', encoding='utf8') as watchfile:
            json.dump(self.watchlist, watchfile, ensure_ascii=False, indent=4)
            watchfile.close()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def username_to_id(self, ctx: commands.Context, username: str) -> None:
        """
        Checks twitter id of given username.\n
        Command hided, only available for owners.
        """
        user = self.twitter_client.get_user(username=username)
        await ctx.send(f'username: {user.data.name}\nid: {user.data.id}')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def pause_update(self, ctx: commands.Context) -> None:
        """
        Pause/resume regular update on Twitter channel.\n
        Command hided, only available for owners.
        """
        self.pause = not self.pause
        print(f"[Twitter] Daily update { 'resumed' if self.pause else 'paused' }.")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Twitter(client))
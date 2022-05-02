import discord
from discord.ext import commands
import json
import tweepy
import datetime
import asyncio

with open('settings/twitter.json', mode='r', encoding='utf8') as twfile:
    twdata = json.load(twfile)
    twfile.close()

with open('settings/twitter_watchlist.json', mode='r', encoding='utf8') as watchfile:
    watchlist = json.load(watchfile)
    watchfile.close()

twClient = tweepy.Client(
            bearer_token=twdata['BEARERTOKEN'],
            consumer_key=twdata['APIKEY'],
            consumer_secret=twdata['APIKEY_SECRET'],
            access_token=twdata['ACCESSTOKEN'],
            access_token_secret=twdata['ACCESSTOKEN_SECRET'])

POST_TIME = {'H': 18, 'M': 30}

class tweet(commands.Cog):
    def __init__(self, nbot:commands.Bot):
        self.client = nbot
    
    # start routine twitter_posting
    # temp method, planning to use constuctor
    # command hided, only available for owners
    @commands.command(hidden=True)
    @commands.is_owner()
    async def starttwitter(self, ctx):
        embed = discord.Embed()
        embed.title = f'Twitter Posting Routine Started'
        embed.description = f"Followed users' liked post will be shared in each day {POST_TIME['H']}:{POST_TIME['M']}."
        await ctx.send(embed=embed)
        await self.twitter_posting()

    # post liked post of followed user in specified channel
    # post daily, 18:30
    async def twitter_posting(self):
        while True:
            await asyncio.sleep(self.seconds_until(POST_TIME['H'], POST_TIME['M']))
            for id in watchlist:
                name = twClient.get_user(id=int(id)).data.name
                username = twClient.get_user(id=int(id)).data.username
                liked_tweets = twClient.get_liked_tweets(id=int(id), max_results=100, expansions=['author_id'], user_auth=True)
                for tweet in reversed(liked_tweets.data):
                    usernamePost = twClient.get_user(id=tweet.author_id).data.username
                    tweetid = tweet.id
                    if not(tweetid in watchlist[id]['liked_post']):
                        watchlist[id]['liked_post'].append(tweetid)
                        for text_ch in watchlist[id]['bonded_ch']:
                            await self.client.get_channel(int(text_ch)).send(f'{name} (@{username}) liked this tweet.\nhttps://twitter.com/{usernamePost}/status/{tweetid}')
            with open('settings/twitter_watchlist.json', mode='w', encoding='utf8') as watchfile:
                json.dump(watchlist, watchfile, ensure_ascii=False, indent=4)
                watchfile.close()
            await asyncio.sleep(120)
    
    # timer for twitter_posting
    def seconds_until(self, hours, minutes):
        given_time = datetime.time(hours, minutes)
        now = datetime.datetime.now()
        future_exec = datetime.datetime.combine(now, given_time)
        if (future_exec - now).days < 0:
            future_exec = datetime.datetime.combine(now + datetime.timedelta(days=1), given_time)
        return (future_exec - now).total_seconds()

    # command &&checkstwitter, checks twitter id of given username
    # command hided, only available for owners
    @commands.command(hidden=True)
    @commands.is_owner()
    async def checkstwitter(self, ctx:commands.Context, username):
        user = twClient.get_user(username=username)
        await ctx.send(f'username: {user.data.name}\nid: {user.data.id}')
    
    # command &&addtwitter, add given username into watchlist and save into json
    # command hided, only available for owners
    @commands.command(hidden=True)
    @commands.is_owner()
    async def addtwitter(self, ctx:commands.Context, username):
        name = twClient.get_user(username=username).data.name
        id = twClient.get_user(username=username).data.id
        embed = discord.Embed()
        if str(id) in watchlist:
            if ctx.channel.id in watchlist[str(id)]['bonded_ch']:
                embed.title = f'Add to Twitter Watch List'
                embed.description = f'You have already bonded {name} (@{username}) liked tweets to {ctx.channel.name}.'
                embed.url = f'https://twitter.com/{username}'
                await ctx.send(embed=embed)
            elif not(ctx.channel.id in watchlist[str(id)]['bonded_ch']):
                watchlist[str(id)]['bonded_ch'].append(ctx.channel.id)
                embed.title = f'Add to Twitter Watch List'
                embed.description = f'{name} (@{username}) liked tweets will be posted in {ctx.channel.name}.'
                embed.url = f'https://twitter.com/{username}'
                await ctx.send(embed=embed)
        else:
            watchlist[str(id)] = {'bonded_ch': [],
                                'liked_post': []}
            watchlist[str(id)]['bonded_ch'].append(ctx.channel.id)
            embed.title = f'Add to Twitter Watch List'
            embed.description = f'{name} (@{username}) liked tweets will be posted in {ctx.channel.name}.'
            embed.url = f'https://twitter.com/{username}'
            await ctx.send(embed=embed)
        with open('settings/twitter_watchlist.json', mode='w', encoding='utf8') as watchfile:
            json.dump(watchlist, watchfile, ensure_ascii=False, indent=4)
            watchfile.close()
    
def setup(nbot):
    nbot.add_cog(tweet(nbot))
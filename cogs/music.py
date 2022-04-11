from distutils.command.upload import upload
from http import server
from re import S
from time import time
from typing import Any
from urllib import request
import discord
from discord import embeds
from discord.channel import VoiceChannel
from discord.ext import commands
import yt_dlp
import datetime

# import json file, youtube email and password inside
import json
with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

# class declear
# serve for global list
class Queue:
    def __init__(self, url2=None, title=None, yt_url=None, uploader=None, pusher=None, duration=None):
        self.url2 = url2
        self.title = title
        self.yt_url = yt_url
        self.uploader = uploader
        self.pusher = pusher
        self.duration = duration

class TimeList:
    def __init__(self):
        self.t_video = None
        self.t_start = None
        self.t_end = None


# globol list
# option for ydl, ffmpeg
FFMPEG_OPT = {  'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
                'options': '-vn'}
YDL_OPT = { 'format': 'bestaudio',
            'perfer_ffmpeg': True,
            'noplaylist': True,
            'cookiefile': 'cookies.txt',
            'geo_bypass_country': 'JP'}

# queue for multimedia flow control
queue = {} 
misc = {}
current_playing = {}

# time calculation for &&np
timeList = {}

# multimedia related function
class music(commands.Cog):
    def __init__(self, nbot):
        self.client = nbot

    # event trigger by load_queue(ctx)
    @commands.Cog.listener()
    async def on_queue_load(self, ctx):
        global current_playing
        serverID = ctx.message.guild.id
        source = await discord.FFmpegOpusAudio.from_probe(current_playing[serverID].url2, **FFMPEG_OPT)
        ctx.voice_client.play(source, after=lambda x=None: self.load_queue(ctx=ctx))
        embed2 = discord.Embed()
        embed2.title = f'Now Playing 🎵 {current_playing[serverID].title} by {current_playing[serverID].uploader}'
        embed2.url = current_playing[serverID].yt_url
        embed2.description = f'Queued by [{current_playing[serverID].pusher}]'
        await ctx.send(embed=embed2)

    # called by play after finish a song, trigger event to show info of next song
    def load_queue(self, ctx):
        global queue, misc, current_playing, timeList
        serverID = ctx.message.guild.id
        if misc[serverID] != -1:
            current_playing[serverID] = queue[serverID][0]
            queue[serverID].pop(0)
            misc[serverID] -= 1
            timeList[serverID].t_video = datetime.timedelta(seconds=current_playing[serverID].duration)
            timeList[serverID].t_start = datetime.datetime.now()
            timeList[serverID].t_end = timeList[serverID].t_video + timeList[serverID].t_start
            self.client.dispatch("queue_load", ctx)
        elif misc[serverID] == -1:
            ctx.voice_client.stop()
    
    # command &&j, lazy version of &&skip
    @commands.command()
    async def j(self, ctx):
        await ctx.invoke(self.client.get_command('join'))

    # command &&join, join/change voice channel
    @commands.command()
    async def join(self, ctx):
        embed = discord.Embed()
        if ctx.author.voice is None:
            embed.description = "❎ You are not in any voice channel"
            await ctx.send(embed=embed)
            return
        voice_ch = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_ch.connect()
            embed.description = f'✅ Joined and bonded to `{voice_ch}`'
            await ctx.send(embed=embed)
        else:
            await ctx.voice_client.move_to(voice_ch)
            embed.description = f'➡️ Changed channel from `{ctx.voice_client.channel}` to `{voice_ch}`'
            await ctx.send(embed=embed)

        global queue, misc, current_playing, timeList
        serverID = ctx.message.guild.id
        if not(serverID in misc):
            misc[serverID] = -1
        if not(serverID in queue):
            queue[serverID] = []
        if not(serverID in current_playing):
            current_playing[serverID] = Queue()
        if not(serverID in timeList):
            timeList[serverID] = TimeList()

    # command &&ds, lazy version of &&discon
    @commands.command()
    async def ds(self, ctx):
        await ctx.invoke(self.client.get_command('discon'))

    # command &&discon, leave voice channel
    @commands.command()
    async def discon(self, ctx):
        await ctx.voice_client.disconnect()
        embed = discord.Embed(description='🛄 Leave channel to find backpack')
        await ctx.send(embed=embed)
    
    # command &&p url, lazy version of &&play url
    @commands.command()
    async def p(self, ctx, url):
        await ctx.invoke(self.client.get_command('play'), url=url)

    # command &&play url, play youtube/youtube-dl supported video
    @commands.command()
    async def play(self, ctx, url):
        global queue, misc, current_playing, timeList
        global FFMPEG_OPT, YDL_OPT
        embed = discord.Embed()
        if ctx.author.voice is None:
            embed.description = "❎ You are not in any voice channel, can't play any song"
            await ctx.send(embed=embed)
            return
        if ctx.voice_client is None:
            await ctx.invoke(self.join)
        
        serverID = ctx.message.guild.id
        v_client = ctx.voice_client

        with yt_dlp.YoutubeDL(YDL_OPT) as ytDL:
            info = ytDL.extract_info(url, download=False)
            v_title = info.get('title', None)
            v_url = info.get('url', None)
            v_uploader = info.get('uploader', None)
            v_duration = info.get('duration', None)
            url2 = info['formats'][0]['url']
            
        if v_client.is_playing():
            misc[serverID] += 1
            queue[serverID].append(Queue(url2, v_title, v_url, v_uploader, ctx.author.mention, v_duration))
            embed2 = discord.Embed(title=f'Added to queue, position {misc[serverID]+1}')
            embed2.description = f'[{v_title} by {v_uploader}]({url})\r\nQueued by [{ctx.author.mention}]'
            await ctx.send(embed=embed2)
            return     
        
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPT)
        current_playing[serverID] = Queue(url2, v_title, v_url, v_uploader, ctx.author.mention, v_duration)
        timeList[serverID].t_video = datetime.timedelta(seconds=v_duration)
        timeList[serverID].t_start = datetime.datetime.now()
        timeList[serverID].t_end = timeList[serverID].t_video + timeList[serverID].t_start

        v_client.play(source, after=lambda x=None: self.load_queue(ctx=ctx))
        embed.title = f'Now Playing 🎵 {v_title} by {v_uploader}'
        embed.url = v_url
        embed.description = f'Queued by [{ctx.author.mention}]'
        await ctx.send(embed=embed)

    # command &&fs, lazy version of &&skip
    @commands.command()
    async def fs(self, ctx):
        await ctx.invoke(self.client.get_command('skip'))

    # command &&skip, skip song and load next song
    @commands.command()
    async def skip(self, ctx):
        global queue, misc, current_playing, timeList
        global FFMPEG_OPT
        embed = discord.Embed()
        serverID = ctx.message.guild.id

        if ctx.voice_client is None:
            embed.description = 'I am not in a voice channel.'
            await ctx.send(embed=embed)
            return
        
        if not(ctx.voice_client.is_playing()):
            embed.description = 'I am not playing anything.'
            await ctx.send(embed=embed)
            return

        ctx.voice_client.stop()
        embed.description = "⏭️ Skipped"
        await ctx.send(embed=embed)
        if misc[serverID] != -1:
            current_playing[serverID] = queue[serverID][0]
            queue[serverID].pop(0)
            misc[serverID] -= 1
            timeList[serverID].t_video = datetime.timedelta(seconds=current_playing[serverID].duration)
            timeList[serverID].t_start = datetime.datetime.now()
            timeList[serverID].t_end = timeList[serverID].t_video + timeList[serverID].t_start
            source = await discord.FFmpegOpusAudio.from_probe(current_playing[serverID].url2, **FFMPEG_OPT)
            ctx.voice_client.play(source, after=lambda x=None: self.load_queue(ctx=ctx))
            embed2 = discord.Embed()
            embed2.title = f'Now Playing 🎵 {current_playing[serverID].title} by {current_playing[serverID].uploader}'
            embed2.url = current_playing[serverID].yt_url
            embed2.description = f'Queued by [{current_playing[serverID].pusher}]'
            await ctx.send(embed=embed2)

    # command &&pause, puase music play by bot
    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        embed = discord.Embed(description="⏸️ Paused")
        await ctx.send(embed=embed)
    
    # command &&resume, resume music play by bot
    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        embed = discord.Embed(description="▶️ Resumed")
        await ctx.send(embed=embed)

    # command &&q, lazy version of &&queue
    @commands.command()
    async def q(self, ctx):
        await ctx.invoke(self.client.get_command('queue'))

    # command &&queue, check songs in queue
    @commands.command()
    async def queue(self, ctx):
        global queue, misc
        embed = discord.Embed()
        serverID = ctx.message.guild.id
        if misc[serverID] == -1:
            embed.description = 'Queue is empty!'
            await ctx.send(embed=embed)
        elif misc[serverID] != -1:
            output = '```CSS\r\n[Songs in queue]\r\n'
            for i in range(misc[serverID]+1):
                output += f'{i+1}: {queue[serverID][i].title}\r\n'
            output += '```'
            await ctx.send(output)

    # command &&np, check now playing
    @commands.command()
    async def np(self, ctx):
        global current_playing, timeList
        embed = discord.Embed()
        if ctx.voice_client is None:
            embed.description = 'I am not in a voice channel.'
            await ctx.send(embed=embed)
            return
        
        serverID = ctx.message.guild.id
        if ctx.voice_client.is_playing():
            timePast = datetime.datetime.now() - timeList[serverID].t_start
            Factor = int(timePast / timeList[serverID].t_video * 20)
            StatusBar = ['▱'] * 20
            for n in range(Factor+1):
                StatusBar[n] = '▰'
            StatusBarString = ''.join(StatusBar)
            embed.title = f'Now Playing 🎵 {current_playing[serverID].title} by {current_playing[serverID].uploader}'
            embed.url = current_playing[serverID].yt_url
            embed.description = f'Queued by [{current_playing[serverID].pusher}]\r\n{self.timedelta_str(ctx, timePast)} {StatusBarString} {self.timedelta_str(ctx, timeList[serverID].t_video)}'
        else:
            embed.description = 'No song is playing now.'
        await ctx.send(embed=embed)

    def timedelta_str(self, ctx, timedelta):
        second = timedelta.total_seconds()
        tthr = int(second // 3600)
        ttmin = int((second - (tthr * 3600)) // 60)
        tts = int((second - (tthr * 3600)) % 60)
        outstr = ''

        if tthr > 0:
            outstr = f'{tthr}:'
        if (tthr > 0) & (ttmin < 10):
            outstr += f'0{ttmin}:'
        else:
            outstr += f'{ttmin}:'
        if tts < 10:
            outstr += f'0{tts}'
        else:
            outstr += f'{tts}'

        return outstr

    # command &&rr, lazy version of &&remove
    @commands.command()
    async def rr(self, ctx, q_num=None):
        await ctx.invoke(self.client.get_command('remove'), q_num=q_num)

    # command &&remove, remove song in queue
    @commands.command()
    async def remove(self, ctx, q_num=None):
        global queue, misc
        serverID = ctx.message.guild.id
        embed = discord.Embed()
        if misc[serverID] < 0:
            embed.description = 'No song in queue for you to remove.'
            await ctx.send(embed=embed)
            return

        if q_num != None:
            rr_q = int(q_num)
            
            if (rr_q - 1) > misc[serverID]:
                embed.description = 'Dont have such many song.'
                await ctx.send(embed=embed)
                return
            elif (rr_q - 1) < 0:
                embed.description = 'Invalid number.'
                await ctx.send(embed=embed)
                return
            else:
                embed.title = 'Removed from queue'
                embed.description = f'[{queue[serverID][rr_q-1].title} by {queue[serverID][rr_q-1].uploader}]({queue[serverID][rr_q-1].yt_url})'
                await ctx.send(embed=embed)
                queue[serverID].pop(rr_q-1)
                misc[serverID] -= 1
                return
        else:
            output = '```CSS\r\n[Input the queue number you want to remove the song]\r\n'
            for i in range(misc[serverID]+1):
                output += f'{i+1}: {queue[serverID][i].title}\r\n'
            output += 'c: Cancel action'
            output += '```'
            await ctx.send(output)
            msg = await self.client.wait_for('message', check=lambda message: (message.author == ctx.author) & (message.channel == ctx.channel), timeout=None)
            q_num2 = msg.content
            if q_num2 == 'c':
                embed.description = 'Action cancelled.'
                await ctx.send(embed=embed)
                return
            else:
                rr_q2 = int(q_num2)
                if (rr_q2 - 1) > misc[serverID]:
                    embed.description = 'Dont have such many song. Action cancelled.'
                    await ctx.send(embed=embed)
                    return
                elif (rr_q2 - 1) < 0:
                    embed.description = 'Invalid number. Action cancelled.'
                    await ctx.send(embed=embed)
                    return
                else:
                    embed.title = 'Removed from queue'
                    embed.description = f'[{queue[serverID][rr_q2-1].title} by {queue[serverID][rr_q2-1].uploader}]({queue[serverID][rr_q2-1].yt_url})'
                    await ctx.send(embed=embed)
                    queue[serverID].pop(rr_q2-1)
                    misc[serverID] -= 1
                    return

def setup(nbot):
    nbot.add_cog(music(nbot))

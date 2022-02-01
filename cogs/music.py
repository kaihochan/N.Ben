from time import time
from urllib import request
import discord
from discord import embeds
from discord.channel import VoiceChannel
from discord.ext import commands
import youtube_dl
import datetime

# import json file, youtube email and password inside
import json
with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

# globol variable
# queue for multimedia flow control
FFMPEG_OPT = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
queue = []; ctr00 = -1
v_title_pe = None; v_url_pe = None; v_uploader_pe = None; request_pe = None
url2_pass = None

# global variable
# time calculation for &&np
timeNow = None; timeVideo = None; timeStart = None; timeEnd = None

# multimedia related function
class music(commands.Cog):
    def __init__(self, nbot):
        self.client = nbot

    # event trigger by load_queue(ctx)
    @commands.Cog.listener()
    async def on_queue_load(self, ctx):
        global url2_pass
        source = await discord.FFmpegOpusAudio.from_probe(url2_pass, **FFMPEG_OPT)
        ctx.voice_client.play(source, after=lambda x=None: self.load_queue(ctx=ctx))
        embed2 = discord.Embed()
        embed2.title = f'Now Playing 🎵 {v_title_pe} by {v_uploader_pe}'
        embed2.url = v_url_pe
        embed2.description = f'Queued by [{request_pe}]'
        await ctx.send(embed=embed2)

    # called by play after finish a song, trigger event to show info of next song
    def load_queue(self, ctx):
        global ctr00, v_title_pe, v_url_pe, v_uploader_pe, request_pe, timeVideo, timeStart, timeEnd
        global url2_pass
        if ctr00 != -1:
                url2_pass = queue[0][0]
                v_title_pe = queue[0][1]
                v_url_pe = queue[0][2]
                v_uploader_pe = queue[0][3]
                request_pe = queue[0][4]
                timeVideo = datetime.timedelta(seconds=queue[0][5])
                timeStart = datetime.datetime.now()
                timeEnd = timeStart + timeVideo
                queue.pop(0)
                ctr00 -= 1
                self.client.dispatch("queue_load", ctx)
        elif ctr00 == -1:
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
        voice_ch = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_ch.connect()
            embed.description = f'✅ Joined and bonded to `{voice_ch}`'
            await ctx.send(embed=embed)
        else:
            await ctx.voice_client.move_to(voice_ch)
            embed.description = f'➡️ Changed channel from `{ctx.voice_client.channel}` to `{voice_ch}`'
            await ctx.send(embed=embed)

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
        global ctr00, v_title_pe, v_url_pe, v_uploader_pe, request_pe, timeVideo, timeStart, timeEnd
        global FFMPEG_OPT
        embed = discord.Embed()
        if ctx.author.voice is None:
            embed.description = "❎ You are not in any voice channel, can't play any song"
            await ctx.send(embed=embed)
            return
        if ctx.voice_client is None:
            await ctx.invoke(self.join)

        YDL_OPT = { 'format': 'bestaudio', 
                    'username': jdata['YT_EMAIL'], 
                    'password': jdata['YT_PW'], 
                    'cookiefile': 'cookies.txt',
                    'proxy': jdata['YT-DL_PROXY'],
                    'geo_bypass_country': 'JP'}
        v_client = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPT) as ytDL:
            info = ytDL.extract_info(url, download=False)
            v_title = info.get('title', None)
            v_url = info.get('url', None)
            v_uploader = info.get('uploader', None)
            v_duration = info.get('duration', None)
            url2 = info['formats'][0]['url']
            
        if v_client.is_playing():
            ctr00 += 1
            queue.append([url2, v_title, v_url, v_uploader, ctx.author.mention, v_duration])
            embed2 = discord.Embed(title=f'Added to queue, position {ctr00+1}')
            embed2.description = f'[{v_title} by {v_uploader}]({url})\r\nQueued by [{ctx.author.mention}]'
            await ctx.send(embed=embed2)
            return     
        
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPT)
        v_title_pe = v_title
        v_url_pe = v_url
        v_uploader_pe = v_uploader
        request_pe = ctx.author.mention
        timeVideo = datetime.timedelta(seconds=v_duration)
        timeStart = datetime.datetime.now()
        timeEnd = timeStart + timeVideo

        v_client.play(source, after=lambda x=None: self.load_queue(ctx=ctx))
        embed.title = f'Now Playing 🎵 {v_title_pe} by {v_uploader_pe}'
        embed.url = v_url_pe
        embed.description = f'Queued by [{request_pe}]'
        await ctx.send(embed=embed)

    # command &&fs, lazy version of &&skip
    @commands.command()
    async def fs(self, ctx):
        await ctx.invoke(self.client.get_command('skip'))

    # command &&skip, skip song and load next song
    @commands.command()
    async def skip(self, ctx):
        global ctr00, v_title_pe, v_url_pe, v_uploader_pe, request_pe, timeVideo, timeStart, timeEnd
        global FFMPEG_OPT
        embed = discord.Embed()

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
        if ctr00 != -1:
                url2 = queue[0][0]
                v_title_pe = queue[0][1]
                v_url_pe = queue[0][2]
                v_uploader_pe = queue[0][3]
                request_pe = queue[0][4]
                timeVideo = datetime.timedelta(seconds=queue[0][5])
                timeStart = datetime.datetime.now()
                timeEnd = timeStart + timeVideo
                queue.pop(0)
                ctr00 -= 1

                source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPT)
                ctx.voice_client.play(source, after=lambda x=None: self.load_queue(ctx=ctx))
                embed2 = discord.Embed()
                embed2.title = f'Now Playing 🎵 {v_title_pe} by {v_uploader_pe}'
                embed2.url = v_url_pe
                embed2.description = f'Queued by [{request_pe}]'
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
        global ctr00
        embed = discord.Embed()
        if ctr00 == -1:
            embed.description = 'Queue is empty!'
            await ctx.send(embed=embed)
        elif ctr00 != -1:
            output = '```CSS\r\n[Songs in queue]\r\n'
            for i in range(ctr00+1):
                output += f'{i+1}: {queue[i][1]}\r\n'
            output += '```'
            await ctx.send(output)

    # command &&np, check now playing
    @commands.command()
    async def np(self, ctx):
        global v_title_pe, v_url_pe, v_uploader_pe, request_pe, timeNow, timeStart, timeEnd
        embed = discord.Embed()
        if ctx.voice_client is None:
            embed.description = 'I am not in a voice channel.'
            await ctx.send(embed=embed)
            return
        
        if ctx.voice_client.is_playing():
            timeNow = datetime.datetime.now()
            timePast = timeNow - timeStart
            timeDuration = timeEnd - timeStart
            Factor = int(timePast / timeDuration * 20)
            StatusBar = ['▱'] * 20
            for n in range(Factor+1):
                StatusBar[n] = '▰'
            StatusBarString = ''.join(StatusBar)
            embed.title = f'Now Playing 🎵 {v_title_pe} by {v_uploader_pe}'
            embed.url = v_url_pe
            embed.description = f'Queued by [{request_pe}]\r\n{self.timedelta_str(ctx, timePast)} {StatusBarString} {self.timedelta_str(ctx, timeDuration)}'
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
        global ctr00
        if q_num != None:
            rr_q = int(q_num)
            embed = discord.Embed()
            if ctr00 < 0:
                embed.description = 'No song in queue for you to remove.'
                await ctx.send(embed=embed)
                return
            elif (rr_q - 1) > ctr00:
                embed.description = 'Dont have such many song.'
                await ctx.send(embed=embed)
                return
            elif (rr_q - 1) < 0:
                embed.description = 'Invalid number.'
                await ctx.send(embed=embed)
                return
            else:
                embed.title = 'Removed from queue'
                embed.description = f'[{queue[rr_q-1][1]} by {queue[rr_q-1][3]}]({queue[rr_q-1][2]})'
                await ctx.send(embed=embed)
                queue.pop(rr_q-1)
                ctr00 -= 1
                return
        else:
            embed2 = discord.Embed()
            if ctr00 < 0:
                embed2.description = 'No song in queue for you to remove.'
                await ctx.send(embed=embed2)
                return
            else:
                output = '```CSS\r\n[Input the queue number you want to remove the song]\r\n'
                for i in range(ctr00+1):
                    output += f'{i+1}: {queue[i][1]}\r\n'
                output += 'c: Cancel action'
                output += '```'
                await ctx.send(output)
                msg = await self.client.wait_for('message', check=lambda message: (message.author == ctx.author) & (message.channel == ctx.channel), timeout=None)
                q_num2 = msg.content
                if q_num2 == 'c':
                    embed2.description = 'Action cancelled.'
                    await ctx.send(embed=embed2)
                    return
                else:
                    rr_q2 = int(q_num2)
                    if (rr_q2 - 1) > ctr00:
                        embed2.description = 'Dont have such many song. Action cancelled.'
                        await ctx.send(embed=embed2)
                        return
                    elif (rr_q2 - 1) < 0:
                        embed2.description = 'Invalid number. Action cancelled.'
                        await ctx.send(embed=embed2)
                        return
                    else:
                        embed2.title = 'Removed from queue'
                        embed2.description = f'[{queue[rr_q2-1][1]} by {queue[rr_q2-1][3]}]({queue[rr_q2-1][2]})'
                        await ctx.send(embed=embed2)
                        queue.pop(rr_q2-1)
                        ctr00 -= 1
                        return

def setup(nbot):
    nbot.add_cog(music(nbot))

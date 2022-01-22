from urllib import request
import discord
from discord import embeds
from discord.channel import VoiceChannel
from discord.ext import commands
import youtube_dl

# import json file, youtube email and password inside
import json
with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

# globol variable
# queue for multimedia flow control
queue = []; ctr00 = -1
v_title_pe = None; v_url_pe = None; v_uploader_pe = None; request_pe = None

# multimedia related function
class music(commands.Cog):
    def __init__(self, nbot):
        self.client = nbot

    # event trigger by load_queue(ctx)
    @commands.Cog.listener()
    async def on_queue_load(self, ctx):
        embed2 = discord.Embed()
        embed2.title = f'Now Playing 🎵 {v_title_pe} by {v_uploader_pe}'
        embed2.url = v_url_pe
        embed2.description = f'Queued by [{request_pe}]'
        await ctx.send(embed=embed2)

    # called by play after finish a song, trigger event to show info of next song
    def load_queue(self, ctx):
        global ctr00, v_title_pe, v_url_pe, v_uploader_pe, request_pe
        if ctr00 != -1:
                source_q = queue[0][0]
                v_title_pe = queue[0][1]
                v_url_pe = queue[0][2]
                v_uploader_pe = queue[0][3]
                request_pe = queue[0][4]
                queue.pop(0)
                ctr00 -= 1
                ctx.voice_client.play(source_q, after=lambda x=None: self.load_queue(ctx=ctx))
                self.client.dispatch("queue_load", ctx)
    
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
        global ctr00
        embed = discord.Embed()
        if ctx.author.voice is None:
            embed.description = "❎ You are not in any voice channel, can't play any song"
            await ctx.send(embed=embed)
            return
        if ctx.voice_client is None:
            await ctx.invoke(self.join)

        FFMPEG_OPT = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPT = {'format': "bestaudio", 'username': jdata['YT_EMAIL'], 'password': jdata['YT_PW']}
        v_client = ctx.voice_client
        with youtube_dl.YoutubeDL(YDL_OPT) as ytDL:
            info = ytDL.extract_info(url, download=False)
            v_title = info.get('title', None)
            v_url = info.get("url", None)
            v_uploader = info.get("uploader", None)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPT)
            
        if v_client.is_playing():
            ctr00 += 1
            queue.append([source, v_title, v_url, v_uploader, ctx.author.mention])
            embed2 = discord.Embed(title=f'Added to queue, position {ctr00+1}')
            embed2.description = f'[{v_title} by {v_uploader}]({url})\r\nQueued by [{ctx.author.mention}]'
            await ctx.send(embed=embed2)
            return
        elif not(v_client.is_playing()):
            if ctr00 == -1:
                source_q = source
                v_title_q = v_title
                v_url_q = v_url
                v_uploader_q = v_uploader
                request_q = ctx.author.mention
        
        v_client.play(source_q, after=lambda x=None: self.load_queue(ctx=ctx))
        embed.title = f'Now Playing 🎵 {v_title_q} by {v_uploader_q}'
        embed.url = v_url_q
        embed.description = f'Queued by [{request_q}]'
        await ctx.send(embed=embed)

    # command &&fs, lazy version of &&skip
    @commands.command()
    async def fs(self, ctx):
        await ctx.invoke(self.client.get_command('skip'))

    # command &&skip, skip song and load next song
    @commands.command()
    async def skip(self, ctx):
        global ctr00
        ctx.voice_client.stop()
        embed = discord.Embed(description="⏭️ Skipped")
        await ctx.send(embed=embed)
        if ctr00 != -1:
                source_q = queue[0][0]
                v_title_q = queue[0][1]
                v_url_q = queue[0][2]
                v_uploader_q = queue[0][3]
                request_q = queue[0][4]
                queue.pop(0)
                ctr00 -= 1
                ctx.voice_client.play(source_q, after=lambda x=None: self.load_queue(ctx=ctx))
                embed2 = discord.Embed()
                embed2.title = f'Now Playing 🎵 {v_title_q} by {v_uploader_q}'
                embed2.url = v_url_q
                embed2.description = f'Queued by [{request_q}]'
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

def setup(nbot):
    nbot.add_cog(music(nbot))

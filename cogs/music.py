import discord
from discord.channel import VoiceChannel
from discord.ext import commands
import youtube_dl

# multimedia related function
class music(commands.Cog):
    def __init__(self, nbot):
        self.client = nbot

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

    # command &&discon, leave voice channel
    @commands.command()
    async def discon(self, ctx):
        await ctx.voice_client.disconnect()
        embed = discord.Embed(description='🛄 Leave channel to find backpack')
        await ctx.send(embed=embed)
    
    # command &&play url, play youtube/youtube-dl supported video
    @commands.command()
    async def play(self, ctx, url):
        embed = discord.Embed()
        if ctx.author.voice is None:
            embed.description = "❎ You are not in any voice channel, can't play any song"
            await ctx.send(embed=embed)
            return
        if ctx.voice_client is None:
            await ctx.invoke(self.join)
        ctx.voice_client.stop()
        FFMPEG_OPT = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPT = {'format': "bestaudio"}
        v_client = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPT) as ytDL:
            info = ytDL.extract_info(url, download=False)
            v_title = info.get('title', None)
            v_url = info.get("url", None)
            v_uploader = info.get("uploader", None)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPT)
            v_client.play(source)
        
        embed.title = f'Now Playing 🎵 {v_title} by {v_uploader}'
        embed.url = v_url
        embed.description = f'Queued by [{ctx.author.mention}]'
        await ctx.send(embed=embed)

        

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

def setup(nbot):
    nbot.add_cog(music(nbot))

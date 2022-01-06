import discord
from discord.channel import VoiceChannel
from discord.ext import commands
import youtube_dl

class music(commands.Cog):
    def __init__(self, nbot):
        self.client = nbot

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send('You are not in any voice channel')
        voice_ch = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_ch.connect()
        else:
            await ctx.voice_client.move_to(voice_ch)
        
    @commands.command()
    async def discon(self, ctx):
        await ctx.voice_client.disconnect()
    
    @commands.command()
    async def play(self, ctx, url):
        ctx.voice_client.stop()
        FFMPEG_OPT = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPT = {'format': "bestaudio"}
        v_client = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPT) as ytDL:
            info = ytDL.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPT)
            v_client.play(source)

def setup(nbot):
    nbot.add_cog(music(nbot))

import discord
from discord.ext import commands
import yt_dlp
import datetime
import re
import asyncio

class Server:
    def __init__(self) -> None:
        self.queue: list[Queue] = []
        self.play_current: Queue = None
        self.play_duration: datetime.timedelta = None
        self.play_at: datetime.datetime = None
        self.loop: bool = False

class Song:
    def __init__(self) -> None:
        pass

class Queue:
    def __init__(self, url2=None, title=None, yt_url=None, uploader=None, pusher=None, duration=None):
        self.url2 = url2
        self.title = title
        self.yt_url = yt_url
        self.uploader = uploader
        self.pusher = pusher
        self.duration: float = duration

FFMPEG_OPT = {  'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
                'options': '-vn'}
YDL_OPT = { 'format': 'bestaudio',
            'perfer_ffmpeg': True,
            'cookiefile': 'settings/cookies.txt',
            'geo_bypass_country': 'JP',
            'ignoreerrors': True}

class Music(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.music_server: dict[str, Server] = {}

    def timedelta_to_str(self, timedelta: datetime.timedelta) -> str:
        string = str(timedelta)
        return (string if string[0] != "0" else string[2:]).split('.')[0]

    async def load_queue(self, ctx: commands.Context) -> None:
        server_id = ctx.message.guild.id
        if not self.music_server[server_id].loop:
            if len(self.music_server[server_id].queue) > 0:
                self.music_server[server_id].play_current = self.music_server[server_id].queue.pop(0)
            else:
                return ctx.voice_client.stop()
        await self.play_source(ctx=ctx)

    async def remove_queue(self, ctx: commands.Context, number: int) -> None:
        server_id = ctx.message.guild.id
        embed = discord.Embed()
        if -1 < number < len(self.music_server[server_id].queue):
            embed.title = "Removed from queue"
            embed.description = f"[{self.music_server[server_id].queue[number].title} by {self.music_server[server_id].queue[number].uploader}]({self.music_server[server_id].queue[number].yt_url})"
            self.music_server[server_id].queue.pop(number)
            return await ctx.send(embed=embed)
        else:
            embed.description = "Invalid number."
            return await ctx.send(embed=embed)

    async def add_source(self, ctx: commands.Context, video: "dict[str]") -> None:
        embed = discord.Embed()
        server_id = ctx.message.guild.id
        title = video.get('title', None)
        url = video.get('webpage_url', None)
        channel = video.get('channel', None)
        time = video.get('duration', None)
        for formats in video['formats']:
            if not re.search(r"(ytimg)|(manifest)", formats['url'], re.IGNORECASE):
                url2 = formats['url']
                break
        if ctx.voice_client.is_playing():
            self.music_server[server_id].queue.append(Queue(url2, title, url, channel, ctx.author.mention, time))
            embed.title = f"Added to queue, position {len(self.music_server[server_id].queue)}"
            embed.description = f'[{title} by {channel}]({url})\r\nQueued by [{ctx.author.mention}]'
            return await ctx.send(embed=embed)
        self.music_server[server_id].play_current = Queue(url2, title, url, channel, ctx.author.mention, time)
        await self.play_source(ctx=ctx)
    
    async def play_source(self, ctx: commands.Context) -> None:
        server_id = ctx.message.guild.id
        self.music_server[server_id].play_duration = datetime.timedelta(seconds=self.music_server[server_id].play_current.duration)
        self.music_server[server_id].play_at = datetime.datetime.now()
        source = await discord.FFmpegOpusAudio.from_probe(self.music_server[server_id].play_current.url2, **FFMPEG_OPT)
        ctx.voice_client.play(source, after=lambda x=None: asyncio.run_coroutine_threadsafe(self.load_queue(ctx=ctx), self.client.loop))
        embed = discord.Embed(
            title=f"Now Playing 🎵 {self.music_server[server_id].play_current.title} by {self.music_server[server_id].play_current.uploader}",
            url=self.music_server[server_id].play_current.yt_url,
            description=f"Queued by [{self.music_server[server_id].play_current.pusher}]",
            )
        await ctx.send(embed=embed)

    @commands.command(aliases=['pg'])
    async def clear(self, ctx: commands.Context) -> None:
        """Clear songs in queue."""
        server_id = ctx.message.guild.id
        self.music_server[server_id].queue.clear()
        embed = discord.Embed(description="🚮 Queue cleared")
        await ctx.send(embed=embed)

    @commands.command(aliases=['ds'])
    async def disconnect(self, ctx: commands.Context) -> None:
        """Leave voice channel."""
        await ctx.voice_client.disconnect()
        embed = discord.Embed(description="🛄 Leave channel to find backpack")
        await ctx.send(embed=embed)

    @commands.command(aliases=['j'])
    async def join(self, ctx:commands.Context) -> None:
        """Join/change voice channel."""
        embed = discord.Embed()
        if ctx.author.voice is None:
            embed.description = "❎ You are not in any voice channel"
            return await ctx.send(embed=embed)
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            embed.description = f'✅ Joined and bonded to `{voice_channel}`'
            await ctx.send(embed=embed)
        else:
            await ctx.voice_client.move_to(voice_channel)
            embed.description = f'➡️ Changed channel from `{ctx.voice_client.channel}` to `{voice_channel}`'
            await ctx.send(embed=embed)
        server_id = ctx.message.guild.id
        if server_id not in self.music_server:
            self.music_server[server_id] = Server()

    @commands.command()
    async def loop(self, ctx: commands.Context) -> None:
        """Enable/disable looping song."""
        server_id = ctx.message.guild.id
        self.music_server[server_id].loop = not self.music_server[server_id].loop
        embed = discord.Embed(description="🔂 Looping ON" if self.music_server[server_id].loop else "🔂 Looping OFF")
        await ctx.send(embed=embed)

    @commands.command(aliases=['np'])
    async def nowplaying(self, ctx: commands.Context) -> None:
        """Check now playing."""
        embed = discord.Embed()
        if ctx.voice_client is None:
            embed.description = 'I am not in a voice channel.'
            return await ctx.send(embed=embed)
        server_id = ctx.message.guild.id
        if ctx.voice_client.is_playing():
            time_played = datetime.datetime.now() - self.music_server[server_id].play_at
            factor = int(time_played / self.music_server[server_id].play_duration * 20) + 1
            progress = ['▱'] * 20
            for n in range(factor):
                progress[n] = '▰'
            embed.title = f'Now Playing 🎵 {self.music_server[server_id].play_current.title} by {self.music_server[server_id].play_current.uploader}'
            embed.url = self.music_server[server_id].play_current.yt_url
            embed.description = f"Queued by [{self.music_server[server_id].play_current.pusher}]\r\n{self.timedelta_to_str(time_played)} {''.join(progress)} {self.timedelta_to_str(self.music_server[server_id].play_duration)}"
        else:
            embed.description = 'No song is playing now.'
        await ctx.send(embed=embed)

    @commands.command(aliases=['p'])
    async def play(self, ctx: commands.Context, url: str) -> None:
        """Play youtube/youtube-dl supported video."""
        global FFMPEG_OPT, YDL_OPT
        if ctx.author.voice is None:
            embed = discord.Embed(description="❎ You are not in any voice channel, can't play any song")
            return await ctx.send(embed=embed)
        if ctx.voice_client is None:
            await ctx.invoke(self.join)
        with yt_dlp.YoutubeDL(YDL_OPT) as ytDL:
            if re.search(r"list=", url):
                start = False
                if re.search(r"youtu.be", url):
                    id = re.match(r"https://youtu.be/([\w-]{11})", url).group(1)
                    video = ytDL.extract_info(f"https://youtu.be/{id}", download=False)
                    await self.add_source(ctx, video)
                elif re.search(r"watch", url):
                    id = re.match(r"https://www.youtube.com/watch\?v=([\w-]{11})", url).group(1)
                    video = ytDL.extract_info(f"https://youtu.be/{id}", download=False)
                    await self.add_source(ctx, video)
                else:
                    id = None
                    start = True
                info = ytDL.extract_info(url, download=False)
                for video in info["entries"]:
                    if video is None:
                        continue
                    if start:
                        await self.add_source(ctx, video)
                    if video.get('id', None) == id:
                        start = True
            else:
                video = ytDL.extract_info(url, download=False)
                await self.add_source(ctx, video)
    
    @commands.command(aliases=['q'])
    async def queue(self, ctx: commands.Context) -> None:
        """Check songs in queue."""
        server_id = ctx.message.guild.id
        if len(self.music_server[server_id].queue) == 0:
            embed = discord.Embed(description="Queue is empty!")
            await ctx.send(embed=embed)
        else:
            output = "```CSS\r\n[Songs in queue]\r\n"
            for i in range(len(self.music_server[server_id].queue)):
                output += f"{i+1}: {self.music_server[server_id].queue[i].title}\r\n"
            output += "```"
            await ctx.send(output)

    @commands.command(aliases=['r'])
    async def remove(self, ctx: commands.Context, number: int = None) -> None:
        """Remove song in queue."""
        server_id = ctx.message.guild.id
        embed = discord.Embed()
        if len(self.music_server[server_id].queue) == 0:
            embed.description = "No song in queue for you to remove."
            return await ctx.send(embed=embed)
        if number is not None:
            await self.remove_queue(ctx=ctx, number=number-1)
        else:
            output = "```CSS\r\n[Input the queue number you want to remove the song]\r\n"
            for i in range(len(self.music_server[server_id].queue)):
                output += f"{i+1}: {self.music_server[server_id].queue[i].title}\r\n"
            output += "c: Cancel action"
            output += "```"
            await ctx.send(output)
            msg = await self.client.wait_for("message", check=lambda message: (message.author == ctx.author) & (message.channel == ctx.channel), timeout=None)
            if msg.content == 'c':
                embed.description = "Action cancelled."
                return await ctx.send(embed=embed)
            else:
                number = int(msg.content)
                await self.remove_queue(ctx=ctx, number=number-1)

    @commands.command(aliases=['fs'])
    async def skip(self, ctx: commands.Context) -> None:
        """Skip song and load next song."""
        embed = discord.Embed()
        server_id = ctx.message.guild.id
        if ctx.voice_client is None:
            embed.description = 'I am not in a voice channel.'
            return await ctx.send(embed=embed)
        if not ctx.voice_client.is_playing():
            embed.description = 'I am not playing anything.'
            return await ctx.send(embed=embed)
        ctx.voice_client.stop()
        embed.description = "⏭️ Skipped"
        await ctx.send(embed=embed)
        if len(self.music_server[server_id].queue) > 0:
            self.music_server[server_id].play_current = self.music_server[server_id].queue.pop(0)
            await self.play_source(ctx=ctx)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Music(client))

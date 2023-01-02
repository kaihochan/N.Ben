import discord
from discord.ext import commands
import yt_dlp
from datetime import datetime, timedelta
import re
import asyncio

class Song:
    def __init__(self, title, url, uploader, requester, duration) -> None:
        self.title: str = title
        self.url: str = url
        self.uploader: str = uploader
        self.requester: str = requester
        self.duration: timedelta = timedelta(seconds=duration)

class Server:
    def __init__(self) -> None:
        self.current_song: Song = None
        self.play_at: datetime = None
        self.__queue: list[Song] = []
        self.__loop: bool = False
        self.__loop_list: bool = False

    def __enter__(self) -> "Server":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    def size(self) -> int:
        return len(self.__queue)

    def iterator(self) -> enumerate[Song]:
        return enumerate(self.__queue)
    
    def empty(self) -> bool:
        return len(self.__queue) == 0

    def enqueue(self, song: Song) -> None:
        self.__queue.append(song)

    def dequeue(self) -> None:
        if self.__loop | self.empty():
            return
        if self.__loop_list:
            self.__queue.append(self.current_song)
        self.current_song = self.__queue.pop(0)
        self.play_at = datetime.now()
    
    def remove(self, index: int) -> Song:
        return self.__queue.pop(index)

    def clear(self) -> None:
        self.__queue = []

    def toggle_loop(self) -> bool:
        self.__loop = not self.__loop
        if self.__loop & self.__loop_list:
            self.__loop_list = False
        return self.__loop
    
    def toggle_loop_list(self) -> bool:
        self.__loop_list = not self.__loop_list
        if self.__loop & self.__loop_list:
            self.__loop = False
        return self.__loop_list
    
    def loop(self) -> bool:
        return self.__loop | self.__loop_list

class Music(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.music_server: dict[str, Server] = {}
        self.FFMPEG_OPT = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
            'options': '-vn'
            }
        self.YTDLP_OPT = { 
            'format': 'bestaudio',
            'perfer_ffmpeg': True,
            'cookiefile': 'settings/cookies.txt',
            'ignoreerrors': True,
            'skip_download': True,
            'extract_flat': 'in_playlist'
            }

    def timedelta_to_str(self, timedelta: timedelta) -> str:
        string = str(timedelta)
        return (string if string[0] != "0" else string[2:]).split('.')[0]
    
    async def load_queue(self, ctx: commands.Context) -> None:
        with self.music_server[ctx.message.guild.id] as server:
            if (not server.loop()) & server.empty():
                return ctx.voice_client.stop()
            server.dequeue()
            await self.play_source(ctx=ctx)

    async def add_source(self, ctx: commands.Context, video: "dict[str]") -> None:
        with self.music_server[ctx.message.guild.id] as server:
            if ctx.voice_client.is_playing():
                server.enqueue(Song(video.get('title'), video.get('webpage_url', video.get('url')), video.get('channel'), ctx.author.mention, video.get('duration')))
                return await ctx.send(embed=discord.Embed(
                                title = f"Added to queue, position {server.size()}",
                                description = f"[{video.get('title')} by {video.get('channel')}]({video.get('webpage_url', video.get('url'))})\r\nQueued by [{ctx.author.mention}]"
                                ))
            server.current_song = Song(video.get('title'), video.get('webpage_url', video.get('url')), video.get('channel'), ctx.author.mention, video.get('duration'))
            await self.play_source(ctx=ctx)
    
    async def play_source(self, ctx: commands.Context) -> None:
        with self.music_server[ctx.message.guild.id] as server:
            for formats in yt_dlp.YoutubeDL(self.YTDLP_OPT | {'extract_flat': False}).extract_info(server.current_song.url, download=False).get('formats'):
                if not re.search(r"(ytimg)|(manifest)", formats['url'], re.IGNORECASE):
                    source_url = formats['url']
                    break
            source = await discord.FFmpegOpusAudio.from_probe(source_url, **self.FFMPEG_OPT)
            ctx.voice_client.play(source, after=lambda x=None: asyncio.run_coroutine_threadsafe(self.load_queue(ctx=ctx), self.client.loop))
            await ctx.send(embed=discord.Embed(
                title=f"Now Playing 🎵 {server.current_song.title} by {server.current_song.uploader}",
                url=server.current_song.url,
                description=f"Queued by [{server.current_song.requester}]"
                ))

    @commands.command(aliases=['c','pg'])
    async def clear(self, ctx: commands.Context) -> None:
        """Clear songs in queue."""
        self.music_server[ctx.message.guild.id].clear()
        await ctx.send(embed=discord.Embed(description="🚮 Queue cleared"))

    @commands.command(aliases=['ds'])
    async def disconnect(self, ctx: commands.Context) -> None:
        """Leave voice channel."""
        await ctx.voice_client.disconnect()
        await ctx.send(embed=discord.Embed(description="🛄 Leave channel to find backpack"))
    
    @commands.command(aliases=['j'])
    async def join(self, ctx:commands.Context) -> None:
        """Join/change voice channel."""
        if ctx.author.voice is None:
            return await ctx.send(embed=discord.Embed(description="❎ You are not in any voice channel"))
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
            await ctx.send(embed=discord.Embed(description=f"✅ Joined and bonded to `{ctx.author.voice.channel}`"))
        else:
            await ctx.voice_client.move_to(ctx.author.voice.channel)
            await ctx.send(embed=discord.Embed(description=f"➡️ Changed channel from `{ctx.voice_client.channel}` to `{ctx.author.voice.channel}`"))
        if ctx.message.guild.id not in self.music_server:
            self.music_server[ctx.message.guild.id] = Server()
    
    @commands.command(aliases=['l'])
    async def loop(self, ctx: commands.Context) -> None:
        """Enable/disable looping song."""
        await ctx.send(embed=discord.Embed(description="🔂 Looping ON" if self.music_server[ctx.message.guild.id].toggle_loop() else "🔂 Looping OFF"))
    
    @commands.command(aliases=['ll'])
    async def looplist(self, ctx: commands.Context) -> None:
        """Enable/disable looping song list."""
        await ctx.send(embed=discord.Embed(description="🔂 Looping list ON" if self.music_server[ctx.message.guild.id].toggle_loop_list() else "🔂 Looping list OFF"))

    @commands.command(aliases=['np'])
    async def nowplaying(self, ctx: commands.Context) -> None:
        """Check now playing."""
        if ctx.voice_client is None:
            return await ctx.send(embed=discord.Embed(description="I am not in a voice channel."))
        with self.music_server[ctx.message.guild.id] as server:
            if ctx.voice_client.is_playing():
                time_played = datetime.now() - server.play_at
                progress = ['▱'] * 20
                for n in range(int(time_played / server.current_song.duration * 20) + 1):
                    progress[n] = '▰'
                await ctx.send(embed=discord.Embed(
                    title=f"Now Playing 🎵 {server.current_song.title} by {server.current_song.uploader}",
                    url=server.current_song.url,
                    description=f"Queued by [{server.current_song.requester}]\n{self.timedelta_to_str(time_played)} {''.join(progress)} {self.timedelta_to_str(server.current_song.duration)}"
                    ))
            else:
                await ctx.send(embed=discord.Embed(description="No song is playing now."))

    @commands.command(aliases=['p'])
    async def play(self, ctx: commands.Context, *, keyword: str) -> None:
        """Play youtube/youtube-dl supported video."""
        if ctx.author.voice is None:
            return await ctx.send(embed=discord.Embed(description="❎ You are not in any voice channel, can't play any song"))
        if ctx.voice_client is None:
            await ctx.invoke(self.join)
        with yt_dlp.YoutubeDL(self.YTDLP_OPT) as ytDL:
            if ("youtube" in keyword) | ("youtu.be" in keyword):
                if "list=" not in keyword:
                    video = ytDL.extract_info(keyword, download=False)
                    await self.add_source(ctx, video)
                else:
                    id = re.search(r".?([\w-]{11})", keyword).group(1)
                    videos = ytDL.extract_info(keyword, download=False)['entries']
                    start = False
                    for video in videos:
                        if video is None:
                            continue
                        if video.get('id', None) == id:
                            start = True
                        if start:
                            try:
                                await self.add_source(ctx, video)
                            except:
                                pass
            else:
                videos = ytDL.extract_info(f"ytsearch5:{keyword}", download=False)['entries']
                output = "```CSS\r\n[Search results]\r\n"
                for index, video in enumerate(videos):
                    output += f"{index+1}: {video.get('title', None)}\r\n"
                output += "c: Cancel action```"
                await ctx.send(output)
                reply = await self.client.wait_for("message", check=lambda message: (message.author == ctx.author) & (message.channel == ctx.channel), timeout=None)
                try:
                    await self.add_source(ctx, ytDL.extract_info(videos[int(reply.content)-1].get('url'), download=False))
                except (ValueError, IndexError) as e:
                    await ctx.send("Action cancelled." if reply.content == "c" else "Invaild value.")

    @commands.command(aliases=['q'])
    async def queue(self, ctx: commands.Context) -> None:
        """Check songs in queue."""
        with self.music_server[ctx.message.guild.id] as server:
            if server.empty():
                await ctx.send(embed=discord.Embed(description="Queue is empty!"))
            else:
                output = "```CSS\n[Songs in queue]\n"
                for index, song in server.iterator():
                    output += f"{index+1}: {song.title}\n"
                output += "```"
                await ctx.send(output)

    @commands.command(aliases=['r'])
    async def remove(self, ctx: commands.Context, number: int = None) -> None:
        """Remove song in queue."""
        with self.music_server[ctx.message.guild.id] as server:
            if server.empty():
                return await ctx.send(embed=discord.Embed(description="No song in queue for you to remove."))
            if number is None:
                output = "```CSS\n[Input the queue number you want to remove the song]\n"
                for index, song in server.iterator():
                    output += f"{index+1}: {song.title}\n"
                output += "c: Cancel action```"
                await ctx.send(output)
                reply = await self.client.wait_for("message", check=lambda message: (message.author == ctx.author) & (message.channel == ctx.channel), timeout=None)
            try:
                if number is None:
                    number = int(reply.content)
                removed_song = server.remove(number-1)
                await ctx.send(embed=discord.Embed(
                    title="Removed from queue",
                    description=f"[{removed_song.title} by {removed_song.uploader}]({removed_song.url})"
                    ))
            except (ValueError, IndexError) as e:
                if reply.content == "c":
                    await ctx.send(embed=discord.Embed(description="Action cancelled."))
                else:
                    await ctx.send(embed=discord.Embed(description="Invaild value."))
    
    @commands.command(aliases=['fs', 's'])
    async def skip(self, ctx: commands.Context) -> None:
        """Skip song and load next song."""
        if ctx.voice_client is None:
            return await ctx.send(embed=discord.Embed(description="I am not in a voice channel."))
        if not ctx.voice_client.is_playing():
            return await ctx.send(embed=discord.Embed(description="I am not playing anything."))
        ctx.voice_client.stop()
        await ctx.send(embed=discord.Embed(description="⏭️ Skipped"))
        with self.music_server[ctx.message.guild.id] as server:
            server.dequeue()
            if not server.empty():
                await self.play_source(ctx=ctx)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Music(client))

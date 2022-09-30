import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import datetime
import regex as re
import json

class Events(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.prog_dw = re.compile(r"([\p{Unified_Ideograph=True}]+|\b)(achun)?(dw)(_xd|_owo)?([{\p{Unified_Ideograph=True}]+|\b)|([\u738b\u9ec3])?(\u4fca\u9298|\u6625\u51a5)|\u30c0\u30cb\u30a8\u30eb", re.IGNORECASE|re.UNICODE)
        self.prog_gay = re.compile(r"([\p{Unified_Ideograph=True}]+|\b)(gay)([\p{Unified_Ideograph=True}]+|\b)|\u57fa\u4f6c", re.IGNORECASE|re.UNICODE)
        self.prog_not = re.compile(r"\b(not)\b|[\u5514\u543e][\u4fc2\u7cfb]", re.IGNORECASE|re.UNICODE)
        self.prog_n_word = re.compile(r"\b(nigga)(s\b|\b)", re.IGNORECASE|re.UNICODE)
        self.prog_n_word_hard_r = re.compile(r"\b(nigger)(s\b|\b)", re.IGNORECASE|re.UNICODE)

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message) -> None:
        if (message.author.bot):
            return
        if ((self.prog_dw.search(message.content) is not None) & (self.prog_gay.search(message.content) is not None)):
            return await message.channel.send("No" if self.prog_not.search(message.content) is not None else "Yes")
        elif self.prog_dw.search(message.content):
            return await message.channel.send("Gay")
        elif self.prog_gay.search(message.content):
            return await message.channel.send("DW")
        for i in self.prog_n_word.finditer(message.content):
            if str(message.author.id) not in self.client.ndata:
                self.client.ndata[str(message.author.id)] = {"total": 0, "hard_r": 0, "last":0}
            self.client.ndata[str(message.author.id)]["total"] += 1
        for i in self.prog_n_word_hard_r.finditer(message.content):
            if str(message.author.id) not in self.client.ndata:
                self.client.ndata[str(message.author.id)] = {"total": 0, "hard_r": 0, "last":0}
            self.client.ndata[str(message.author.id)]["total"] += 1
            self.client.ndata[str(message.author.id)]["hard_r"] += 1
        with open('settings/nword.json', mode='w', encoding='utf8') as nfile:
            json.dump(self.client.ndata, nfile, ensure_ascii=False, indent=4)
            nfile.close()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> None:
        vcch = get(self.client.voice_clients, guild=member.guild)
        if (str(member.id) in self.client.kdata) & (after.channel is not None):
            if self.client.kdata[str(member.id)] > 0:
                await member.move_to(None)
                self.client.kdata[str(member.id)] -= 1
                with open('settings/kick.json', mode='w', encoding='utf8') as kfile:
                    json.dump(self.client.kdata, kfile, ensure_ascii=False, indent=4)
                    kfile.close()
                embed = discord.Embed(
                    title="Auto-kick counter",
                    description=f"User:\t\t{member.mention}\n",)
                embed.set_thumbnail(url=member.avatar_url)
                embed.add_field(
                    name='Kick count left',
                    value=self.client.kdata[str(member.id)])
                chList = []
                for ch in member.guild.text_channels:
                    chList.append(ch.name)
                if 'music' in chList:
                    return await member.guild.text_channels[chList.index('music')].send(embed=embed)
                elif '一般' in chList:
                    return await member.guild.text_channels[chList.index('一般')].send(embed=embed)
                elif 'general' in chList:
                    return await member.guild.text_channels[chList.index('general')].send(embed=embed)
                else:
                    return
        if (member.bot) | (before is None) | (vcch is None):
            return
        if vcch.channel != before.channel:
            return
        if after.channel == None:
            memNum = len(vcch.channel.members)
            if memNum == 1:
                print(f'[auto-countdown] {vcch.channel.name} in {vcch.guild.name} @ {datetime.datetime.now()}')
                await asyncio.sleep(60)
                await self.auto_disconnect(member, before)
  
    async def auto_disconnect(self, member:discord.Member, before:discord.VoiceState) -> None:
        vcch = get(self.client.voice_clients, guild=member.guild)
        if (before is None) | (vcch is None):
            return
        if vcch.channel != before.channel:
            return
        memNum = len(vcch.channel.members)
        if memNum != 1:
            return
        await vcch.disconnect()
        chList = []
        for ch in member.guild.text_channels:
            chList.append(ch.name)
        embed = discord.Embed()
        embed.description = '🛄 All people gone, leave channel to find backpack'
        print(f'[auto-disconnect] {vcch.channel.name} in {vcch.guild.name} @ {datetime.datetime.now()}')
        if 'music' in chList:
            return await member.guild.text_channels[chList.index('music')].send(embed=embed)
        elif '一般' in chList:
            return await member.guild.text_channels[chList.index('一般')].send(embed=embed)
        elif 'general' in chList:
            return await member.guild.text_channels[chList.index('general')].send(embed=embed)
        else:
            return

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Events(client))
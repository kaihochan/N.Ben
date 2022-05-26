import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import datetime
import re
import json
import os

class events(commands.Cog):
    def __init__(self, nbot):
        self.client = nbot

    # event trigger by message contain dw or gay
    # if message contain n-words, update json
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if (message.author.bot):
            return
        match_dw = re.search(r"\b(dw)\b", message.content, re.IGNORECASE)
        match_gay = re.search(r"\b(gay)\b", message.content, re.IGNORECASE)
        match_not = re.search(r"\b(not)\b", message.content, re.IGNORECASE)
        if (match_dw is not None) & (match_gay is not None):
            if match_not:
                return await message.channel.send('No')
            else:
                return await message.channel.send('Yes')
        elif match_dw:
            return await message.channel.send('Gay')
        elif match_gay:
            return await message.channel.send('DW')
        for i in re.finditer(r"\b(nigga)(s\b|\b)", message.content, re.IGNORECASE):
            if str(message.author.id) not in self.client.ndata:
                self.client.ndata[str(message.author.id)] = {'total': 0, 'hard_r': 0, 'last':0}
            self.client.ndata[str(message.author.id)]['total'] += 1
        for i in re.finditer(r"\b(nigger)(s\b|\b)", message.content, re.IGNORECASE):
            if str(message.author.id) not in self.client.ndata:
                self.client.ndata[str(message.author.id)] = {'total': 0, 'hard_r': 0, 'last':0}
            self.client.ndata[str(message.author.id)]['total'] += 1
            self.client.ndata[str(message.author.id)]['hard_r'] += 1
        with open('settings/nword.json', mode='w', encoding='utf8') as nfile:
            json.dump(self.client.ndata, nfile, ensure_ascii=False, indent=4)
            nfile.close()

    # event trigger by people leaving
    # if only bot in voice channel, bot will disconnect in 1 min time
    @commands.Cog.listener()
    async def on_voice_state_update(self, member:discord.Member, before:discord.VoiceState, after:discord.VoiceState):
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

    # late function call by on_voice_state_update to disconnect the bot     
    async def auto_disconnect(self, member:discord.Member, before:discord.VoiceState):
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

def setup(nbot):
    nbot.add_cog(events(nbot))
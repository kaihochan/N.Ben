import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import datetime
import os

class events(commands.Cog):
    def __init__(self, nbot):
        self.client = nbot

    # event trigger by message contain dw or gay
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if (message.author.bot):
            return
        GayList = ['GAY', 'GAy', 'GaY', 'Gay', 'gAY', 'gAy', 'gaY', 'gay']
        dwList = ['DW', 'dw', 'Dw', 'dW', 'ダニエル']
        for i in range(len(GayList)):
            for j in range(len(dwList)):
                if (GayList[i] in message.content) & (dwList[j] in message.content):
                    if ('not' in message.content):
                        await message.channel.send('No')
                    else:
                        await message.channel.send('Yes')
                    return
        for k in range(len(dwList)):
            if dwList[k] in message.content:
                await message.channel.send('Gay')
                return
        for n in range(len(GayList)):
            if GayList[n] in message.content:
                await message.channel.send('DW')
                return

    # event trigger by people leaving
    # if only bot in voice channel, bot will disconnect in 1 min time
    @commands.Cog.listener()
    async def on_voice_state_update(self, member:discord.Member, before:discord.VoiceState, after:discord.VoiceState):
        vcch = get(self.client.voice_clients, guild=member.guild)
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
            await member.guild.text_channels[chList.index('music')].send(embed=embed)
            return
        elif '一般' in chList:
            await member.guild.text_channels[chList.index('一般')].send(embed=embed)
            return
        elif 'general' in chList:
            await member.guild.text_channels[chList.index('general')].send(embed=embed)
            return
        else:
            return

def setup(nbot):
    nbot.add_cog(events(nbot))
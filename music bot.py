import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print(f'{client.user} logged in')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
    
#     if message.content.startswith('cool'):
#         await message.channel.send('Cool beans')

@client.command()
async def play(ctx, url):
    if ctx.author.voice:
        voiceChannel = ctx.author.voice.channel
        print('first')
    else:
        voiceChannel = discord.utils.get(ctx.guild.voice_channels)
        if not voiceChannel:
            await ctx.channel.send('There are no voice channels dickhead')
            return

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None:
        if not voice.is_connected():
            await voice.disconnect()
            await voiceChannel.connect()
    else:
        await voiceChannel.connect()

client.run(os.getenv('TOKEN'))
import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix='bt ')

@client.event
async def on_ready():
    print(f'{client.user} logged in')

@client.event
async def on_disconnect():
    for voice in client.voice_clients:
        voice.disconnect()

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
    else:
        voiceChannel = discord.utils.get(ctx.guild.voice_channels)
        if not voiceChannel:
            await ctx.channel.send('There are no voice channels dickhead')
            return

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is None:
        voice = await voiceChannel.connect()
    elif not voice.is_connected() or voice.channel != voiceChannel:
        await voice.disconnect(force=True)
        voice = await voiceChannel.connect()

client.run(os.getenv('TOKEN'))
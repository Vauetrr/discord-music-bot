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
    voiceChannel, voice = await join(ctx)

@client.command()
async def join(ctx):
    if ctx.author.voice:
        voiceChannel = ctx.author.voice.channel
    else:
        voiceChannel = discord.utils.get(ctx.guild.voice_channels)
        if not voiceChannel:
            await ctx.send('There are no voice channels dickhead')
            return

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is None:
        voice = await voiceChannel.connect()
    elif not voice.is_connected() or voice.channel != voiceChannel:
        await voice.disconnect(force=True)
        voice = await voiceChannel.connect()

    return (voiceChannel, voice)

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None and voice.is_connected():
        await voice.disconnect(force=True)
    else:
        ctx.send("tf you on about")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None and voice.is_playing():
        voice.pause()
    else:
        await ctx.send("don't disrespect the bao tan")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None and voice.is_paused():
        voice.resume()
    else:
        await ctx.send("\"shush\" - Bao Tan")

client.run(os.getenv('TOKEN'))
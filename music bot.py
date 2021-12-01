import discord
import os
from discord import FFmpegPCMAudio
from discord.ext import commands
from youtube_dl import YoutubeDL

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
    voice = await join(ctx)
    if voice is None:
        await ctx.send("huh?")
        return
        
    ydl_ops = {'format': 'bestaudio/best', 'noplaylist': 'True'}
    ffmpeg_ops = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 4294', 'options': '-vn'}

    if not voice.is_playing():
        with YoutubeDL(ydl_ops) as ydl:
            info = ydl.extract_info(url, download=False)
        newUrl = info['url']
        voice.play(FFmpegPCMAudio(newUrl, **ffmpeg_ops))
    else:
        await ctx.send("\"patience is patience\" - Sun Tzu")

@client.command()
async def join(ctx):
    if ctx.author.voice:
        voiceChannel = ctx.author.voice.channel
    else:
        voiceChannel = discord.utils.get(ctx.guild.voice_channels)
        if not voiceChannel:
            await ctx.send('there are no voice channels dickhead')
            return None

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is None:
        voice = await voiceChannel.connect()
    elif not voice.is_connected() or voice.channel != voiceChannel:
        await voice.disconnect(force=True)
        voice = await voiceChannel.connect()

    return voice

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
        await ctx.send("\"shush\" - bao tan")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None and (voice.is_playing() or voice.is_paused()):
        voice.stop()
    else:
        await ctx.send("bao tan says stfu")

client.run(os.getenv('TOKEN'))
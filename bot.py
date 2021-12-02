import discord
import os
import asyncio
import random
from discord import FFmpegPCMAudio
from discord.ext import commands
from youtube_dl import YoutubeDL

# global vars
client = commands.Bot(command_prefix='bt ')
playlist = []

# basic events
@client.event
async def on_ready():
    print(f'{client.user} logged in')
    # disconnect from voice channels bot may have been left in
    for voice in client.voice_clients:
        await voice.connect()
        await voice.disconnect(force=True)

@client.event
async def on_disconnect():
    # leave voice channels/clients when leaving discord
    for voice in client.voice_clients:
        await voice.disconnect(force=True)

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
    
#     if message.content.startswith('cool'):
#         await message.channel.send('Cool beans')


### connection commands


@client.command()
async def join(ctx):
    """joins the active voice channel, or otherwise the first one
        # Returns:
        the voice client created by connecting to the voice channel
    """
    # get author's voice channel, otherwise first voice channel, to connect to
    if ctx.author.voice:
        voiceChannel = ctx.author.voice.channel
    else:
        voiceChannel = discord.utils.get(ctx.guild.voice_channels)
        if not voiceChannel:
            await ctx.send('there are no voice channels dickhead')
            return None

    # connect to the voice channel and return the associated voice client
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is None:
        voice = await voiceChannel.connect()
    elif not voice.is_connected() or voice.channel != voiceChannel:
        await voice.disconnect(force=True)
        voice = await voiceChannel.connect()

    return voice

@client.command()
async def leave(ctx):
    """leave the current voice channel if connected"""
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None and voice.is_connected():
        await voice.disconnect(force=True)
    else:
        ctx.send("tf you on about")


### music commands


@client.command()
async def play(ctx, url):
    """play the song at the given youtube url"""
    # join if not joined (unless impossible)
    voice = await join(ctx)
    if voice is None:
        await ctx.send("huh?")
        return

    # function parameters
    ydl_ops = {'format': 'bestaudio/best', 'noplaylist': 'True'}
    ffmpeg_ops = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 4294', 'options': '-vn'}
    positions = {1: 'st', 2: 'nd', 3: 'rd'}

    # play the song, or add to playlist if a song is already playing
    if voice.is_playing():
        pos = len(playlist) + 1
        playlist.append((ctx, url))
        await ctx.send(f"\"patience, your track is {pos}{positions.get(pos, 'th')} in the queue\" - Sun Tzu")
    else:
        with YoutubeDL(ydl_ops) as ydl:
            info = ydl.extract_info(url, download=False)
        newUrl = info['url']
        voice.play(FFmpegPCMAudio(newUrl, **ffmpeg_ops), after=playNext)

@client.command()
async def pause(ctx):
    """pause the current track"""
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None and voice.is_playing():
        voice.pause()
    else:
        await ctx.send("don't disrespect the bao tan")

@client.command()
async def resume(ctx):
    """resume the current track"""
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None and voice.is_paused():
        voice.resume()
    else:
        await ctx.send("\"shush\" - bao tan")

@client.command()
async def stop(ctx):
    """stops the music and queue altogether"""
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    playlist.clear()
    if voice is not None and (voice.is_playing() or voice.is_paused()):
        voice.stop()
    else:
        await ctx.send("bao tan says stfu")


### queue commands


def playNext(error):
    """plays the next song in the queue"""
    if len(playlist):
        ctx, url = playlist.pop(0)
        coro = play(ctx, url)
        fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
        try:
            fut.result()
        except Exception as e:
            print(e)

@client.command()
async def skip(ctx):
    """stops playing the current track and plays the next in the queue (if any)"""
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None and (voice.is_playing() or voice.is_paused()):
        # this is in a try/except because the voice doesn't stop fast enough without await
        try:
            await voice.stop()
        except TypeError:
            pass
        if len(playlist):
            newCtx, url = playlist.pop(0)
            await play(newCtx, url)
        
    else:
        await ctx.send("shut yo ass up and praise bao tan")

@client.command()
async def insert(ctx, url):
    """queues the track to play next"""
    playlist.insert(0, (ctx, url))
    await ctx.send("your track is playing next, you impatient bastard")

@client.command()
async def shuffle(ctx):
    """shuffles the order of the queue"""
    random.shuffle(playlist)
    await ctx.send("\"ah, I do love a bit of anarchy\" - bao tan")

# run the bot
client.run(os.getenv('TOKEN'))
import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} logged in')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('cool'):
        await message.channel.send('Cool beans')

client.run(os.getenv('TOKEN'))
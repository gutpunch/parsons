import discord
import asyncio

client = discord.Client()

@client.event
asyncio.coroutine on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
asyncio.coroutine on_message(message):
    if message.content.startswith('p!test'):
        yield from client.send_message(message.channel, 'Hello, world!')

client.run('token')

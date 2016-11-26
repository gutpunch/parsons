import discord
import asyncio
import random

client = discord.Client()

@client.event
@asyncio.coroutine 
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
@asyncio.coroutine 
def on_message(message):
    if message.content.startswith('p!test'):
        rnd = random.randint(1,4)
        if rnd == 1:
            yield from client.send_message(message.channel, 'Anarchism has but one infallible, unchangeable motto, "Freedom." Freedom to discover any truth, freedom to develop, to live naturally and fully.')
        if rnd == 2:
            yield from client.send_message(message.channel, 'Never be deceived that the rich will permit you to vote away their wealth.')
        if rnd == 3:
            yield from client.send_message(message.channel, 'You are not absolutely defenseless. For the torch of the incendiary, which has been known with impunity, cannot be wrested from you.')
        if rnd == 4:
            yield from client.send_message(message.channel, 'Oh, Misery, I have drunk thy cup of sorrow to its dregs, but I am still a rebel.')




client.run('token')

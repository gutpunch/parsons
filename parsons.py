#!/usr/bin/python3

import discord
import asyncio
import random
import sys
import json
import os

client = discord.Client()
recipients = []

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

    # Quotes from Lucy Parsons, selected randomly
    if message.content.startswith('p!quote'):
        rnd = random.randint(1,4)
        if rnd == 1:
            yield from client.send_message(message.channel, 'Anarchism has but one infallible, unchangeable motto, "Freedom." Freedom to discover any truth, freedom to develop, to live naturally and fully.')
        if rnd == 2:
            yield from client.send_message(message.channel, 'Never be deceived that the rich will permit you to vote away their wealth.')
        if rnd == 3:
            yield from client.send_message(message.channel, 'You are not absolutely defenseless. For the torch of the incendiary, which has been known with impunity, cannot be wrested from you.')
        if rnd == 4:
            yield from client.send_message(message.channel, 'Oh, Misery, I have drunk thy cup of sorrow to its dregs, but I am still a rebel.')

    # Vouch for IWW member to be marked trusted.
    elif message.content.startswith('p!vouch'):

        author = message.author # The member currently vouching
        recipient = message.mentions[0] # The member being vouched for

        # Can't vouch for self
        if author.name == recipient.name:
            yield from client.send_message(message.channel, 'You can\'t vouch for yourself, ya goof!')
            return

        # If the member is already in CNT they don't need to be vouched for
        for role in recipient.roles:
            if role.name == 'CNT':
                yield from client.send_message(message.channel, 'Member is already CNT!')
                return

        # Check recipients list
        recipient_dictionary = {'Name': '', 'Vouchers': []}

        if len(recipients) > 0:
            # do stuff
            for dictionary in recipients:
                if dictionary['Name'] == recipient.name:
                    recipient_dictionary = dictionary
        else:
            recipient_dictionary['Name'] = recipient.name 
            recipients.append(recipient_dictionary)

        # If the voucher is in CNT then we can do work
        for role in author.roles:
            if role.name == 'CNT':
                # Check that this member hasn't already vouched
                if author.name in recipient_dictionary['Vouchers']:
                    yield from client.send_message(message.channel, author.mention + ' has already vouched for ' + recipient.mention)
                    return
                else:
                    recipient_dictionary['Vouchers'].append(author.name)
                    yield from client.send_message(message.channel, author.mention + ' vouched for ' + recipient.mention)
                    if len(recipient_dictionary['Vouchers']) == 2:
                        # TODO: add CNT role to 'recipient' ; remove IWW role from 'recipient'
                        yield from client.add_roles(recipient, role)
                        yield from client.send_message(message.channel, recipient.mention + ' marked as trusted.')
                return

        # Otherwise the voucher is not in CNT and cannot vouch
        yield from client.send_message(message.channel, 'Sorry, only CNT can vouch for other members!') 


def main(db_file="database.json"):
    token = 'token'
    try:
        with open(db_file, 'r') as f:
            recipients = json.load(f)
    except json.decoder.JSONDecodeError:
        print("noot noot")

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(client.start(token))
    except KeyboardInterrupt:
        loop.run_until_complete(client.logout())    
        with open(db_file, 'w') as f:
            json.dump(recipients, f)
    finally:
        loop.close()


main()
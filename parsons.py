#!/usr/bin/python3

import discord
import toml
import asyncio
import json
import os
import random

client = discord.Client()
recipients = []

@client.event
@asyncio.coroutine
def on_ready():
	print("Logged in as")
	print(client.user.name)
	print(client.user.id)
	print("------")

@client.event
@asyncio.coroutine
def on_message(message):
	if message.content.startswith("p!vouch"):
		author = message.author
		recipient = message.mentions[0]
		can_vouch = False
		for role in author.roles:
			if role.name == "CNT" or role.name == "FAI":
				can_vouch = True
				break 
	if can_vouch == True:
		# can't vouch for self
		if author.name == recipient.name:
			yield from client.send_message(message.channel, "You can't vouch for yourself, ya goof!")
			return
	    
		# if the member is already in CNT they don't need to be vouched for
		for role in recipient.roles:
			if role.name == "CNT":
				yield from client.send_message(message.channel, recipient.mention + " is already CNT.")
				return
	
		# check recipients list
		recipient_dictionary = {"Name": "", "Vouchers": []}
		if len(recipients) > 0:
			for dictionary in recipients:
				if dictionary["Name"] == recipient.name:
					recipient_dictionary = dictionary
				else:
					recipient_dictionary["Name"] = recipient.name
					recipients.append(recipient_dictionary)
			if author.name in recipient_dictionary["Vouchers"]:
				yield from client.send_message(message.channel, author.mention + " has already vouched for " + recipient.mention)
				return
			else:
				recipient_dictionary["Vouchers"].append(author.name)
				yield from client.send_message(message.channel, author.mention + " vouched for " + recipient.mention)
			if len(recipient_dictionary["Vouchers"]) == 2:
				yield from client.add_roles(recipient, role)
				yield from client.send_message(message.channel, recipient.mention + " marked as trusted.")
				old_role = {}
				for role2 in recipient.roles:
					if role2.name == "IWW":
						old_role = role2
						yield from client.remove_roles(recipient, old_role)
						return
		else:
			yield from client.send_message(message.channel, "Sorry, only CNT/FAI can vouch for another member.")

def main(db_file="database.json"):
	global recipients
	conf = toml.load("conf.toml")
	try:
		with open(db_file, 'r') as f:
		    recipients = json.load(f)
	except (json.decoder.JSONDecodeError, FileNotFoundError):
		print("noot noot")

	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(client.start(conf['token']))
	except KeyboardInterrupt:
		loop.run_until_complete(client.logout())
		with open(db_file, 'w') as f:
			json.dump(recipients, f)
	finally:
		loop.close()

main()

#!/usr/bin/python3

import discord
import asyncio
import toml
import json
import os
import random

def get_role(name):
	for server in client.servers:
		for role in server.roles:
			if role.name == name:
				return role

client = discord.Client()
recipients = []

role_iww = {}
role_cnt = {}
role_fai = {}

@client.event
@asyncio.coroutine
def on_ready():
	print("Logged in as")
	print(client.user.name)
	print(client.user.id)
	print("------")
	
	global role_iww
	global role_cnt
	global role_fai
	role_iww = get_role("IWW")
	role_cnt = get_role("CNT")
	role_fai = get_role("FAI")

@client.event
@asyncio.coroutine
def on_message(message):
	global role_iww
	global role_cnt
	global role_fai

	if message.content.startswith("p!vouch "):
		if len(message.mentions) == 0:
			yield from client.send_message(message.channel, "Invalid syntax - command needs a user mention.")
			return

		author = message.author
		recipient = message.mentions[0]
		recipient_dictionary = {"Name": "", "Vouchers": [], "Veto": False}

		if len(recipients) > 0:
			for dictionary in recipients:
				if dictionary["Name"] == recipient.name:
					recipient_dictionary = dictionary
		else:
			recipient_dictionary["Name"] = recipient.name
			recipients.append(recipient_dictionary)

		if recipient_dictionary["Veto"] == False:
			if role_cnt in author.roles or role_fai in author.roles:
				if author.name == recipient.name:
					yield from client.send_message(message.channel, "You can't vouch for yourself, ya goof!")
					return	
				if role_cnt in recipient.roles:
					yield from client.send_message(message.channel, "User is already CNT.")
					return
				if role_fai in recipient.roles:
					yield from client.send_message(message.channel, "User is already FAI.")
					return
				
				if author.name in recipient_dictionary["Vouchers"]:
					yield from client.send_message(message.channel, author.mention + " has already vouched for " + recipient.mention)
					return
				else:
					recipient_dictionary["Vouchers"].append(author.name)
					yield from client.send_message(message.channel, author.mention + " vouched for " + recipient.mention)
					if len(recipient_dictionary["Vouchers"]) == 3:
						yield from client.add_roles(recipient, role_cnt)
						pin = yield from client.send_message(message.channel, recipient.mention + " has been marked as trusted and added to CNT.")
						yield from client.remove_roles(recipient, role_iww)
						yield from client.pin_message(pin)
					return
			else:
				yield from client.send_message(message.channel, "Sorry, only CNT/FAI can vouch for other users.")
				return
		else:
			yield from client.send_message(message.channel, recipient.mention + " has been vetoed from CNT approval and cannot claim vouchers.")		
	elif message.content.startswith("p!veto "):
		if len(message.mentions) == 0:
			yield from client.send_message(message.channel, "Invalid syntax - command needs a user mention.")
			return

		author = message.author
		recipient = message.mentions[0]
		recipient_dictionary = {"Name": "", "Vouchers": [], "Veto": False}

		if len(recipients) > 0:
			for dictionary in recipients:
				if dictionary["Name"] == recipient.name:
					recipient_dictionary = dictionary
		else:
			recipient_dictionary["Name"] = recipient.name
			recipients.append(recipient_dictionary)

		if role_fai in author.roles:
			if recipient_dictionary["Veto"] == False:
				recipient_dictionary["Veto"] = True
				yield from client.send_message(message.channel, recipient.mention + " has been vetoed from CNT approval.")	
				recipient_dictionary["Vouchers"].clear()
				if role_cnt in recipient.roles:
					yield from client.remove_roles(recipient, role_cnt)
					yield from client.add_roles(recipient, role_iww)
				return
			elif recipient_dictionary["Veto"] == True:
				recipient_dictionary["Veto"] = False
				yield from client.send_message(message.channel, recipient.mention + " has been allowed CNT approval.")
				return
		else:
			yield from client.send_message(message.channel, "Sorry, only FAI can veto users.")
			return
	elif message.content.startswith("p!tag "):
		print("noot noot")

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
		loop.run_until_complete(client.start(conf["token"]))
	except KeyboardInterrupt:
		loop.run_until_complete(client.logout())
		with open(db_file, 'w') as f:
			json.dump(recipients, f)
	finally:
		loop.close()

main()

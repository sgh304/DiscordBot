### 888b    888                     888   .d8888b.     888888b.   .d88888b.88888888888 ###
### 8888b   888                     888  d88P  Y88b    888  "88b d88P" "Y88b   888     ###
### 88888b  888                     888       .d88P    888  .88P 888     888   888     ###
### 888Y88b 888 .d88b. 888  888  888888888   8888"     8888888K. 888     888   888     ###
### 888 Y88b888d8P  Y8b888  888  888888       "Y8b.    888  "Y88b888     888   888     ###
### 888  Y8888888888888888  888  888888  888    888    888    888888     888   888     ###
### 888   Y8888Y8b.    Y88b 888 d88PY88b.Y88b  d88P    888   d88PY88b. .d88P   888     ###
### 888    Y888 "Y8888  "Y8888888P"  "Y888"Y8888P"     8888888P"  "Y88888P"    888     ###

###                   Newt3 BOT -- A simple Discord Chatbot for Newt3                  ###

### Authors:																		   ###
###							- Wes Smith												   ###
###							- Sam Holloway											   ###
###							- Aaron Simpson											   ###

import discord
from discord.ext import commands
import newt3_api
from random import randint

### BOT SETUP

client = discord.Client()
bot = commands.Bot(command_prefix = '?', description = 'Newt3 BOT')

### ON READY

@bot.event
async def on_ready():
	print('Logging is as {}'.format(bot.user.name))

### COMMANDS

@bot.command()
async def info(command = None):
##		Outputs some helpful info.
	if command:
		return #ADD A function to look at a specific function here
	output = (	'Hello, I am a bot! These are some things I can do:\n'
				'?items champion lane \n'
				'		-Gets the three most popular build paths for the specified champion and lane. \n'
				'?counters champion lane \n'
				'		-Gets the five champions with the highest winrate versus the specified champion and lane. \n'
				'?bans\n'
				'		-Gets the five champs with the highest win rates this patch. \n'
				'----------------------------------------------------------------- \n'
				'Example: ?items Jhin Bot \n'
				'Example: ?counters Gnar Top \n'
				'Example: ?bans')
	await bot.say(output)
	return output

@bot.command()
async def bans(role = None):
##		Outputs the top 5 win rate champions
	try:
		win_rates = newt3_api.get_champion_win_rates(number = 5)
		output = 'According to champion.gg, {}, {}, {}, {}, and {} are some good bans.'.format(win_rates[0].name, win_rates[1].name, win_rates[2].name, win_rates[3].name, win_rates[4].name)
	except newt3_api.NonExistantRoleException:
		output = '{} is not a valid role name. Please try again.'.format(role)
	finally:
		await bot.say(output)
		return output

@bot.command()
async def counters(name, role = None):
##		Takes in a champion name and role and outputs the top 5 counters for that champion
##		in that role. If no role is passed, the counters for champion's most popular role are
##		output.
	try:
		info = newt3_api.get_champion_info(name = name)
		matchups = newt3_api.get_champion_matchups(name = name, role = role, number = 5, info = info)
		if not role:
			role = newt3_api.get_champion_most_popular_role(name = name, info = info)
		output = 'According to champion.gg, {}, {}, {}, {}, and {} are some good counters for {} in {}.'.format(matchups[0].name, matchups[1].name, matchups[2].name, matchups[3].name, matchups[4].name, name, role)
	except newt3_api.NonExistantChampionException:
		output = '{} is not a valid champion name. Please try again.'.format(name)
	except newt3_api.NonExistantRoleException:
		output = '{} is not a valid role name. Please try again.'.format(role)
	except newt3_api.InvalidRoleException:
		output = '{} is not a role for {}. Please try again'.format(role, name)
	finally:
		await bot.say(output)
		return output

@bot.command()
async def items(name, role = None):
##		Takes in a champion name and role and outputs the top 3 builds for that champion
##		in that role. If no role is passed, the builds for champion's most popular role are
##		output.
	try:
		builds = newt3_api.get_champion_builds(name = name, role = role, number = 3)
		output = 	(
					'According to champion.gg, some good builds for {} are:\n'
					'	-{}\n'
					'	-{}\n'
					'	-{}\n'
					).format(name, builds[0].items, builds[1].items, builds[2].items)
	except newt3_api.NonExistantChampionException:
		output = '{} is not a valid champion name. Please try again.'.format(name)
	except newt3_api.NonExistantRoleException:
		output = '{} is not a valid role name. Please try again.'.format(role)
	except newt3_api.InvalidRoleException:
		output = '{} is not a role for {}. Please try again'.format(role, name)
	finally:
		await bot.say(output)
		return output

@bot.command()
async def picks(role = None):
##		Takes in a role and outputs the top 5 picks in that role based on win rate.
##		If no role is passed, it outputs the top 5 picks in general.
	try:
		win_rates = newt3_api.get_champion_win_rates(role = role, number = 5)
		role_output = ''
		if role:
			role_output = ' for {}'.format(newt3_api.get_proper_role(role))
		output = 'According to champion.gg, {}, {}, {}, {}, and {} are some good bans{}.'.format(win_rates[0].name, win_rates[1].name, win_rates[2].name, win_rates[3].name, win_rates[4].name, role_output)
	except newt3_api.NonExistantRoleException:
		output = '{} is not a valid role name. Please try again.'.format(role)
	finally:
		await bot.say(output)
		return output

### RUN NEWT3 BOT

bot.run("Mzk0MjcxMjIxNjc3Njg2Nzk0.DSxz6A.Rj5IaLDsiEPwMQ2nX1GW6XL7_ZY")

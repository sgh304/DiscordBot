### 888b    888                     888   .d8888b.           d88888888888b.8888888 ###
### 8888b   888                     888  d88P  Y88b         d88888888   Y88b 888   ###
### 88888b  888                     888       .d88P        d88P888888    888 888   ###
### 888Y88b 888 .d88b. 888  888  888888888   8888"        d88P 888888   d88P 888   ###
### 888 Y88b888d8P  Y8b888  888  888888       "Y8b.      d88P  8888888888P"  888   ###
### 888  Y8888888888888888  888  888888  888    888     d88P   888888        888   ###
### 888   Y8888Y8b.    Y88b 888 d88PY88b.Y88b  d88P    d8888888888888        888   ###
### 888    Y888 "Y8888  "Y8888888P"  "Y888"Y8888P"    d88P     888888      8888888 ### 

###           Newt3 API -- An API to support the Newt3 Discord Chatbot             ###

### Authors:                                                                       ###
###							- Wes Smith											   ###
###							- Sam Holloway										   ###
###							- Aaron Simpson										   ###

### Pulls League of Legends information from:                                      ###
###							- champion.gg                                          ###
###							- op.gg                                                ###

import collections
import json
import re
import requests

### GENERAL INFO

def get_champion_win_rates(role = None, number = None):
##		Takes in a role and number and returns the names and win rates of the champions in that role with
##		the top number win rates
	if role:
		role = get_proper_role(role)
	response = requests.get('http://champion.gg/statistics/#?sortBy=general.winPercent&order=descend')
	# Pull winrate table from the page
	raw_string = re.search('matchupData.stats = \[[\S\s]*?\]', response.text).group(0)
	string = raw_string.replace('matchupData.stats = ', '')
	raw_champion_list = json.loads(string)
	# Simplify list and return
	Champion = collections.namedtuple('Champion', ['name', 'win_rate'])
	champion_list = [Champion(champion['key'], champion['general']['winPercent']) for champion in raw_champion_list if not role or champion['role'] == role]
	champion_list.sort(key = lambda champion: champion.win_rate, reverse = True)
	if not number:
		number = len(champion_list)
	return champion_list[:number]

### SPECIFIC CHAMPION INFO

def get_champion_info(name):
##		The bread and butter of the champion info functions, takes a champion's name and returns
##		a dictionary containing a bunch of information on that champion or raises a ChampionException
##		if the name is invalid. The returned dictionary can be passed around to other functions to
##		prevent many repeated web requests.
	# Put name in proper form
	name = name[:1].upper() + name[1:].lower()
	# Request champion page from champion.gg
	response = requests.get('http://champion.gg/champion/{}'.format(name))
	# Make sure a champion page is acquired
	if response.status_code == 500:
		raise NonExistantChampionException
	# Get roles (in popularity order)
	roles_exp = re.compile('\/champion\/{}\/[A-Za-z]*'.format(name))
	raw_roles = roles_exp.findall(response.text)
	roles = [raw_role.replace('/champion/{}/'.format(name), '') for raw_role in raw_roles]
	# Iterate through roles to get role-specific info
	win_rates = {}
	win_rate_exp = re.compile('Win Rate\n      </a>\n     </td>\n     <td>\n      [0-9]*.[0-9]*%')
	matchups = {}
	matchups_exp = re.compile('"matchups":\[[\s\S]*?]')
	Matchup = collections.namedtuple('Matchup', ['name', 'win_rate', 'games'])
	for role in roles:
		# Get role page
		role_response = requests.get('http://champion.gg/champion/{}/{}'.format(name, role))
		# Get win rate
		raw_role_win_rate = win_rate_exp.search(role_response.text).group(0)
		role_win_rate = raw_role_win_rate.replace('Win Rate\n      </a>\n     </td>\n     <td>\n      ', '')
		win_rates[role] = role_win_rate
		#Get matchups
		raw_role_matchups = matchups_exp.search(role_response.text).group(0)
		role_matchups_string = raw_role_matchups.replace('"matchups":', '')
		role_cgg_matchups = json.loads(role_matchups_string)
		role_matchups = [Matchup(cgg_matchup['key'], 1 - cgg_matchup['winRate'], cgg_matchup['games']) for cgg_matchup in role_cgg_matchups]
		role_matchups.sort(key=lambda matchup: matchup.win_rate, reverse=True)
		matchups[role] = role_matchups
	#Return dictionary
	return 	{
				'Name': name,
				'Roles': roles,
				'Win Rate': win_rates,
				'Matchups': matchups
			}

def get_champion_roles(name = None, info = None):
##		Takes a champion name and returns a list of that champion's roles in order of popularity.
##		A pre-fetched info dictionary can also be passed in instead of a name to avoid repeated
##		web requests.
	if not info:
		info = get_champion_info(name = name)
	return info['Roles']

def get_champion_most_popular_role(name = None, info = None):
##		Takes a champion name and returns that champion's most popular role. A pre-fetched info
##		dictionary can also be passed in instead of a name to avoid repeated web requests.
	if not info:
		info = get_champion_info(name = name)
	return get_champion_roles(info = info)[0]

def get_champion_win_rate(name = None, role = None, info = None):
##		Takes a champion name and role and returns the champion's win rate for that role. If no role
##		is passed, the win rate of the champion's most popular role is output.
	if not info:
		info = get_champion_info(name = name)
	if role:
		role = get_proper_role(role)
	else:
		role = get_champion_most_popular_role(info = info)
	if role not in info['Roles']:
		raise InvalidRoleException
	return info['Win Rate'][role]

def get_champion_matchups(name = None, role = None, number = None, info = None):
##		Takes a champion name and role and number and returns the champion's worst number matchups in
##		that role. If no role is passed, the matchups of the champion's most popular role is output. If
##		no number is passed, all matchups are output.
	if not info:
		info = get_champion_info(name = name)
	if role:
		role = get_proper_role(role)
	else:
		role = get_champion_most_popular_role(info = info)
	total_matchups = len(info['Matchups'][role])
	if not number or number > total_matchups:
		number = total_matchups
	return info['Matchups'][role][:number]

### INPUT

def get_proper_role(role):
##		Takes an input role (usually a command parameter typed by a user) and checks it against some
##		common alternate names for League of Legends roles, outputting the role name expected
##		by champion.gg or raising RoleException if the input is invalid
	role = role.lower()
	role_dict = {
					'top': 'Top', 't': 'Top',
					'mid': 'Middle', 'middle': 'Middle', 'm': 'Middle',
					'bot': 'ADC', 'adc': 'ADC', 'adcarry': 'ADC', 'b': 'ADC', 'a': 'ADC',
					'support': 'Support', 'supporter': 'Support', 'shitter': 'Support', 's': 'Support',
					'jg': 'Jungle', 'jungle': 'Jungle', 'jungler': 'Jungle', 'j': 'Jungle',
				}
	if role not in role_dict:
		raise NonExistantRoleException
	return role_dict[role]

### EXCEPTIONS

class NonExistantChampionException(Exception):
##		Raised when information is requested for a champion that doesn't exist
	pass

class NonExistantRoleException(Exception):
##		Raised when information is requested for a role that doesn't exist
	pass

class InvalidRoleException(Exception):
##		Raised when information is requested for a role that a given champion is not played in
	pass
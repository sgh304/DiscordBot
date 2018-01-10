# Some tests to make sure Sam doesn't break anything else

import collections
import newt3_api
import re

def run_api_tests():
	# Note these don't always test for accuracy of returned info. It does when possible, but otherwise
	# the tests kind of just check that info is indeed returned 
	print('** Initializing Newt3 API tests')
	successes = 0
	failures = 0
	TestChampion = collections.namedtuple('TestChampion', ['name', 'most_popular_role'])
	test_champions =	[
						TestChampion('Malphite', 'Top'),
						TestChampion('Annie', 'Middle'),
						TestChampion('Vayne', 'ADC'),
						TestChampion('Taric', 'Support'),
						TestChampion('Nocturne', 'Jungle')
						]

	print('** General champion info')
	test_champion_infos = {}
	for test_champion in test_champions:
		print('Champion info for {}...	'.format(test_champion.name), end = '')
		try:
			test_champion_infos[test_champion] = newt3_api.get_champion_info(test_champion.name)
			print('SUCCESS!')
			successes += 1
		except newt3_api.NonExistantChampionException:
			print('Failed. Non existant champion.')
			failures += 1

	print('** Specific champion info without pre-fetched info')
	for test_champion in test_champions:
		api_most_popular_role = newt3_api.get_champion_most_popular_role(name = test_champion.name)
		print('{}\'s most popular role is {}...	'.format(test_champion.name, api_most_popular_role), end = '')
		if api_most_popular_role == test_champion.most_popular_role:
			print('SUCCESS!')
			successes += 1
		else:
			print('Failed.')
			failures += 1
		api_win_rate = newt3_api.get_champion_win_rate(name = test_champion.name)
		print('{}\'s win rate in {} is {}... '.format(test_champion.name, api_most_popular_role, api_win_rate), end = '')
		if re.fullmatch('[0-9][0-9].[0-9][0-9]%', api_win_rate):
			print('SUCCESS!')
			successes += 1
		else:
			print('Failed.')
			failures += 1

	print('** Specific champion info with pre-fetched info')
	for test_champion in test_champions:
		api_most_popular_role = newt3_api.get_champion_most_popular_role(info = test_champion_infos[test_champion])
		print('{}\'s most popular role is {}...	'.format(test_champion.name, api_most_popular_role), end = '')
		if api_most_popular_role == test_champion.most_popular_role:
			print('SUCCESS!')
			successes += 1
		else:
			print('Failed.')
			failures += 1
		api_win_rate = newt3_api.get_champion_win_rate(info = test_champion_infos[test_champion])
		print('{}\'s win rate in {} is {}... '.format(test_champion.name, api_most_popular_role, api_win_rate), end = '')
		if re.fullmatch('[0-9][0-9].[0-9][0-9]%', api_win_rate):
			print('SUCCESS!')
			successes += 1
		else:
			print('Failed.')
			failures += 1

	print('** Test some requests that may come from actual commands')
	for test_champion in test_champions:
		print('?counters {}...	'.format(test_champion.name), end = '')
		try:
			newt3_api.get_champion_matchups(name = test_champion.name, number = 5)
			print('SUCCESS!')
			successes += 1
		except:
			print('Failed.')
			failures += 1
	print('?bans...	', end = '')
	api_bans = newt3_api.get_champion_win_rates(number = 5)
	print(api_bans)
	if len(api_bans) == 5:
		print('SUCCESS!')
		successes += 1
	else:
		print('Failed.')
		failures += 1

	print('** Tests complete.')
	print('** Successes: {} ({:.2f}%)'.format(successes, (successes / (successes + failures) * 100)))
	print('** Failures: {} ({:.2f}%)'.format(failures, (failures / (successes + failures) * 100)))

def run_bot_tests():
	# Not sure how to do these. Note that the bot's commands return their output as well
	# as send them to the actual bot, so maybe this could be leveraged somehow.
	pass

run_api_tests()
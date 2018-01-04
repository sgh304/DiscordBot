import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import urllib
import urllib.request
import re
import json
from random import randint

client = discord.Client()

description = "Bot for Newt3 Discord Server"
bot = commands.Bot(command_prefix = '?', description = description)

@bot.event
async def on_ready():
    print("logging in")
    print(bot.user.name)
    print("")

##Get Reccommended Items for Champion
@bot.command()
async def items(champion, lane=None):
    #Check if valid champion
    if not await get_champion_info(champion, message=True):
        return
    #Get most popular lane if needed
    if not lane:
        lane = await get_most_popular_lane(champion, message=True)
    htmldoc = urllib.request.urlopen("http://na.op.gg/champion/" + champion + "/statistics/" + lane + "/item").read()
    soup = BeautifulSoup(htmldoc)
    ##Get item names
    name_divs = soup.findAll("ul", {"class" : "champion-stats__list"})
    items = re.findall(r"bc'&gt;(.*?)&lt;", str(name_divs))
    ##Get Win Rates
    win_rate_divs = soup.findAll('td', {"class" :"champion-stats__table__cell--winrate"})
    win_rates = []

    for i in win_rate_divs:
        win_rates.append(str(i)[-11:-5])

    for i in range(0,8,3):
        await bot.say("Build {}: {} > {} ? {} | Win Rate: {}".format(i//3 + 1, items[i], items[i+1], items[i+2], win_rates[i//3] ))


@bot.command()
async def bans():
    #Get winrate page from champion.gg
    htmldoc = urllib.request.urlopen('http://champion.gg/statistics/#?sortBy=general.winPercent&order=descend').read()
    soup = BeautifulSoup(htmldoc)
    data = str(soup.find_all('script')[18])

    #Pull winrate table from the page
    exp = re.compile('\[[A-Za-z0-9:.,"\}\{ -_]*\]')
    match = exp.search(data)
    champ_string = match.string[match.start():match.end()]
    champ_dict = json.loads(champ_string)

    #Construct simpler list (dictionaries containing name, winrate)
    champ_list = []
    for champ in champ_dict:
        name = champ['key']
        winrate = champ['general']['winPercent']
        champ_list.append({'name': name, 'winrate': winrate})
    champ_list.sort(key=lambda champ: champ['winrate'], reverse=True)

    #Output the top 5 -- wow those are some good bans!
    output = 'According to champion.gg, some good bans are: {}, {}, {}, {}, and {}.'.format(champ_list[0]['name'], champ_list[1]['name'], champ_list[2]['name'], champ_list[3]['name'], champ_list[4]['name'])
    meme_output = 'According to the Grand Carnivalist, some good bans are: RIVEN, RIVEN, RIVEN, RIVEN, and RIVEN!'
    if randint(0,100) == 44:
        await bot.say(meme_output)
    else:
        await bot.say(output)

##Get the top 5 counters for a given champion
@bot.command()
async def counters(champion, lane=None):
    #Check if valid champion
    if not await get_champion_info(champion, message=True):
        return
    #Get most popular lane if needed
    if not lane:
        lane = await get_most_popular_lane(champion, message=True)
    htmldoc = urllib.request.urlopen("http://na.op.gg/champion/" + champion + "/statistics/" + lane + "/matchups").read()
    soup = BeautifulSoup(htmldoc)

    ##Get champion names
    name_divs = soup.find_all("div", {"class" : "champion-matchup-list__champion"})
    counters = re.findall(r"<span>(.*?)</span>", str(name_divs))
    win_rates = re.findall(r"([0123456789\.]{1,5})(?=%)", str(name_divs))

    ##Sort win_rates then take 1 - win_rates
    win_rates, counters = zip(*sorted(zip(win_rates, counters)))
    win_rates = [100 - float(x) for x in win_rates]

    # Display top five counters and their win rates
    for i in range(0,5):
        await bot.say("{} | Win Rate: {}%".format(counters[i], win_rates[i]))

#Returns a dictionary with some info about a given champion, or returns false and prints a message if the champion requested is invalid.
#This should help with further command development.
async def get_champion_info(champion, message=False):
    #Get champion's name in proper form
    champion_name = champion[:1].upper() + champion[1:].lower()
    #Get champion info page
    try:
        champion_response = urllib.request.urlopen('http://champion.gg/champion/{}'.format(champion_name))
        champion_response_text = str(champion_response.read())
    except:
        #Print a message and return false if champion is invalid
        if message:
            await bot.say('{} is not a valid champion name. Typo?'.format(champion))
        return False
    #Get lanes (in popularity order)
    lanes_exp = re.compile('\/champion\/{}\/[A-Za-z]*'.format(champion_name))
    raw_lanes_strings = lanes_exp.findall(champion_response_text)
    lanes = [raw_lane_string.replace('/champion/{}/'.format(champion_name), '') for raw_lane_string in raw_lanes_strings]
    #Get win rate
    win_rate_exp = re.compile('Win Rate\\\\n      <\/a>\\\\n     <\/td>\\\\n     <td>\\\\n      [0-9]*.[0-9]*%')
    raw_win_rate_string = win_rate_exp.search(champion_response_text).group(0)
    win_rate = raw_win_rate_string.replace('Win Rate\\n      </a>\\n     </td>\\n     <td>\\n      ', '')
    #Return dictionary
    return {
        'Name': champion_name,
        'Lanes': lanes,
        'Win Rate': win_rate
    }

async def get_most_popular_lane(champion, message=False):
    champion_dict = await get_champion_info(champion)
    champion_name = champ_dict['Name']
    lane = champ_dict['Lanes'][0]
    if message:
        bot.say('No lane selected. Defaulting to {}\'s most popular lane, {}. ' \
            'If you want another lane, try something like this: "?items {} {}"'.format(champion_name, lane, champion_name, lane))
    return lane

bot.run("Mzk0MjcxMjIxNjc3Njg2Nzk0.DSxz6A.Rj5IaLDsiEPwMQ2nX1GW6XL7_ZY")

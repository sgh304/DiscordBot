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
async def items(champion, lane = None):
    if lane is None:
        await bot.say("Please choose a lane! Try something like this: \"?items Jhin bot\"")
    else:
        htmldoc = urllib.request.urlopen("http://na.op.gg/champion/" + champion + "/statistics/" + lane + "/item").read()
        soup = BeautifulSoup(htmldoc)
        ##Get item names
        name_divs = soup.findAll("ul", {"class" : "champion-stats__list"})
        items = re.findall(r"bc'&gt;(.*?)&lt;", str(name_divs))
        print(items)

        ##Get Win Rates
        win_rate_divs = soup.findAll('td', {"class" :"champion-stats__table__cell--winrate"})
        win_rates = []
        for i in win_rate_divs:
            win_rates.append(str(i)[-11:-5])
        await bot.say("The top three %s %s builds are: (op.gg)" % (champion, lane))
        message1 = "Build 1: " + items[0] + " > " + items[1] + " > " + items[2] + " | Win Rate: " + win_rates[0]
        message2 = "Build 2: " + items[3] + " > " + items[4] + " > " + items[5] + " | Win Rate: " + win_rates[1]
        message3 = "Build 3: " + items[6] + " > " + items[7] + " > " + items[8] + " | Win Rate: " + win_rates[2]
        await bot.say(message1)
        await bot.say(message2)
        await bot.say(message3)

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

    #Construct simpler list (tuples in form (name, winrate))
    champ_list = []
    for champ in champ_dict:
        name = champ['key']
        winrate = champ['general']['winPercent']
        champ_list.append((name, winrate))
    champ_list.sort(key=lambda champ: champ[1], reverse=True)

    #Get the top 5 -- wow those are some good bans!!!
    bans = champ_list[:5]
    output = 'According to champion.gg, some good bans are: '
    for index in range(4):
        output += bans[index][0] + ', '
    output += 'and ' + bans[4][0] + '.'

    #But of course we ban Riven instead!!!!
    meme_output = 'According to the Grand Carnivalist, some good bans are: RIVEN, RIVEN, RIVEN, RIVEN, and RIVEN!'
    #print(output)
    #Output

    if randint(0,50) == 25:
        await bot.say(meme_output)
    else:
        await bot.say(output)

##Get the top 5 counters for a given champion
@bot.command()
async def counters(champion):
    htmldoc = urllib.request.urlopen("http://na.op.gg/champion/" + champion + "/statistics/top/matchup").read()
    soup = BeautifulSoup(htmldoc)

    ##Get champion names
    name_divs = soup.findAll("ul", {"class" : "champion-matchup-champion-list"})
    counters = re.findall(r"bc'&gt;(.*?)&lt;", str(name_divs))
    start = "&gt;"
    end = "&lt;"
    print(counters)

    ##Get win rates
    win_rate_divs = soup.findAll('td', {"class" :"champion-matchup-champion-list__winrate"})
    win_rates = []
    for i in win_rate_divs:
        win_rates.append(str(i)[-11:-5])
    print(win_rates)
    
    # Display top five counters and their win rates
    await bot.say("The top five %s counters are: (op.gg)" % champion)
    message1 = "Best Counter: " + counters[0] + " | Win Rate: " + win_rates[0]
    message2 = "Second: " + counters[1] + " | Win Rate: " + win_rates[1]
    message3 = "Third: " + counters[2] + " | Win Rate: " + win_rates[2]
    message4 = "Fourth: " + counters[3] + " | Win Rate: " + win_rates[3]
    message5 = "Fifth: " + counters[4] + " | Win Rate: " + win_rates[4]
    
    await bot.say(message1)
    await bot.say(message2)
    await bot.say(message3)
    await bot.say(message4)
    await bot.say(message5)
    
bot.run("Mzk0MjcxMjIxNjc3Njg2Nzk0.DSxz6A.Rj5IaLDsiEPwMQ2nX1GW6XL7_ZY")

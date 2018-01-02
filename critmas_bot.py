import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import urllib
import urllib.request
import re

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
async def items(champion):
    htmldoc = urllib.request.urlopen("http://na.op.gg/champion/" + champion + "/statistics/top/item").read()
    soup = BeautifulSoup(htmldoc)

    ##Get item names
    name_divs = soup.findAll("ul", {"class" : "champion-stats__list"})
    items = re.findall(r"bc'&gt;(.*?)&lt;", str(name_divs))
    start = "&gt;"
    end = "&lt;"
    print(items)

    ##Get Win Rates
    win_rate_divs = soup.findAll('td', {"class" :"champion-stats__table__cell--winrate"})
    win_rates = []
    for i in win_rate_divs:
        win_rates.append(str(i)[-11:-5])
    print(win_rates)
    await bot.say("The top three %s builds are: (op.gg)" % champion)
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
    output = 'According to the Grand Carnivalist, some good bans are: RIVEN, RIVEN, RIVEN, RIVEN, and RIVEN!'

    #Output
    await bot.say(output)

bot.run("Mzk0MjcxMjIxNjc3Njg2Nzk0.DSxz6A.Rj5IaLDsiEPwMQ2nX1GW6XL7_ZY")

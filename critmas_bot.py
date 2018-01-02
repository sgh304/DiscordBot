import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import urllib
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

bot.run("Mzk0MjcxMjIxNjc3Njg2Nzk0.DSxz6A.Rj5IaLDsiEPwMQ2nX1GW6XL7_ZY")

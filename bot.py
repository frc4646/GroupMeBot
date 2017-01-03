import groupy
from groupy import Bot
import time
from bs4 import BeautifulSoup
import re
import urllib
import http
import json
import hashlib
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

ADMIN_NAME_HASH = config['DEFAULT']['AdminNameHash'] #MD5 hash of the bot admin's name, they have the power to !kill
TBA_APP_ID = config['DEFAULT']['TBAAppID']
GROUP_NAME = config['DEFAULT']['GroupName']

bot = Bot.list().first
groups = groupy.Group.list()
for i in groups:
    if i.name == GROUP_NAME:
        group=i
oldMsg = ""

def andymark_item(partnumber):
    url = 'http://www.andymark.com/product-p/am-'+str(partnumber)+'.htm'
    r = urllib.request.urlopen(url).read() #TODO: Change this to use http.client so we don't have 2 libraries doing the same thing
    try:
        soup = BeautifulSoup(r, "lxml")
    except:
        soup = BeautifulSoup(r, "html.parser")
    price = soup.find_all("span", itemprop="price")
    if soup.title.get_text()=="AndyMark Robot Parts Kits Mecanum Omni Wheels":
        return(None) #404 checking
    else:
        name = re.sub(r'\([^)]*\)', '', soup.title.get_text())
        #print(price[0].text)
        #money = price[0].text.encode('utf8','ignore')
        money = price[0].get_text()
        return([url, name, money])
        #print(re.sub(r'\([^)]*\)', '', soup.title.get_text())) #kill the parenthesis
        #print(float(price[0].get_text()))

def vex_item(partnumber):
    url = 'http://www.vexrobotics.com/'+str(partnumber)+'.html'
    r = urllib.request.urlopen(url).read() #TODO: Change this to use http.client so we don't have 2 libraries doing the same thing
    try:
        soup = BeautifulSoup(r, "lxml")
    except:
        soup = BeautifulSoup(r, "html.parser")
    price = soup.find_all("span", class_="price")
    if soup.title.get_text()=="404: Page Not Found  - VEX Robotics":
        return(None) #404 checking
    else:
        name = re.sub(r'\([^)]*\)', '', soup.title.get_text())
        money = price[0].get_text()
        return([url, name, money])

def tbaGetName(team):
    try:
        url = "/api/v2/team/frc"+str(team)+"?X-TBA-App-Id="+TBA_APP_ID
        print(url)
        c = http.client.HTTPSConnection("www.thebluealliance.com")
        c.request("GET", url)
        response = c.getresponse()
        teamData = response.read().decode("utf-8")
        #print(teamData)
        data = json.loads(teamData)
        return data['nickname']
    except:
        return(None)

def reminder():
    #TODO: AUTOMATE THIS
    print("this thing doesn't even work yet, why are you calling it")

while True:
    latestMsg = group.messages().newest
    if latestMsg != oldMsg:
        #print(latestMsg)
        if latestMsg.text == "Hi bot!":
            bot.post("Hi, "+latestMsg.name)
        else:
            cmdname = latestMsg.text.split(" ")[0]
            if cmdname == "!amlookup":
                productNo = latestMsg.text.split(" ")[1]
                part = andymark_item(productNo)
                if part:
                    #print(part)
                    bot.post("The item you looked up is a "+part[1]+". It costs "+part[2]+".")
                else:
                    bot.post("Item not found.")
            elif cmdname == "!nextmeeting":
                if int(time.strftime("%W")) <= 12:
                    if int(time.strftime("%W")) = 1:
                        bot.post("Kickoff is Saturday! G E T H Y P E")
                        bot.post("Also be sure to download the encrypted manual when it comes out!")
                    else if int(time.strftime("%w")) == 0:
                        bot.post("The next meeting is held Monday at 6:30 PM!")
                    else if int(time.strftime("%w")) <= 5:
                        bot.post("The next meeting will be held TODAY and every weekday at 6:30 PM!")
                    else if int(time.strftime("%w")) == 6:
                        bot.post("The next meeting will be held TODAY and every Saturday at 12:00 PM!")
                else:
                    if int(time.strftime("%w")) <= 1:
                        bot.post("The next meeting will be on Monday at 6:30 PM!")
                    else:
                        bot.post("The next meeting will be on Saturday at 12 PM!")
                #TODO: combine this with a google calendar for cases such as the FTC events and build season
            elif cmdname == "!zesty": #DO NOT DOCUMENT THIS COMMAND EVER
                bot.post("ayy lmao")
            elif cmdname == "!about" or cmdname == "!?" or cmdname == "!help":
                bot.post("For more information, visit https://github.com/frc4646/GroupMeBot")
            elif cmdname == "!tba":
                teamNo = latestMsg.text.split(" ")[1]
                teamName = tbaGetName(teamNo)
                if teamNo == "8":
                    bot.post("TBA Link to team #8, The 8th team, Team \"The Ocho\" 8: https://thebluealliance.com/team/8")
                    bot.post("Wait, when did they change their name?")
                elif teamName:
                    bot.post("TBA Link to team "+teamNo+", "+teamName+": https://thebluealliance.com/team/"+teamNo)
                else:
                    bot.post("TBA Link to team: https://thebluealliance.com/team/"+teamNo)
            elif cmdname == "!kill":
                m = hashlib.md5(latestMsg.name.encode("utf-8","ignore")).hexdigest()
                print(m)
                if m == ADMIN_NAME_HASH:
                    bot.post("Shutting down")
                    exit()
                else:
                    bot.post("You're not an admin.")
            elif cmdname == "!manual" or cmdname == "!rtfm" or cmdname == "!thegame":
                bot.post("Manual is here: http://www.firstinspires.org/resource-library/frc/competition-manual-qa-system")
            elif cmdname == "!vexlookup": #
                productNo = latestMsg.text.split(" ")[1]
                part = vex_item(productNo)
                if part:
                    #print(part)
                    bot.post("The item you looked up is a "+part[1].split(" - ")[0]+". It costs "+part[2]+".")
                else:
                    bot.post("Item not found.")
        oldMsg = latestMsg
    time.sleep(2)

import groupy
from groupy import Bot
import time
from bs4 import BeautifulSoup
import re
import urllib
import http
import json

bot = Bot.list().first
groups = groupy.Group.list()
for i in groups:
	if i.name == "TrunkBot Test":
		group=i
oldMsg = ""

def andymark_item(partnumber):
	url = 'http://www.andymark.com/product-p/am-'+str(partnumber)+'.htm'
	r = urllib.request.urlopen(url).read() #TODO: Change this to use http.client so we don't have 2 libraries doing the same thing
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

def tbaGetName(team):
	# try:
	url = "/api/v2/team/frc"+str(team)+"?X-TBA-App-Id=frc4646:GroupMeBot:v01"
	print(url)
	c = http.client.HTTPSConnection("www.thebluealliance.com")
	c.request("GET", url)
	response = c.getresponse()
	print(response.read())
	teamData=response.read().decode("utf-8")
	print(teamData)
	data = json.loads(teamData)
	return data['nickname']
	# except:
	# return(None)

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
					print(part)
					bot.post("The item you looked up is a "+part[1]+". It costs "+part[2]+".")
				else:
					bot.post("Item not found.")
			elif cmdname == "!nextmeeting":
				if int(time.strftime("%m")) <= 3:
					bot.post("Meetindgs are held at 6:30 PM every weekday and at 9:00 AM on Saturdays!")
				else:
					bot.post("Meetings are held at 6:30 PM on Mondays and at 12:00 PM on Saturdays!")
				#TODO: combine this with a google calendar for cases such as the FTC events and build season
			elif cmdname == "!zesty": #DO NOT DOCUMENT THIS COMMAND EVER
				bot.post("ayy lmao")
			elif cmdname == "!about" or cmdname == "!?" or cmdname == "!help":
				bot.post("For more information, visit https://github.com/frc4646/GroupMeBot")
			elif cmdname == "!tba":
				teamNo = latestMsg.text.split(" ")[1]
				teamName = tbaGetName(teamNo)
				if teamName:
					bot.post("TBA Link to team "+teamNo+", "+teamName+": https://thebluealliance.com/team/"+teamNo)
				else:
					bot.post("TBA Link to team: https://thebluealliance.com/team/"+teamNo)
				#TODO: let's make it look up the team name through the API AND WORK
		oldMsg = latestMsg
	time.sleep(2)

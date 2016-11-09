import groupy
from groupy import Bot
import time
from bs4 import BeautifulSoup
import re
import urllib

bot = Bot.list().first
groups = groupy.Group.list()
for i in groups:
	if i.name == "TrunkBot Test":
		group=i
oldMsg = ""

def andymark_item(partnumber):
	url = 'http://www.andymark.com/product-p/am-'+str(partnumber)+'.htm'
	r = urllib.request.urlopen(url).read()
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

while True:
	latestMsg = group.messages().newest
	if latestMsg != oldMsg:
		print(latestMsg)
		if latestMsg.text == "Hi bot!":
			bot.post("Hi, "+latestMsg.name)
		else:
			if latestMsg.text.split(" ")[0] == "amlookup":
				productNo = latestMsg.text.split(" ")[1]
				part = andymark_item(productNo)
				if part:
					print(part)
					bot.post("The item you looked up is a "+part[1]+". It costs "+part[2]+".")
				else:
					bot.post("Item not found.")
		oldMsg = latestMsg
	time.sleep(2)

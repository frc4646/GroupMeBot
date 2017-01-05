from bs4 import BeautifulSoup
import re
import urllib
import http
import json

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

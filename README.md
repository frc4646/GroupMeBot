#Team ASAP GroupMe bot

Bot to remind members of meetings and perform various commands. Will probably run on a Raspberry Pi in a closet at our build space.

Uses:
* GroupyAPI
* BeautifulSoup  

You can also install the lxml parser with `apt-get install python-lxml` if you want, but the program will use just Python's built in HTML parser if you don't have it

I have added a requirements.txt so you can just cd to this repo, then run `pip install -r requirements.txt`

Before you run this bot, please change the config file options to change the TBA app ID to reflect your team number and set the MD5 hash of your name to be able to issue admin commands.

Current Commands:
* !amlookup [part #]: Lookup a part on AndyMark
* !nextmeeting: Find out when the next meeting is (WIP)
* !about: Links back here
* !tba: looks up teams from thebluealliance.com
* !kill: Kill the bot (admin only)
* Hi Bot!: Say hello to the Bot

#Team ASAP GroupMe bot

Bot to remind members of meetings and perform various commands. Will probably run on a Raspberry Pi in a closet at our build space.

Uses:
* GroupyAPI
* BeautifulSoup  
You can also install the lxml parser with `apt-get install python-lxml` if you want, but the program will use just Python's built in HTML parser if you don't have it

I have added a requirements.txt so you can just cd to this repo, then run `pip install -r requirements.txt`

Current Commands:
* !amlookup [part #]: Lookup a part on AndyMark
* !nextmeeting: Find out when the next meeting is (WIP)
* !about: Links back here
* !tba: looks up teams from thebluealliance.com
* Hi Bot!: Say hello to the Bot

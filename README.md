# Bee-Storm-bot

Discord.py Bot specifically made for Annus Team (or: Bee Storm) Discord server. Although the source code is open-source, in case you wanna run this bot on your server, you will need to make some changes, because of some 'hardcoded' server-specific things (in future updates - refactor, it may not be that bad):
- IDs (roles, owner's, channels, etc.)
- TOKEN (bot token required for running)
- multiple-server issues (made for running on one server, multiple server run is untested, probably won't work and if so, will do real mess)
- language (made for Czech server, so he speaks Czech)
- commands (for example command '$svatky' applies only for Czech calendar, Czech Republic)

# Functions

- compatible only with Annus Team Discord server (can be running on 1 server only)
- simple JSON Database for storing stats
- counting the number of predefined role mentions, bot mentions with commands showing stats, leaderboard
- reacting to predefined messages, bot mention
- simple commands (hello, time, repeat)
- name day command (Who has Name day today/at specific day?)
- birthday command (members store their birthdays and bot reminds/congrats that day)
- reminder command (reminds something at specific date/time to member)
- random fact every predefined hours at predefined time (300+ random facts)
- daily message at noon (date, who has nameday or specific messages on Christmas, New Year's Eve)
- new Year message
- non-aggresive censure
- admin commands

# Database

Using simple 'db.json' file and JSON format <=> python dict. 
- if the file content is entirely lost, bot can auto-restore the stats (slow process, server-specific feature)
- storing predefined role mentions, birthdays, reminders and bot data
- corrupt database file will be sent in message and if not interrupted or stopped, bot will perform auto-recovery

# Log and crash recovery

Bot is recording it's activites and storing them into logfile.
- if bot is currently restoring database, logging into file is disabled (log remains just in console)
- every time bot runs, bot run stat will be incremented
- in case of some crash, bot may try to reboot itself up to 3 times
- possibility of server message logging and internal logging
- replit hosting related: after exception in runtime (temporary ban), bot will try to reboot (kill & start again) multiple times

# Fly.io hosting

- Deploy (run or update): `flyctl deploy`
- Double messages fix (after deploy): `fly scale count 1`

# TODO list

Bot is currently still under development, but should work just fine. Currently there may be some things to be done in the future, but all of them are not core and required things to run the bot, as the bot in the present state works correctly and as expected. If something should be done, it will be listed in issues.


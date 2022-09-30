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

# Database

Using simple 'db.json' file and JSON format <=> python dict. 
- if the file content is entirely lost, bot can auto-restore the stats (slow process, server-specific feature)
- storing predefined role mentions, birthdays, reminders and bot runs

# Log and crash recovery

Bot is recording it's activites and storing them into logfile.
- if bot is currently restoring database, logging is disabled
- every time bot runs, bot run stat will be incremented
- in case of some crash, bot may try to reboot itself up to 3 times

# TODO list

Bot is currently still under development, but should work just fine. Currently there aren't much things to be done in the future:
- heavy code refactor (variables, czenglish code, repeated code blocks, hardcoded things/features, effectivity, ...)
- reboot command
- git command (url to this github)
- admin specific commands (so everything is not so dependend on editing source code)

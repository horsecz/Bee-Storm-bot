# Bee-Storm-bot

Discord.py Bot specifically made for Annus Team (or: Bee Storm) Discord server. Although the source code is open-source, in case you wanna run this bot on your server, you will need to make some changes, because of some 'hardcoded' server-specific things (in future updates - refactor, it may not be that bad):
- IDs (roles, owner's, channels, etc.)
- multiple-server issues (made for running on one server, multiple server run is untested, probably won't work and if so, will do real mess)
- language (made for Czech server, so he speaks Czech)
- commands (for example command '$svatky' applies only for Czech calendar, Czech Republic)

## Discontinued

**Development is discontinued.** No one cares about this bot and I don't wanna do this anymore.

## Start
Start with python (and modules discord, pytz) installed:
`python app.py`

# Online at 'Fly.io' hosting

- Deploy (run or update): `flyctl deploy`
    - performed automatically on github push
- Double messages fix (after deploy): `fly scale count 1`

# Functions

- compatible only with Annus Team Discord server (can be running on 1 server only)
- simple JSON Database for storing stats
- counting the number of predefined role mentions, bot mentions with commands showing stats, leaderboard
- reacting to predefined messages, bot mention
- simple commands (hello, time, repeat)
- name day command (Who has Name day today/at specific day?)
- daily message at noon (date, who has nameday or specific messages on Christmas, New Year's Eve)
- non-aggresive censure
- admin commands

## Database

Using simple 'db.json' file and JSON format <=> python dict. 
- if the file content is entirely lost, bot can auto-restore the stats (slow process, server-specific feature)
- storing predefined role mentions, reminders and bot data
- corrupt database file will be sent in message and bot will perform auto-recovery of some data

## Logs

Bot is recording it's activites and storing them into logfile.
- if bot is currently restoring database, logging into file is disabled (log remains just in console)
- possibility of server messages logging and internal logging

# To be done
Some things need to be completed or updated:
- Help message
- Admin commands message
- Source code related: remove unused global variables, code logic refactor, comments, etc. => refactor part 2

New (upcoming) features:
- Dead room revival

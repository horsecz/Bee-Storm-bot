# ---------- #
# ----------
#   DATABASE.PY
# ----------   
#   Database and its operations
# ---------- #

from os.path import exists
import json
import discord
import globals
import logs
import srani
import utility

# Recover stats about tags in channel
async def recovery(tag_channel):
    globals.DB_RECOVERY_RUNNING = True
    await utility.change_bot_activity(discord.Status.idle, "Recovering database stats!")
    globals.srani_list = []
    update(True)
    msg_cnt = 0
    total_poops = 0
    progress_msg_cnt_trshld = 10000

    async for msg in tag_channel.history(limit=None):
        try:
            msg_cnt = msg_cnt + 1
            await srani.add_if_tag_in_message(msg, msg.author.id)
            if srani.is_any_tag_in_message(msg.content):
                total_poops = total_poops + 1

            # Progress report
            if (msg_cnt % progress_msg_cnt_trshld == 0):
                logs.info('Recovery: analyzed ' + str(msg_cnt/1000) + 'k messages', 'Database recovery')
                await utility.change_bot_activity(discord.Status.idle, "Restoring database. (" + str(msg_cnt/1000) + "k messages anaylzed)")
        except Exception as e:
            logs.exception(e, 'Database recovery')
            logs.exception('STATE:' +
                      '\n Message number: ' + str(msg_cnt) + 
                      "\n Author: " +
                      str(msg.author.id) + "\n Content: " + str(msg.content) + 
                      "\n Date: " +
                      str(msg.created_at.date) + "\n URL: " +
                      str(msg.jump_url), 'Database recovery')

    logs.info('Recovery: Completed. Analyzed ' + str(msg_cnt) + ' messages and found ' + str(total_poops) + ' poop tags', 'Database recovery')
    globals.DB_RECOVERY_RUNNING = False
    await utility.change_bot_activity(discord.Status.online, "Ready! Try '$help' for commands list.")
    update(True)


# Refresh server members in database
# If no_log is specified, this action won't be logged
async def member_refresh(no_log=None):
    for guild in globals.bot.guilds:
        for serverMember in guild.members:
            found = False
            for member in globals.srani_list:
                if serverMember.id == member["id"]:
                    found = True
                    break

            if not found:
                if no_log == False or no_log == None:
                    logs.info('Server member ' + str(serverMember) + ' added to database', 'Database')
                await srani.new_member(serverMember.id)

# Load database into list(s)
async def load():
    # If database file not found, create the file
    if exists(globals.db_file_path) == False:
        f = open(globals.db_file_path, 'w')
        f.close()

    # Load database
    with open(globals.db_file_path, 'r') as openfile:
        try:
            globals.json_obj = json.load(openfile)
        except Exception as e:
            # As for now, the hosting Fly.io causes that every code change (push from GitHub) removes entire database file.
            # Due to this, exception will not be logged as it will happen every push/code update.
            #logs.exception(e, 'Database')

            # Corrupt database -> create needed keys
            globals.json_obj = {}
            globals.DB_UPDATE_DISABLED = True
            globals.DB_EMPTY = True
            with open(globals.db_file_path, 'w') as openfile: # "Root" key
                json.dump(globals.json_obj, openfile, indent=1) 

        if not "srani" in globals.json_obj.keys():
            globals.json_obj["srani"] = []
            with open(globals.db_file_path, 'w') as openfile:
                json.dump(globals.json_obj, openfile, indent=1)
        if not "birthday" in globals.json_obj.keys():
            globals.json_obj["birthday"] = []
            with open(globals.db_file_path, 'w') as openfile:
                json.dump(globals.json_obj, openfile, indent=1)
        if not "bot_data" in globals.json_obj.keys():
            globals.json_obj["bot_data"] = {
                "bot_runs": 0,
                "welcome_msg": False,
                "random_messages": False,
                "total_poops": 0
            }
            with open(globals.db_file_path, 'w') as openfile:
                json.dump(globals.json_obj, openfile, indent=1)
        if not "reminders" in globals.json_obj.keys():
            globals.json_obj["reminders"] = []
            with open(globals.db_file_path, 'w') as openfile:
                json.dump(globals.json_obj, openfile, indent=1)
        
        globals.DB_UPDATE_DISABLED = False
        globals.srani_list = globals.json_obj["srani"]
        globals.birthday_list = globals.json_obj["birthday"]
        globals.bot_data = globals.json_obj["bot_data"]
        globals.reminder_list = globals.json_obj["reminders"]
        globals.DB_LOADED = True


# Update contents in JSON database
# If no_log is specified, this action won't be logged
def update(no_log=None):
    if globals.DB_UPDATE_DISABLED:
        if no_log == False or no_log == None:
            logs.error("database " + str(globals.db_file_path) + " not updated ", 'Database')
        return
    
    with open('db.json', 'w') as openfile:
        globals.json_obj["srani"] = globals.srani_list
        globals.json_obj["birthday"] = globals.birthday_list
        globals.json_obj["bot_data"] = globals.bot_data
        globals.json_obj["reminders"] = globals.reminder_list
        json.dump(globals.json_obj, openfile, indent=1)
    
    if no_log == False or no_log == None:
        logs.info("updated database " + str(globals.db_file_path), 'Database')

# ---------- #
# ----------
#   BOT_EVENTS.PY
# ----------   
#   Module for handling discord bot events
# ---------- #

import globals
import database
import logs
import utility
import discord
import srani
import random
from discord.ext import commands

bot = globals.bot

async def on_ready():
    await database.load()

    logs.info('Logged in as {0.user}'.format(globals.bot), 'Initialization')
    logs.info('Bot run number ' + str(globals.bot_data["bot_runs"] + 1), 'Initialization')
    
    await database.member_refresh(True)
    logs.info('Loaded database', 'Initialization')

    utility.load_svatky()
    logs.info('Svatky loaded', 'Initialization')

    utility.start_periods()
    logs.info('Periodical events started', 'Initialization')

    if globals.MESSAGE_LOGGING_ENABLED:
        logs.info("Message logging into " + globals.msg_logs_file_path + " file enabled", 'Initialization')

    utility.update_bot_runs()
    await utility.change_bot_activity(discord.Status.online, "Ready! Try '$help' for commands list.")
    logs.info('Initialization completed - bot is running and is ready for input', 'Initialization')

    if globals.DB_AUTO_RECOVERY and globals.DB_EMPTY:
        await database.recovery(globals.bot.get_channel(globals.channel_general))


async def on_message(message):
    # do not reply on bot messages or when database is not being updated
    if message.author == bot.user or globals.DB_UPDATE_DISABLED:
        return

    # log messages, process commands
    try:
        logs.user_message(message.channel.name, str(message.author), message.content)
    except:
        pass
    await globals.bot.process_commands(message)

    # check if user is in database (if not - add him)
    author_id = message.author.id
    srani_member = srani.get_member(author_id)
    if srani_member == None:
        await srani.new_member(message.author.id)
        srani_member = srani.get_member(author_id)

    # poop tags
    await srani.add_if_tag_in_message(message, message.author.id, True)
    await srani.check_board_changes(message.channel, message.author.id, str(message.author))

    # bot tag/mention
    if globals.tag_bot_self in message.content:
        await message.reply(random.choice(globals.bot_tag))
        globals.tagy_count = globals.tagy_count + 1
        database.update(True)

    # reply to predefined messages
    await utility.bot_predefined_message_reply(message)

async def on_guild_channel_delete(channel):
    await utility.bot_message_to_channel("Kanal " + channel.name + " vypadl z okna!", globals.channel_kgb)

async def on_guild_channel_create(channel):
    await utility.bot_message_to_channel("Buh nam pozehnal novym kanalem " + channel.name + "!", globals.channel_kgb)

async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound) or isinstance(error, commands.errors.CommandNotFound):
        await ctx.send(
            random.choice([
                'Neznamy prikaz! Zkus $help.',
                'Takovy prikaz urcite umet nemam. Co takhle zkusit $help?',
                'Nechapu, co po mne tedka chces.',
                'Spatnej prikaz',
                '$help exists, your command does not'
            ]))

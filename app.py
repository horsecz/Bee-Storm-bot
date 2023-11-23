# ---------- #
# ----------
#   APP.PY
# ----------   
#   Core module for bot start, run and handling
# ---------- #

import globals
import logs
import sys
import bot_events
import bot_commands
import bot_tasks
from discord.ext import commands, tasks

bot = globals.bot

# Bot events declarations

@bot.event
async def on_ready():
    await bot_events.on_ready()

@bot.event
async def on_message(message):
    await bot_events.on_message(message)

@bot.event
async def on_guild_channel_delete(channel):
    await bot_events.on_guild_channel_delete(channel)

@bot.event
async def on_guild_channel_create(channel):
    await bot_events.on_guild_channel_create(channel)

@bot.event
async def on_command_error(ctx, error):
    await bot_events.on_command_error(ctx, error)

# Bot commands declarations

@bot.command()
async def runtime(ctx):
    await bot_commands.runtime(ctx)

@bot.command()
async def github(ctx):
    await bot_commands.github(ctx)

@bot.command()
async def git(ctx):
    await bot_commands.github(ctx)

@bot.command()
async def help(ctx):
    await bot_commands.help(ctx)

@bot.command(pass_context=True)
async def repeat(ctx, *args):
    await bot_commands.repeat(ctx, *args)

@bot.command()
async def hello(ctx):
    await bot_commands.hello(ctx)

@bot.command()
async def tagy(ctx):
    await bot_commands.tagy(ctx)

@bot.command()
async def totalsrani(ctx):
    await bot_commands.totalsrani(ctx)

@bot.command()
async def sraniboard(ctx):
    await bot_commands.sraniboard(ctx)

@bot.command()
async def sranistats(ctx):
    await bot_commands.sranistats(ctx)

@bot.command()
async def pentaboard(ctx):
    await bot_commands.pentaboard(ctx)


@bot.command()
async def multiboard(ctx):
    await bot_commands.multiboard(ctx)

@bot.command()
async def svatek(ctx, *args):
    await bot_commands.svatek(ctx, *args)

# Admin commands declarations

@bot.command()
@commands.is_owner()
async def files(ctx):
    await bot_commands.files(ctx)

@files.error
async def files_error(ctx, error):
    await bot_commands.admin_command_error(ctx, error)

@bot.command()
@commands.is_owner()
async def msg_remove(ctx, *args):
    await bot_commands.msg_remove(ctx, *args)

@msg_remove.error
async def msg_remove_error(ctx, error):
    await bot_commands.admin_command_error(ctx, error)

@bot.command()
@commands.is_owner()
async def admin(ctx):
    await bot_commands.admin(ctx)

@admin.error
async def admin_error(ctx, error):
    await bot_commands.admin_command_error(ctx, error)

@bot.command()
@commands.is_owner()
async def refreshdata(ctx):
    await bot_commands.refreshdata(ctx)

@refreshdata.error
async def refreshdata_error(ctx, error):
    await bot_commands.admin_command_error(ctx, error)

# Tasks declarations

@tasks.loop(hours=1)
async def daily_message():
    await bot_tasks.daily_message()

@tasks.loop(hours=1)
async def dead_room_revival():
    await bot_tasks.dead_room_revival()

# Run

try:
    logs.info('Starting bot ...', 'Bot start')
    globals.bot.run(globals.BOT_TOKEN)
except Exception as e:
    logs.exception(e, 'Bot start')
    sys.exit(1)
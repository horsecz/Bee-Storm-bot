# ---------- #
# ----------
#   BOT_COMMMANDS.PY
# ----------   
#   Module for handling discord bot commands
# ---------- #

import globals
import random
import srani
import discord
import sys
import logs
import asyncio

##
##
## BASIC COMMANDS
##
##

async def github(ctx):
    await ctx.reply(globals.text_github)

async def help(ctx):
    await ctx.send(globals.help_message)

async def repeat(ctx, *args):
    if len(args) == 0:
        await ctx.send(
            random.choice(['Co mam jako opakovat?', 'Nejakej text k opakovani by se hodil', 'Gde text']))
    elif len(args) == 1:
        await ctx.send(args[0])
    else:
        await ctx.send(args[0])
        await ctx.send(args[1])
        await ctx.send("Vic delat nebudu.")

async def hello(ctx):
    await ctx.send(random.choice(globals.hello_cmd))

async def tagy(ctx):
    await ctx.send("Pocet otravnych tagu mne: " + str(globals.tagy_count))

async def totalsrani(ctx):
    await ctx.send("Na tomto serveru se sralo jiz celkem: " + str(globals.bot_data["total_poops"]) + "x")
    if globals.DB_RECOVERY_RUNNING:
        await ctx.send("Upozorneni: Probiha obnova databaze - data se mohou menit a nemusi byt momentalne presna.")

async def sraniboard(ctx):
    if srani.find_top_pooper_count() > 0:
        await srani.refresh_order(ctx)
        i = 0
        text = ""
        while (i < 5):
            id = globals.srani_order[i][0]
            name = await globals.bot.fetch_user(id)
            name = name.name
            count = str(globals.srani_order[i][1])
            text = text + "\n **" + str(i + 1) + ".** " + name + " (" + count + " srani)"
            i = i + 1
        await ctx.send("** **\n**SRANIBOARD** - top 5 nejvetsich sracu:\n" + text + "\n")
    else:
        await ctx.send("Na tomto serveru maji bohuzel vsichni zacpu nebo jeste nikdo nesral.")

    if globals.DB_RECOVERY_RUNNING:
        await ctx.send("Upozorneni: Probiha obnova databaze - data se mohou menit a nemusi byt momentalne presna.")

##
##
## ADMIN COMMANDS
##
##

async def command_error(ctx, error):
    if isinstance(error, globals.commands.NotOwner):
        await ctx.send(random.choice(["Tento prikaz muze pouzivat pouze muj vlastnik.",
                                      "Zneuzivani tohoto prikazu je povoleno vsem uzivatelum, kteri jsou mym vlastnikem",
                                      "Nelze mne zneuzit pro tento prikaz. Nejsi muj vlastnik.",
                                      "Vykonani prikazu bylo stornovano. (spoluprace s nevlastniky neni ve smlouve)",]))

async def files(ctx):
    await ctx.send("Zde jsou vsechny soubory:",
                   files=[
                       discord.File(globals.db_file_path),
                       discord.File(globals.log_file_path),
                       discord.File(globals.msg_logs_file_path)
                   ])

async def shutdown(ctx):
    logs.info('Administrator executed command to shut down the bot - shutting down ...', 'Shutdown')
    async with ctx.typing():
        await globals.bot.close()
        globals.bot.destroy()
    sys.exit(0)

async def msg_remove(ctx, *args):
    number = 0
    exception = False
    if (len(args) != 1):
        await ctx.send("Spatny pocet argumentu! Cekam jen jedno cislo.")
        return
    try:
        number = int(args[0])
    except:
        exception = True
    if (exception):
        await ctx.send("CISLO! Ten argument ma byt CELY CISLO!")
        return
    if (number < 1):
        await ctx.send(
            "Fakt ti musim pripominat, ze to cislo ma byt vetsi jak 0?")
        return
    if (number > 100):
        await ctx.send("Vazne chces po me smazat vic jak 100 zprav?")
        return

    i = 0
    channel = ctx.channel
    number = number + 1
    async for msg in channel.history(limit=number):
        await msg.delete()
        await asyncio.sleep(1)
        i = i + 1

    await ctx.send("Smazal jsem " + str(number - 1) + " zprav.")

async def admin(ctx):
    await ctx.send(globals.admin_help)

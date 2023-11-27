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
import utility
import database
import datetime
from discord.ext import commands

##
##
## BASIC COMMANDS
##
##

async def runtime(ctx):
    begin_day = str(globals.bot_start_time.day)
    begin_month = str(globals.bot_start_time.month)
    begin_year = str(globals.bot_start_time.year)
    begin_hour = str(globals.bot_start_time.hour)
    begin_minute = str(globals.bot_start_time.minute)
    text = "Naposledy jsem byl spusten " + begin_day + ". " + begin_month + ". " + begin_year + " v " + begin_hour + " hodin a " + begin_minute + " minut."
    await ctx.send(text)

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
    await utility.bot_recovery_warning(ctx)
    if srani.find_top_pooper_count() > 0:
        await srani.refresh_order()
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

async def sranistats(ctx):
    await srani.refresh_order()

    name = str(ctx.message.author)
    id = ctx.message.author.id
    member = srani.get_member(id)
    if (member == None):
        logs.error('Member ' + str(name) + ' (ID ' + str(id) + ') not found in database when executing command $sranistats', 'Command')
        await ctx.send('Nepodarilo se mi zobrazit tvoje statistiky, nevim kdo jsi a neco je spatne. (<@'+ str(globals.OWNER_ID) +'> help)')
        return
    
    count = str(member["count"])
    multi = str(member["multikills"])
    pentas = str(member["pentakills"])
    hexas = str(member["hexakills"])
    legend = str(member["legendary kills"])
    position = -1
    i = 0
    while (i < len(globals.srani_order)):
        if (globals.srani_order[i][0] == id):
            position = str(i + 1)
            break
        i = i + 1

    if (position == -1):
        position = "?"
        logs.error('Member ' + str(name) + ' (ID ' + str(id) + ') position stat not found when executing command $sranistats', 'Command')
        await ctx.send('Nepodarilo se mi urcit tvoji pozici ve $sraniboard, neco je spatne. (<@'+ str(globals.OWNER_ID) +'> help)')
    
    await ctx.send("** **\n **Statistiky uzivatele " + name +
                   ":**\n\n Pocet srani: " + count + "\n Poradi: " + position +
                   ".\n\n Multikilly: " + multi + "\n Pentakilly: " + pentas +
                   "\n Hexakilly: " + hexas + "\n Legendary killy: " + legend)

async def pentaboard(ctx):
    await utility.bot_recovery_warning(ctx)
    if srani.find_top_pooper_count() > 0 and len(globals.srani_order_penta) > 0:
        await srani.refresh_order()
        i = 0
        while (i < len(globals.srani_order_penta) and i < 5):
            id = globals.srani_order_penta[i][0]
            name = await globals.bot.fetch_user(id)
            name = name.name
            count = str(globals.srani_order_penta[i][1])
            text = text + "\n **" + str(i + 1) + ".** " + name + " (" + count + " pentakillu)"
            i = i + 1

        await ctx.send("** **\n**PENTABOARD** - top 5 nejvetsich pentakilleru:\n" + text +"\n")
    else:
        await ctx.send("Nikdo jeste neudelal pentakill. Jak smutne :(")

async def multiboard(ctx):
    await utility.bot_recovery_warning(ctx)
    if srani.find_top_pooper_count() > 0 and len(globals.srani_order_multi) > 0:
        await srani.refresh_order()
        i = 0
        while (i < len(globals.srani_order_multi) and i < 5):
            id = globals.srani_order_multi[i][0]
            name = await globals.bot.fetch_user(id)
            name = name.name
            count = str(globals.srani_order_multi[i][1])
            text = text + "\n **" + str(
                i + 1) + ".** " + name + " (" + count + " multikillu)"
            i = i + 1

        await ctx.send("** **\n**MULTIBOARD** - top 5 nejvetsich multikilleru:\n" + text +"\n")
    else:
        await ctx.send("Nikdo jeste nezvladl dat DoubleKill nebo vetsi, coz je fakt divne.")

async def svatek(ctx, *args):
    today_date = datetime.now(globals.timezone)
    if len(args) == 0:
        day = today_date.day
        month = today_date.month
        await ctx.send("Dnes ma svatek " + globals.mesice[month - 1][day - 1] + ".")
    elif len(args) == 2:
        try:
            day = int(args[0])
            month = int(args[1])
        except (ValueError):
            await ctx.send("Dva dodatecne argumenty musi byt cisly. (den a mesic)")
            return
        if day > 0 and day <= 31 and month > 0 and month <= 12:
            await ctx.send("Dne " + str(args[0]) + ". " + str(args[1]) + ". ma svatek " + globals.mesice[month - 1][day - 1] + ".")
        else:
            await ctx.send("Nemas spravne datum - den je cislo v rozsahu 1-31, mesic v rozsahu 1-12.")
    else:
        await ctx.send("Naprosto spatny pocet argumentu. Bud nema byt uveden ani jeden, nebo presne dve cisla.") 


##
##
## ADMIN COMMANDS
##
##

async def admin_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send(random.choice(["Tento prikaz muze pouzivat pouze muj vlastnik.",
                                      "Zneuzivani tohoto prikazu je povoleno vsem uzivatelum, kteri jsou mym vlastnikem",
                                      "Nelze mne zneuzit pro tento prikaz. Nejsi muj vlastnik.",
                                      "Vykonani prikazu bylo stornovano. (spoluprace s nevlastniky neni ve smlouve)",]))

async def files(ctx):
    await ctx.send("Zde jsou vsechny soubory:", files=[discord.File(globals.db_file_path),discord.File(globals.log_file_path),discord.File(globals.msg_logs_file_path)])

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

async def refreshdata(ctx):
    logs.info('Admin started manual database recovery.', 'Command')
    try:
        await database.recovery()
    except Exception as e:
        logs.exception(e, 'Command')

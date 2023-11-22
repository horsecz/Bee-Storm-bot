# ---------- #
# ----------
#   MAIN.OLD_SOURCE.PY
# ---------- 
# ---------- 
# ---------- 
# ---------- 
# 
#   OLD BOT SOURCE CODE
# 
#   TODO    To be removed entirely
#           (completed refactored code = removed from here and is/is not present in new source code)
# ---------- 
# ---------- 
# ---------- 
# ----------   
# ---------- #

import random
import sys
import subprocess
import time


def getBotRuntimeString():
    begin_day = str(now.day)
    begin_month = str(now.month)
    begin_year = str(now.year)
    begin_hour = str(now.hour)
    begin_minute = str(now.minute)
    return "Naposledy jsem byl spusten " + begin_day + ". " + begin_month + ". " + begin_year + " v " + begin_hour + " hodin a " + begin_minute + " minut."


def getDateTime():
    current_day = str(datetime.now(timezone).day)
    current_month = str(datetime.now(timezone).month)
    current_year = str(datetime.now(timezone).year)
    current_hour = str(datetime.now(timezone).hour)
    current_minute = str(datetime.now(timezone).minute)
    return "Dnes je " + current_day + ". " + current_month + ". " + current_year + ", " + current_hour + " hodin a " + current_minute + " minut."

def findSraniMemberByID(id):
    for members in srani_list:
        if members["id"] == id:
            return members
    return None


def getSraniCountByID(id):
    member = findSraniMemberByID(id)
    return member["count"]


def getSraniNameByID(id):
    member = findSraniMemberByID(id)
    return member["name"]


def getSvatekString(day, month):
    global mesice
    return mesice[month - 1][day - 1]

async def addReminder(id, tag, text, datetime):
    global reminder_list
    name = await bot.fetch_user(id)
    name = name.name
    try:
        nametag = []
        nametag.append(id)
        nametag.append(tag)

        date = []
        year = str(int(datetime.year))
        month = str(int(datetime.month))
        day = str(int(datetime.day))
        hour = str(int(datetime.hour))
        minute = str(int(datetime.minute))
        date.append(day)
        date.append(month)
        date.append(year)
        date.append(hour)
        date.append(minute)

        id = getNewReminderID(id)

        user_reminder = []
        user_reminder.append(nametag)
        user_reminder.append(text)
        user_reminder.append(date)
        user_reminder.append(id)
        reminder_list.append(user_reminder)
        log_print('addReminder(...): member ' + name + ' added reminder [' +
                  str(id) + '] on ' + day + "/" + month + "/" + year + " at " +
                  hour + ":" + minute)
        db_update()
    except Exception as e:
        log_print('[HANDLED EXCEPTION] addReminder: ' + str(e))
        return


def getNewReminderID(id):
    global reminder_list
    cnt = 0
    used_ids = []
    for people in reminder_list:
        if people[0][0] == id:
            cnt = cnt + 1
            used_ids.append(people[3])

    i = 0
    used_ids.sort()
    for id in used_ids:
        if not id == i:
            cnt = i
            break
        i = i + 1
    return cnt


def getReminderCountOfUser(id):
    global reminder_list
    cnt = 0
    used_ids = []
    for people in reminder_list:
        if people[0][0] == id:
            cnt = cnt + 1
            used_ids.append(people[3])
    return cnt


def getReminderListOfUser(id):
    global reminder_list
    reminders = []
    try:
        for people in reminder_list:
            if people[0][0] == id:
                reminders.append(people)
    except Exception as e:
        log_print('[HANDLED EXCEPTION] getReminderListOfUser: ' + str(e))
    return reminders


async def removeReminder(user_id, id):
    global reminder_list
    name = await bot.fetch_user(user_id)
    name = name.name
    for people_data in reminder_list:
        if people_data[0][1] == user_id and int(people_data[3]) == int(id):
            reminder_list.remove(people_data)
            db_update()
            log_print('removeReminder(...): removed reminder ' + str(id) +
                      ' of user ' + name)
            return True
    log_print('removeReminder(...): reminder ' + str(id) + ' of member ' +
              name + ' was not found')
    return False


#######################

# Prikazy    


@bot.command()
async def sranistats(ctx):
    await refreshSraniOrder(ctx.channel)
    name = str(ctx.message.author)
    id = ctx.message.author.id
    member = getSraniMember(id)
    if (member == None):
        log_print('Member ' + str(name) + ' not found!')
        await ctx.send('Interni chyba pri vypisu statistik [UNKN_MEMB]')
        return
    #id = str(member["id"])
    count = str(member["count"])
    multi = str(member["multikills"])
    pentas = str(member["pentakills"])
    hexas = str(member["hexakills"])
    legend = str(member["legendary kills"])
    position = -1
    i = 0
    while (i < len(srani_order)):
        if (srani_order[i][0] == id):
            position = str(i + 1)
            break
        i = i + 1
    if (position == -1):
        position = "nezname"
    #log_print(name + ' requested starnistats')
    await ctx.send("** **\n **Statistiky uzivatele " + name +
                   ":**\n\n Pocet srani: " + count + "\n Poradi: " + position +
                   ".\n\n Multikilly: " + multi + "\n Pentakilly: " + pentas +
                   "\n Hexakilly: " + hexas + "\n Legendary killy: " + legend)
    if DB_RECOVERY_RUNNING:
        await ctx.send(
            "Upozorneni: Probiha obnova databaze - data se mohou menit a nemusi byt presna."
        )

@bot.command()
async def runtime(ctx):
    await ctx.send(getBotRuntimeString())


@bot.command()
async def svatek(ctx, *args):
    today_date = datetime.now(timezone)
    if len(args) == 0:
        day = today_date.day
        month = today_date.month
        await ctx.send("Dnes ma svatek " + getSvatekString(day, month) + ".")
    elif len(args) == 2:
        try:
            day = int(args[0])
            month = int(args[1])
        except (ValueError):
            await ctx.send(
                "Dva dodatecne argumenty musi byt cisly. (den a mesic)")
            return
        if day > 0 and day <= 31 and month > 0 and month <= 12:
            await ctx.send("Dne " + str(args[0]) + ". " + str(args[1]) +
                           ". ma svatek " + getSvatekString(day, month) + ".")
        else:
            await ctx.send(
                "Nemas spravne datum - den je cislo v rozsahu 1-31, mesic v rozsahu 1-12."
            )
    else:
        await ctx.send(
            "Naprosto spatny pocet argumentu. Bud nema byt uveden ani jeden, nebo presne dve cisla."
        )


@bot.command()
async def pentaboard(ctx):
    if findHighestSrani() > 0:
        await refreshSraniOrder(ctx.channel)
        i = 0
        text = ""
        while (i < 5):
            id = srani_order_penta[i][0]
            name = await bot.fetch_user(id)
            name = name.name
            count = str(srani_order_penta[i][1])
            text = text + "\n **" + str(
                i + 1) + ".** " + name + " (" + count + " pentakillu)"
            i = i + 1
        await ctx.send(
            "** **\n**PENTABOARD** - top 5 nejvetsich pentakilleru:\n" + text +
            "\n")
    else:
        await ctx.send("Nikdo jeste neudelal pentakill.")
    if DB_RECOVERY_RUNNING:
        await ctx.send(
            "Upozorneni: Probiha obnova databaze - data se mohou menit a nemusi byt presna."
        )


@bot.command()
async def multiboard(ctx):
    if findHighestSrani() > 0:
        await refreshSraniOrder(ctx.channel)
        i = 0
        text = ""
        while (i < 5):
            id = srani_order_multi[i][0]
            name = await bot.fetch_user(id)
            name = name.name
            count = str(srani_order_multi[i][1])
            text = text + "\n **" + str(
                i + 1) + ".** " + name + " (" + count + " multikillu)"
            i = i + 1
        await ctx.send(
            "** **\n**MULTIBOARD** - top 5 nejvetsich multikilleru:\n" + text +
            "\n")
    else:
        await ctx.send("Nikdo jeste nezvladl dat DoubleKill nebo vetsi.")
    if DB_RECOVERY_RUNNING:
        await ctx.send(
            "Upozorneni: Probiha obnova databaze - data se mohou menit a nemusi byt presna."
        )

@bot.command()
@commands.is_owner()
async def reboot(ctx):
    global bot_data
    global REBOOT_CMD
    await ctx.send("Bot bude restartovan!")
    bot_data["rebooted"] = True
    REBOOT_CMD = True
    db_update()
    await bot.close()
    bot.destroy()


@reboot.error
async def reboot_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("Pouze muj vlastnik me muze restartovat prikazem.")


@bot.command()
@commands.is_owner()
async def refreshdata(ctx):
    try:
        log_print('[COMMAND] Admin started databse recovery.')
        await databaseStatsRecovery()
    except Exception as e:
        log_print('[HANDLED EXCEPTION] refreshdata: ' + str(e))


@refreshdata.error
async def refreshdb_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send(
            "Pouze muj vlastnik muze aktualizovat nebo obnovovat databazi.")
    print(str(error))


# $reminder {add/remove/list/syntax} {{add: day}{remove: id/all}} {{add:month}[remove: id]} [year] [hour] [minute] [{text/text:} [...]]
@bot.command()
async def reminder(ctx, *args):
    global reminder_list
    auth_name = str(ctx.author)
    auth_id = ctx.author.id
    tag = str(ctx.author.id)
    if len(args) == 0:
        await ctx.send(
            "Prikaz musi mit alespon 1 argument. Zkus `$reminder syntax`!")
        return
    if args[0] == "syntax":
        await ctx.send(
            "Syntax prikazu:\n`$reminder {add/remove/list/syntax} {{add: day}{remove: id/all}} {{add:month}[remove: id]} [year] [hour] [minute] [{text/text:} [...]]`\n\n**Pouziti:**\n```C\n$reminder syntax    tato zprava\n$reminder list    seznam vsech oznameni uzivatele\n$reminder remove all    smaze vsechny reminders uzivatele\n$reminder remove id [id oznameni]    smaze konkretni reminder\n$reminder add {day} {month} [[year] [hour] [minute]] [{text/text:} [...]]    prida oznameni v dany den\n  neuvedeny rok se doplni na soucasny\n  neuvedena hodina se doplni na 12\n  neuvedena minuta se doplni na 00\n  neuvedeny text se doplni na standardni\n  text je vzdycky posledni argument (napr. $reminder add 20 12 2022 text: Konec posledniho semestru na fitu)\n  klicove slovo 'text' nebo 'text:' je nutne napsat pred textem pripominky, pokud je uveden```"
        )
        return
    elif args[0] == "list":
        text = ""
        reminders = getReminderListOfUser(auth_id)
        if len(reminders) == 0:
            await ctx.send("Uzivatel " + auth_name +
                           " nema nastavene zadne upominky.")
            return
        else:
            for reminder in reminders:
                id = reminder[3]
                remind_text = reminder[1]
                date = reminder[2][0] + "/" + reminder[2][1] + "/" + reminder[
                    2][2] + " (" + reminder[2][3] + ":" + reminder[2][4] + ")"
                text = text + date + " **ID " + str(
                    id) + "**: " + remind_text + "\n"
            await ctx.send("** **\n**Seznam upominek pro uzivatele " +
                           auth_name + "**\n\n" + text)
            return
    elif args[0] == "remove":
        if len(args) == 2:  # all
            if args[1] == "all":
                if (getReminderCountOfUser(auth_id) != 0):
                    temp_reminders_list = []
                    cnt = 0
                    for reminder in reminder_list:
                        if reminder[0][0] == auth_id:
                            temp_reminders_list.append(reminder)
                            cnt = cnt + 1

                    for reminder in temp_reminders_list:
                        reminder_list.remove(reminder)
                    db_update()
                    await ctx.send("Smazany vsechny (" + str(cnt) +
                                   ") pripominky uzivatele " + auth_name)
                    return
                else:
                    await ctx.send(
                        "Nic nebylo smazano - zadne pripominky uzivatele " +
                        auth_name + " nenalazeny.")
                    return
            else:
                await ctx.send(
                    "Spatne pouziti $reminder remove - pri dvou argumentech ocekavam pouze `all`."
                )
                return
        elif len(args) == 3:  # id [id]
            if args[1] == "id":
                nan_exception = False
                id = 0
                date = ""
                found = False
                try:
                    id = int(args[2])
                except:
                    nan_exception = True
                finally:
                    if nan_exception == True:
                        await ctx.send(
                            "Pri $reminder remove id ocekavam jako posledni argument cele cislo."
                        )
                        return
                    for reminders in reminder_list:
                        if (reminders[0][0] == auth_id) and (reminders[3]
                                                             == id):
                            reminder_list.remove(reminders)
                            found = True
                            break
                    if found:
                        await ctx.send("Pripominka (id " + str(id) +
                                       ") uspesna smazana.")
                        return
                    else:
                        await ctx.send("Pripominka s ID " + str(id) +
                                       " nenalezena!")
                        return
            else:
                await ctx.send(
                    "Spatne pouziti $reminder remove - pri trech argumentech ocekavam `id` a `[id].`"
                )
                return
        else:
            await ctx.send(
                "Spatny pocet argumentu pro prikaz $reminder remove.")
            return
    elif args[0] == "add":
        if len(args) < 3:
            await ctx.send(
                "Spatny pocet argumentu pro $reminder add. Minimum: 3")
            return
        else:
            nan_exception = False
            date_exception = False
            today = datetime.now(timezone)
            reminder_date = datetime.now(timezone)
            day = 0
            month = 0
            year = int(today.year)
            hour = 12
            minute = 0
            text = "[Pripominka]"
            i = 3
            if len(args) >= 3:
                try:
                    day = int(args[1])
                    month = int(args[2])
                except:
                    nan_exception = True
            if nan_exception:
                await ctx.send(
                    "Argumenty urcujici den, mesic, rok, hodina a minuta musi byt celym cislem!"
                )
                return

            year_except = False
            hour_except = False
            try:
                year = int(args[3])
                i = 4
            except:
                i = 3
                year_except = True
                year = int(today.year)
            if not year_except:
                try:
                    hour = int(args[4])
                    i = 5
                except:
                    hour = 12
                    i = 4
                    hour_except = True
                if not hour_except:
                    try:
                        minute = int(args[5])
                        i = 6
                    except:
                        minute = 0
                        i = 5

            if (len(args) > 3 and len(args) > i + 1):
                if args[i] == "text" or args[i] == "text:":
                    i = i + 1
                    text = ""
                    while (i < len(args)):
                        text = text + ' ' + args[i]
                        i = i + 1
                else:
                    await ctx.send(
                        "Po datu musi nasledovat argument s klicovym slovem `text` nebo `text:`"
                    )
                    return
            try:
                reminder_date = datetime(day=day,
                                         month=month,
                                         year=year,
                                         hour=hour,
                                         minute=minute,
                                         tzinfo=timezone)
            except:
                date_exception = True
            if date_exception:
                await ctx.send("Neplatne datum pripominky.")
                return
            if (year < today.year) or (
                    month < today.month
                    and year == today.year) or (day < today.day
                                                and month == today.month
                                                and year == today.year):
                await ctx.send("Pripominka nesmi byt v minulosti.")
                return
            if (hour < today.hour and day == today.day and month == today.month
                    and year == today.year):
                await ctx.send(
                    "Pripominka k dnesnimu dni muze byt pouze v nasledujicich hodinach!"
                )
                return
            if hour == today.hour and day == today.day and month == today.month and year == today.year:
                if minute < today.minute + 1:
                    await ctx.send(
                        "Pripominka k dnesnimu dni muze byt nejdrive minutu od soucasneho casu."
                    )
                    return

            await addReminder(auth_id, tag, text, reminder_date)
            await ctx.send(
                "Pripominka byla uspesne pridana. Upozorneni probehne " +
                reminder_date.strftime("%d.%m.%Y v %H:%M") +
                " v kanalu `#general`")
    else:
        await ctx.send(
            "Druhy argument musi byt `add`,`remove`,`list` nebo `syntax`!")


#################

# pravidelne zpravy


# zprava kazdy den kolem dopoledne 09:30-10:29
@tasks.loop(hours=1)
async def daily_message():
    global daily_message_christmas
    global daily_message_eoy
    global daily_message_birthday
    global DEVMODE
    time_now = datetime.now(timezone)
    daily_message_additional = ""
    console_print_text = ""
    log_print('[TASKS.LOOP] daily_message: looped ')
    if daily_message_christmas:
        daily_message_additional = "Stastne a vesele Vanoce!"
        console_print_text = 'daily_message: Merry Christmas!'
    if daily_message_eoy:
        console_print_text = 'daily_message: Happy New Years Eve!'
        daily_message_additional = "Bezi posledni hodiny roku " + str(
            time_now.year) + "!"
    if len(daily_message_birthday) > 0:
        birthday_name = daily_message_birthday[0]
        additional = ""
        if (daily_message_birthday[1] >= 1900):
            age = int(time_now.year) - daily_message_birthday[1]
            additional = str(age) + ". "
        console_print_text = 'daily_message: Happy ' + additional + 'B-Day to ' + birthday_name
        daily_message = "Dnes je " + str(time_now.day) + ". " + str(
            time_now.month
        ) + ". a podle mych informaci ma " + additional + "narozeniny " + str(
            birthday_name) + "! "
        if (len(daily_message_birthday) > 2):
            daily_message = "Dnes je " + str(time_now.day) + ". " + str(
                time_now.month
            ) + ". a podle mych informaci maji dnes narozeniny: "
            i = 0
            for even_elements in daily_message_birthday:
                if (i % 2 == 0):
                    birthday_name = even_elements
                    daily_message = daily_message + str(birthday_name) + ", "
                i = i + 1
            daily_message = daily_message + "!"
        daily_message_birthday = []
    else:
        console_print_text = 'daily_message: causal message today'
        daily_message = "Dnes je " + str(time_now.day) + ". " + str(
            time_now.month) + ". a svatek ma " + getSvatekString(
                time_now.day, time_now.month) + ". "
    if (int(time_now.hour) == 9
            and int(time_now.minute) >= 30) or (int(time_now.hour) == 10
                                                and int(time_now.minute) < 30):
        channel = bot.get_channel(channel_general)
        if not DEVMODE:
            log_print(console_print_text)
            await channel.send(daily_message + daily_message_additional)


@tasks.loop(seconds=30)
async def reminders_check():
    global reminders_count_check
    global reminder_list
    time_now = datetime.now(timezone)
    channel = bot.get_channel(channel_general)
    if reminders_count_check == 120:
        log_print(
            '[TASKS.LOOP] reminders_check: looped (logged once per hour)')
    reminders_count_check = reminders_count_check + 1
    if reminders_count_check > 120:
        reminders_count_check = 0
    for reminder in reminder_list:
        if (int(time_now.day) == int(reminder[2][0])
                and int(time_now.month) == int(reminder[2][1])
                and int(time_now.year) == int(reminder[2][2])
                and int(time_now.hour) == int(reminder[2][3])):
            if (int(time_now.minute) == int(reminder[2][4])):
                log_print('reminders_check: reminder activated')
                await channel.send("Pripomenuti pro uzivatele <@!" +
                                   reminder[0][1] + ">: " + reminder[1])
                await removeReminder(reminder[0][1], reminder[3])
                log_print(
                    'reminders_check(): automatically removed completed reminder'
                )
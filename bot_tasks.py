import globals
import datetime
import logs
import math
import utility

# After some inactivity in main channel (#general), send some message(s)
async def dead_room_revival():
    channel = globals.bot.get_channel(globals.channel_general)
    message = await channel.fetch_message(channel.last_message_id)
    last_message_time = message.created_at
    today = datetime.now()

    if math.abs(last_message_time.hour - today.hour) > 18 or math.abs(last_message_time.day - today.day) > 1: # TODO not sure it will work properly
        utility.bot_message_to_channel(globals.dead_room_messages, globals.channel_general)    # TODO not sure this will work

# Daily periodical message - reports day, current date, and name day (CZ) 
async def daily_message():
    time_now = datetime.now(globals.timezone)
    daily_message_additional = ""
    if globals.daily_message_christmas:
        daily_message_additional = "Stastne a vesele Vanoce!"
    if globals.daily_message_eoy:
        daily_message_additional = "Bezi posledni hodiny roku " + str(
            time_now.year) + "!"
    if len(globals.daily_message_birthday) > 0:
        birthday_name = globals.daily_message_birthday[0]
        additional = ""
        if (globals.daily_message_birthday[1] >= 1900):
            age = int(time_now.year) - globals.daily_message_birthday[1]
            additional = str(age) + ". "
        daily_message = "Dnes je " + str(time_now.day) + ". " + str(time_now.month) + ". a podle mych informaci ma " + additional + "narozeniny " + str(birthday_name) + "! "
        if (len(globals.daily_message_birthday) > 2):
            daily_message = "Dnes je " + str(time_now.day) + ". " + str(time_now.month) + ". a podle mych informaci maji dnes narozeniny: "
            i = 0
            for even_elements in globals.daily_message_birthday:
                if (i % 2 == 0):
                    birthday_name = even_elements
                    daily_message = daily_message + str(birthday_name) + ", "
                i = i + 1
            daily_message = daily_message + "!"
        globals.daily_message_birthday = []
    else:
        console_print_text = 'daily_message: causal message today'
        daily_message = "Dnes je " + str(time_now.day) + ". " + str(time_now.month) + ". a svatek ma " + globals.mesice[time_now.month - 1][time_now.day - 1] + ". "
    if (int(time_now.hour) == 9 and int(time_now.minute) >= 30) or (int(time_now.hour) == 10 and int(time_now.minute) < 30):
        channel = globals.bot.get_channel(globals.channel_general)
        await channel.send(daily_message + daily_message_additional)
        logs.info('Daily message sent.', 'Tasks')
 
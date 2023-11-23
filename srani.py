# ---------- #
# ----------
#   SRANI.PY
# ----------   
#   Functions related with pooping tags (@TymoveSrani, etc.)
# ---------- #

from audioop import mul
import globals
import database
import logs
import utility
import random
from collections import OrderedDict

def find_top_pooper_count():
    max = 0
    for member in globals.srani_list:
        if member["count"] > max:
            max = member["count"]

    return max

async def refresh_order():
    cnt_dict = {}
    penta_dict = {}
    multi_dict = {}
    for member in globals.srani_list:
        cnt_dict[member["id"]] = member["count"]
        penta_dict[member["id"]] = member["pentakills"]
        multi_dict[member["id"]] = member["multikills"]

    order = OrderedDict(
        sorted(cnt_dict.items(), key=lambda t: t[1], reverse=True))
    penta = OrderedDict(
        sorted(penta_dict.items(), key=lambda t: t[1], reverse=True))
    multi = OrderedDict(
        sorted(multi_dict.items(), key=lambda t: t[1], reverse=True))
    globals.srani_order = list(order.items())
    globals.srani_order_penta = list(penta.items())
    globals.srani_order_multi = list(multi.items())

async def check_board_changes(discord_context, auth_id, auth_name):
    old_srani_order = globals.srani_order
    result = None
    await refresh_order(discord_context)
    i = 0
    j = 0
    while (i < len(old_srani_order)):
        j = 0
        while (j < len(globals.srani_order)):
            if (old_srani_order[i][0] == globals.srani_order[j][0] and globals.srani_order[j][0] == auth_id):
                if (i == j):
                    break
                else:
                    logs.info('Member ' + auth_name + ' changes position (' + str(i + 1) + '->' + str(j + 1) + ')', 'Poop stats')
                    result = [i + 1, j + 1]
                    break
            j = j + 1
        i = i + 1

    if result != None and not globals.DB_RECOVERY_RUNNING:
        async with discord_context.typing():
            await utility.bot_message_to_channel("V zebricku ($sraniboard) se '" + str(auth_name) + "' posunul z **" + str(result[0]) + ". mista** na **" + str(result[1]) + ".**!", globals.channel_general)
    return result

async def add_if_tag_in_message(message, author_id, bot_reply=False):
    if is_tag_in_message(globals.tag_srani, message.content): 
        await add(author_id)
        if bot_reply == True:
            await message.reply(random.choice(globals.tymovesrani))
    if is_tag_in_message(globals.tag_doublekill, message.content):  
        await add(author_id, 'D')
        if bot_reply == True:
            await message.reply(random.choice(globals.tymovesrani + globals.doublekill))
    if is_tag_in_message(globals.tag_triplekill, message.content):  
        await add(author_id, 'T')
        if bot_reply == True:
            await message.reply(random.choice(globals.tymovesrani + globals.triplekill))
    if is_tag_in_message(globals.tag_quadrakill, message.content):  
        await add(author_id, 'Q')
        if bot_reply == True:
            await message.reply(random.choice(globals.tymovesrani + globals.quadrakill))
    if is_tag_in_message(globals.tag_pentakill, message.content):  
        await add(author_id, 'P')
        if bot_reply == True:
            await message.reply(random.choice(globals.tymovesrani + globals.pentakill))
    if is_tag_in_message(globals.tag_hexakill, message.content):  
        await add(author_id, 'H')
        if bot_reply == True:
            await message.reply(random.choice(globals.tymovesrani + globals.hexakill))
    if is_tag_in_message(globals.tag_legendarykill, message.content):  
        await add(author_id, 'L')
        if bot_reply == True:
            await message.reply(random.choice(globals.tymovesrani + globals.legendarykill))

def is_any_tag_in_message(message):
    if globals.tag_srani in message or globals.tag_doublekill in message or globals.tag_triplekill in message:
        return True
    elif globals.tag_quadrakill in message or globals.tag_pentakill in message or globals.tag_hexakill in message:
        return True
    elif globals.tag_legendarykill in message:
        return True
    else:
        return False

def is_tag_in_message(tag, message):
    if tag in message:
        return True
    else:
        return False
    
def get_total():
    return globals.bot_data["total_poops"]

async def add(id, multiType=None):
    await database.member_refresh()
    member = get_member(id)
    member["count"] = member["count"] + 1
    globals.bot_data["total_poops"] = globals.bot_data["total_poops"] + 1
    #logs.info('Incremented srani count for member ' + str(id))

    if multiType == 'P':
       member["pentakills"] = member["pentakills"] + 1
    elif multiType == 'H':
        member["hexakills"] = member["hexakills"] + 1
    elif multiType == 'L':
        member["legendarykills"] = member["legendarykills"] + 1
    
    if not multiType == None:
        member["multikills"] = member["multikills"] + 1

    database.update(True)

def get_member(id):
    for member in globals.srani_list:
        if member["id"] == id:
            return member
    return None

async def new_member(id):
    sraniMember = {
        "id": id,
        "count": 0,
        "multikills": 0,
        "pentakills": 0,
        "hexakills": 0,
        "legendary kills": 0
    }

    globals.srani_list.append(sraniMember)
    database.update(True)
import discord
import os
from discord.ext import commands, tasks
import json
import random
import asyncio
from collections import OrderedDict
from datetime import datetime
import pytz
import sys
import subprocess

# logovani zprav na serveru do souboru
MESSAGE_LOGGING_ENABLED = True

# automatic database recovery mode
#   - v pripade ztraty db bot zacne automatickou obnovu dat/statistik z cele historie [kanal general v AT]
#   - obnova trva vice jak hodinu, data se prubezne pridavaji jako pri beznych operacich, tudiz je mozne db bezne pouzivat i v prubehu obnovy
#   - zacne v pripade ze je promenna True a databaze 'db.json' je prazdna
DB_AUTO_RECOVERY = True

# developer mode, pokud True:
#  - nevypisuje Hello se zmenami pri spusteni do #kgb
#  - nevypisuje pravidelne zpravy do #general
#  - nezapisuje log_print do souboru
#  - neinkrementuje "bot_run" statistiku (pouziva se v logu)
# pouziti:  [na zivem serveru, na lokalnim neni duvod]
#  pri zacatku developmentu setnout na True, aby nevypisoval zpravy pri restartech,
#  po dokonceni (pred finalnim restartem a zacatkem normalniho behu) vratit na False,
#  zaroven nezapomenout na switch last_update_message
DEVMODE = False

# mention-tag ownera pri spustemi v pripade ze dojde k neocekavanemu restartu
RESTART_MENTION = False

# ID ownera
OWNER_ID = 591643151668871168

# zprava po vyvoji, ktera se prida k Hello po spusteni a oznami update - progress, news
# development_finished urcite zda se vypise update zprava (1) nebo bezna (0)
#  - pred finalnim restartem a DEVMODE == False nastavit na 1,
#    po uspesnem spusteni na 0 (s ulozenim tohoto souboru, ''bez restartu'')
#  - bezna zprava existuje pro pripady (vynuceneho) restartu, ktery neprovedl uzivatel,
#    ale napriklad hosting (replit) -- oznaci admina
development_finished = 0
last_update_message = "odstranena fixace uzivatelu v db na jmeno (nove: na id)"

if development_finished != 1:
    if RESTART_MENTION:
        last_update_message = "zadne zmeny, tento restart nebyl proveden adminem - <@!" + str(
            OWNER_ID) + ">?"
    else:
        last_update_message = "zadne zmeny, tento restart nebyl proveden adminem"

# zona casu v datech
timezone = pytz.timezone("Europe/Prague")

# ids kanalu v Annus Team dc
channel_karantena = 663452074893377546
channel_kgb = 988402540343361606
channel_general = 663806194598805504

help_message = "** **\n Nejlepsi bot na celem Discordu, hostovany zdarma na `replit.com`! Prikazy zacinaji znakem dolaru `$` , jinak je syntaxe stejna jako na jinem Discord botovi.\n\nPokud jde o tagy ci reakce na zpravy (napr. uh oh), zprava ci tag muze byt kdekoliv ve zprave (pokud nejde o vyjimku).\n\n\n**Reaguji na tyto zpravy:**\n```C\nuh oh      [pouze na zacatku zpravy]\n69         \ngdebody    \noznaceni srani (@TymoveSrani;@TymovyDoubleKill;...)  zapocita se do statistik\noznaceni bota (@Bee Storm)\n```\n\n**Momentalne rozumim temto prikazum**:\n```C\nhelp        zobrazi tuto zpravu\n\nhello       <no comment>\nrepeat text text2 text3 ...     zopakuje text\nrandomfact    napise nahodny fakt\ngit    github bota (lze taky pouzit: $github)\ntagy        pocet oznaceni bota od posledniho spusteni\n\nsraniboard  leaderboard clenu serveru ve srani\npentaboard  zebricek pentakilleru\nmultiboard  zebricek vsech, co dali Double Kill a vetsi\nsranistats  statistiky uzivatele\n\nruntime     datum a cas posledniho spusteni bota\ntime        soucasne datum a cas\nsvatek [den mesic]     vypise, kdo ma dnes (nebo v dany den) svatek\nbirthdays    vypise narozeniny clenu serveru, kteri si je zapsali\nbirthday {add/remove} {day month} [year]    zapis narozenin do databaze, bez uvedeneho roku neoznami vek\n\nreminder {add/remove/list/syntax}    prikaz pro pridani pripominky, pro vice informaci 'reminder syntax'```\n\n**Automaticky delam tyto veci:**\n```C\nNahodny fakt    kazdych 7 hodin v case 8-21 hodin napisu do generalu nahodny fakt\nDenni zprava    kazdy den kolem obeda napisu:\n  v beznem dni jeho datum a kdo ma svatek\n  v pripade zapsanych narozenin v $birthdays je oznamim ostatnim\n  neco navic v pripade, ze jsou Vanoce nebo Silvestr\nNovy rok    protoze si toho urcite nikdo nevsimne, dam vam vedet kdy zacne Novy rok\nObnova stats    v pripade ztraty obnovim veskere statistiky```\n"

text_github = "Muj zdrojovy kod je open source a najdes ho zde: https://github.com/horsecz/Bee-Storm-bot"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

#########################

# Random messages

bot_tag = [
    'Netaguj mne ty zmrde!',
    'Co takhle tagnout toho pravyho a vcelu nechat byt?',
    'Nemas nic lepsiho na praci nez tagovat bezbranneho bota?',
    '*activating ignore mode ...*', '*Bee Storm has left server.*',
    'Udelej to znova a vymazu te z databaze :)',
    'Jeste jednou me tagnes a kicknu te ze serveru.', 'Co potrebujes?', 'Ano?',
    'Zrovna na necem delam, neslo by to pozdeji?'
]

hello_cmd = [
    'Nazdar', 'Beemec', 'Cauec', 'Tahni', 'Stormec', 'Zdar', 'Zdurburt',
    'Dobry den', 'Ahoj', 'Hello from the other side'
]
tymovesrani = [
    'Uz zase seres?', 'Skvele!', 'Ja uz myslel, ze dnes nepujdes.',
    'Doufam, ze na zachode ...', 'Zrovna jdu taky!',
    'Podstatne vsak je ... stihls to?', 'Uz bylo na case.',
    'Vzhuru do nebes sraniboardu!', 'Bude i dalsi?',
    'Verim, ze mas na vic, dnes ta penta musi padnout!', 'At se dari!',
    'Budu ti drzet palce.', 'Snad ti to pujde jako vcera.', 'Muzu se pridat?',
    'Nemas tam misto i pro vcelu? Taky uz musim.',
    'To je pekne, ale mas toaletak?',
    '*Information acknowledged and sent to China successfully*',
    '@TymoveSrani! Aha vlastne, takhle ne ...',
    '<@&633366955855970343>! Nejsi v tom sam.', 'Preji mnoho uspechu!', 'Ok.',
    'Nezapomen splachnout.',
    'Kdyz mi nekdo rekl, ze dnes budou padat hovna, tak jsem fakt necekal, ze to myslel doslova.',
    'Citim te az sem, a to jsem jen 1500 radku kodu v Pythonu.',
    'Tak to lituju lidi blizko tebe.'
]
doublekill = [
    'Tymovy dvojzarez!', 'Doublekill!', 'Tady se nekdo rozjizdi!',
    'Jen tak dal!', 'Bude triple?',
    'Jenom pokracuj, pentakill je jeste daleko.',
    'Dnes mam dobrou naladu, takze jsem ti zapsal doublekill jako pentu. *kappaPeek*',
    'Nezastavuj se, cim vic tim lip!', 'O dvojzarez vic ve $sranistats!',
    'A je to tam!'
]
triplekill = [
    'Tymovy trojzarez!', 'Triplekill!', 'Dneska skorujes!', 'Bude dnes penta?',
    'Bude quadra?', 'Pentakill blize nez si myslis! Nevzdavej se!',
    'Three done, two more to go.', 'Party zacina!', 'Bomba!',
    'Triplemaster soon!'
]
quadrakill = [
    'Tymovy ctyrzarez!', 'Neboli te brisko?', 'Delas i neco jineho?',
    'Jsi i jinde nez na zachode?', 'Jeste jednou a jsi mezi mistry.',
    'Quadrakill!', 'Verim, ze dnes ta penta padne!',
    'Jde ti to dobre, ale nezapomen delat i neco jineho.'
]
pentakill = [
    'PENTAKILL!!!!!!!!!', 'Gratuluji k dnesnimu prujmu!',
    'Blahopreji k dnesnimu velkemu uspechu!',
    'Pentakill! Vzhledem k rarite je mozne, ze jsi se zapsal do $pentaboard!',
    'A mame tu dalsiho pentakillera!', 'A ted si dej pauzu.',
    'Budeme slavit nebo jeste pokracujes?'
]
hexakill = [
    'Neni cas zajit k lekari?', 'Nepotrebujes spunt?',
    'Dnes tu zrejme nekdo pil projimadlo misto vody ...', 'HEXAKILL!!!',
    'Takova udalost se nestava kazdy den! Toto musime oslavit!',
    'Neuveritelna udalost!'
]
legendarykill = [
    'Nemam volat 155?', 'Je cas si dat pauzu ...',
    'A mame tu noveho rekordmana!',
    'Co takhle s tim pokracovat zitra? Ve dne se daji delat i jine veci ...',
    'Legendarni.'
]
antimod_text = [
    'Takova slova se tu nepouziva!', 'Okamzite si zklidni svuj slovnik.',
    'Jazyk vyslovujici tyto nevhodne fraze muze byt brzy eliminovan!',
    'Slovni spojeni takoveho druhu se zde nesmi pouzivat!',
    'Prestan takto mluvit!', 'Jeste jednou a vymazu te z databaze. :-)'
]
#########################

# Funcs


def start():
    global json_obj
    global srani_list
    global srani_order
    global srani_order_penta
    global srani_order_multi
    global mesice
    global birthday_list
    global random_facts
    global random_facts_count
    global bot_data
    global tagy_count
    global proper_shutdown
    global timezone
    global now
    global runtime_start_date
    global end_of_year
    global daily_message_christmas
    global daily_message_eoy
    global daily_message_birthday
    global reminders_count_check
    global reminder_list
    global recovery_attempts
    global DB_EMPTY
    global DB_RECOVERY_RUNNING

    DB_EMPTY = False
    DB_RECOVERY_RUNNING = False

    timezone = pytz.timezone("Europe/Prague")
    now = datetime.now(timezone)
    runtime_start_date = now.strftime("%d/%m/%Y %H:%M:%S")
    end_of_year = False
    daily_message_christmas = False
    daily_message_eoy = False
    daily_message_birthday = []

    tagy_count = 0

    proper_shutdown = False

    json_obj = {}
    srani_list = []
    srani_order = []
    srani_order_penta = []
    srani_order_multi = []
    mesice = []
    birthday_list = []
    random_facts = []
    random_facts_count = 0
    reminder_list = []

    bot_data = {}

    reminders_count_check = 0
    recovery_attempts = 0


def start_periods():
    try:
        if random_facts_messages.is_running():
            random_facts_messages.restart()
            birthday_check.restart()
            daily_message.restart()
            end_of_year_prep.restart()
            reminders_check.restart()
            return
    except Exception as e:
        log_print('[EXCEPTION] ' + str(e))

    try:
        random_facts_messages.start()
        birthday_check.start()
        daily_message.start()
        end_of_year_prep.start()
        reminders_check.start()
    except Exception as e:
        log_print('[EXCEPTION] ' + str(e))


async def db_load():
    with open('db.json', 'r') as openfile:
        global json_obj
        global srani_list
        global birthday_list
        global bot_data
        global reminder_list
        global DB_EMPTY
        try:
            json_obj = json.load(openfile)
        except:
            channel = bot.get_channel(channel_kgb)
            await channel.send(
                "Data v databazi jsou poskozena a je nutne vytvorit novou.")
            json_obj = {}
            DB_EMPTY = True
            with open('db.json', 'w') as openfile:
                json.dump(json_obj, openfile)
        if not "srani" in json_obj.keys():
            json_obj["srani"] = []
            with open('db.json', 'w') as openfile:
                json.dump(json_obj, openfile)
        if not "birthday" in json_obj.keys():
            json_obj["birthday"] = []
            with open('db.json', 'w') as openfile:
                json.dump(json_obj, openfile)
        if not "bot_data" in json_obj.keys():
            json_obj["bot_data"] = {"bot_runs": 1, "banned": 0}
            with open('db.json', 'w') as openfile:
                json.dump(json_obj, openfile)
        if not "reminders" in json_obj.keys():
            json_obj["reminders"] = []
            with open('db.json', 'w') as openfile:
                json.dump(json_obj, openfile)
        srani_list = json_obj["srani"]
        birthday_list = json_obj["birthday"]
        bot_data = json_obj["bot_data"]
        reminder_list = json_obj["reminders"]


def db_update():
    with open('db.json', 'w') as openfile:
        json_obj["srani"] = srani_list
        json_obj["birthday"] = birthday_list
        json_obj["bot_data"] = bot_data
        json_obj["reminders"] = reminder_list
        json.dump(json_obj, openfile)
    log_print("db_update(): updated database 'db.json'")


def randfacts_load():
    with open('randfacts.txt', 'r') as openfile:
        global random_facts
        global random_facts_count
        lined = openfile.readlines()
        for line in lined:
            random_facts_count = random_facts_count + 1
            random_facts.append("[Random Fact no. " + str(random_facts_count) +
                                "] " + str(line))


def log_print(text):
    print(text)
    if DEVMODE or DB_RECOVERY_RUNNING:
        return
    timedata = datetime.now(timezone)
    log_time = timedata.strftime("%d/%m/%Y %H:%M.%S")
    with open('log.txt', 'a') as logfile:
        logfile.write("[" + log_time + "]: " + text + "\n")


def message_log(channel, author, text):
    if not MESSAGE_LOGGING_ENABLED:
        return
    timedata = datetime.now(timezone)
    log_time = timedata.strftime("%d/%m/%Y %H:%M.%S")
    with open('message_log.txt', 'a') as logfile:
        logfile.write("[" + log_time + "] [#" + channel + "] " + author +
                      " <<'" + text + "'>>\n")


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


async def newSraniMember(id):
    sraniMember = {
        "id": id,
        "count": 0,
        "multikills": 0,
        "pentakills": 0,
        "hexakills": 0,
        "legendary kills": 0
    }

    srani_list.append(sraniMember)
    db_update()


def getSraniMember(id):
    global srani_list
    for member in srani_list:
        if member["id"] == id:
            return member
    return None


async def addSrani(id):
    global srani_list
    await db_member_refresh()
    member_get = getSraniMember(id)
    member_get["count"] = member_get["count"] + 1
    log_print('addSrani(...): count + 1 to member ' + str(id))
    db_update()
    return


def findHighestSrani():
    max = 0
    for member in srani_list:
        if member["count"] > max:
            max = member["count"]

    return max


async def refreshSraniOrder(ctx):
    global srani_list
    global srani_order
    global srani_order_penta
    global srani_order_multi
    cnt_dict = {}
    penta_dict = {}
    multi_dict = {}
    async with ctx.typing():
        for member in srani_list:
            cnt_dict[member["id"]] = member["count"]
            penta_dict[member["id"]] = member["pentakills"]
            multi_dict[member["id"]] = member["multikills"]

    order = OrderedDict(
        sorted(cnt_dict.items(), key=lambda t: t[1], reverse=True))
    penta = OrderedDict(
        sorted(penta_dict.items(), key=lambda t: t[1], reverse=True))
    multi = OrderedDict(
        sorted(multi_dict.items(), key=lambda t: t[1], reverse=True))
    srani_order = list(order.items())
    srani_order_penta = list(penta.items())
    srani_order_multi = list(multi.items())
    #log_print(srani_order[1][0]) # druhe misto [1] / jmeno [0] ([1] - count)


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


async def db_member_refresh():
    global server_member_list
    global srani_list
    for guild in bot.guilds:
        for serverMember in guild.members:
            #log_print(serverMember)
            found = False
            for member in srani_list:
                if serverMember.id == member["id"]:
                    #log_print('<< found')
                    found = True
                    break

            if not found:
                log_print('new member ' + str(serverMember) + 'added to list')
                await newSraniMember(serverMember.id)


async def messageToChannel(message, channel_id):
    channel = bot.guilds[0].get_channel(channel_id)
    await channel.send(message)


def countTagy():
    global tagy_count
    tagy_count = tagy_count + 1


def getSvatekString(day, month):
    global mesice
    return mesice[month - 1][day - 1]


def load_svatky():
    global mesice
    # leden
    mesice.append([
        "Nový rok, Den obnovy samostatného českého státu", "Karina", "Radmila",
        "Diana", "Dalimil", "Tři králové", "Vilma", "Čestmír", "Vladan",
        "Břetislav", "Bohdana", "Pravoslav", "Edita", "Radovan", "Alice",
        "Ctirad", "Drahoslav", "Vladislav", "Doubravka", "Ilona", "Běla",
        "Slavomír", "Zdeněk", "Milena", "Miloš", "Zora", "Ingrid", "Otýlie",
        "Zdislava", "Robin", "Marika"
    ])
    # únor
    mesice.append([
        "Hynek", "Nela", "Blažej", "Jarmila", "Dobromila", "Vanda", "Veronika",
        "Milada", "Apolena", "Mojmír", "Božena", "Slavěna", "Věnceslav",
        "Valentýn", "Jiřina", "Ljuba", "Miloslava", "Gizela", "Patrik",
        "Oldřich", "Lenka", "Petr", "Svatopluk", "Matěj", "Liliana", "Dorota",
        "Alexandr", "Lumír", "Horymír"
    ])
    # březen
    mesice.append([
        "Bedřich", "Anežka", "Kamil", "Stela", "Kazimír", "Miroslav", "Tomáš",
        "Gabriela", "Františka", "Viktorie", "Anděla", "Řehoř", "Růžena",
        "Rút, Matylda", "Ida", "Elena, Herbert", "Vlastimil", "Eduard",
        "Josef", "Světlana", "Radek", "Leona", "Ivona", "Gabriel", "Marián",
        "Emanuel", "Dita", "Soňa", "Taťána", "Arnošt", "Kvido"
    ])
    # duben
    mesice.append([
        "Hugo", "Erika", "Richard", "Ivana", "Miroslava", "Vendula",
        "Heřman, Hermína", "Ema", "Dušan", "Darja", "Izabela", "Julius",
        "Aleš", "Vincenc", "Anastázie", "Irena", "Rudolf", "Valérie",
        "Rostislav", "Marcela", "Alexandra", "Evženie", "Vojtěch", "Jiří",
        "Marek", "Oto", "Jaroslav", "Vlastislav", "Robert", "Blahoslav"
    ])
    # květen
    mesice.append([
        "Svátek práce", "Zikmund", "Alexej", "Květoslav", "Klaudie",
        "Radoslav", "Stanislav", "Den vítězství", "Ctibor", "Blažena",
        "Svatava", "Pankrác", "Servác", "Bonifác", "Žofie", "Přemysl", "Aneta",
        "Nataša", "Ivo", "Zbyšek", "Monika", "Emil", "Vladimír", "Jana",
        "Viola", "Filip", "Valdemar", "Vilém", "Maxmilián", "Ferdinand",
        "Kamila"
    ])
    # červen
    mesice.append([
        "Laura", "Jarmil", "Tamara", "Dalibor", "Dobroslav", "Norbert",
        "Iveta, Slavoj", "Medard", "Stanislava", "Gita", "Bruno", "Antonie",
        "Antonín", "Roland", "Vít", "Zbyněk", "Adolf", "Milan", "Leoš",
        "Květa", "Alois", "Pavla", "Zdeňka", "Jan", "Ivan", "Adriana",
        "Ladislav", "Lubomír", "Petr a Pavel", "Šárka"
    ])
    # červenec
    mesice.append([
        "Jaroslava", "Patricie", "Radomír", "Prokop", "Cyril, Metoděj",
        "Den upálení mistra Jana Husa", "Bohuslava", "Nora", "Drahoslava",
        "Libuše, Amálie", "Olga", "Bořek", "Markéta", "Karolína", "Jindřich",
        "Luboš", "Martina", "Drahomíra", "Čeněk", "Ilja", "Vítězslav",
        "Magdaléna", "Libor", "Kristýna", "Jakub", "Anna", "Věroslav",
        "Viktor", "Marta", "Bořivoj", "Ignác"
    ])
    # srpen
    mesice.append([
        "Oskar", "Gustav", "Miluše", "Dominik", "Kristián", "Oldřiška", "Lada",
        "Soběslav", "Roman", "Vavřinec", "Zuzana", "Klára", "Alena", "Alan",
        "Hana", "Jáchym", "Petra", "Helena", "Ludvík", "Bernard", "Johana",
        "Bohuslav", "Sandra", "Bartoloměj", "Radim", "Luděk", "Otakar",
        "Augustýn", "Evelína", "Vladěna", "Pavlína"
    ])
    # září
    mesice.append([
        "Linda, Samuel", "Adéla", "Bronislav", "Jindřiška", "Boris",
        "Boleslav", "Regína", "Mariana", "Daniela", "Irma", "Denisa", "Marie",
        "Lubor", "Radka", "Jolana", "Ludmila", "Naděžda", "Kryštof", "Zita",
        "Oleg", "Matouš", "Darina", "Berta", "Jaromír", "Zlata", "Andrea",
        "Jonáš", "Václav, Den české státnosti", "Michal", "Jeroným"
    ])
    # říjen
    mesice.append([
        "Igor", "Olivie, Oliver", "Bohumil", "František", "Eliška", "Hanuš",
        "Justýna", "Věra", "Štefan, Sára", "Marina", "Andrej", "Marcel",
        "Renáta", "Agáta", "Tereza", "Havel", "Hedvika", "Lukáš", "Michaela",
        "Vendelín", "Brigita", "Sabina", "Teodor", "Nina", "Beáta", "Erik",
        "Šarlota, Zoe", "Den vzniku samostatného československého státu",
        "Silvie", "Tadeáš", "Štěpánka"
    ])
    # listopad
    mesice.append([
        "Felix", "Památka zesnulých (dušičky)", "Hubert", "Karel", "Miriam",
        "Liběna", "Saskie", "Bohumír", "Bohdan", "Evžen", "Martin", "Benedikt",
        "Tibor", "Sáva", "Leopold", "Otmar",
        "Mahulena, Den boje za svobodu a demokracii", "Romana", "Alžběta",
        "Nikola", "Albert", "Cecílie", "Klement", "Emílie", "Kateřina",
        "Artur", "Xenie", "René", "Zina", "Ondřej"
    ])
    # prosinec
    mesice.append([
        "Iva", "Blanka", "Svatoslav", "Barbora", "Jitka", "Mikuláš",
        "Benjamín", "Květoslava", "Vratislav", "Julie", "Dana", "Simona",
        "Lucie", "Lýdie", "Radana", "Albína", "Daniel", "Miloslav", "Ester",
        "Dagmar", "Natálie", "Šimon", "Vlasta", "Adam, Eva, Štědrý den",
        "1. svátek vánoční", "Štěpán, 2. svátek vánoční", "Žaneta", "Bohumila",
        "Judita", "David", "Silvestr"
    ])


async def databaseStatsRecovery():
    global srani_list
    global DB_RECOVERY_RUNNING

    DB_RECOVERY_RUNNING = True
    await changeBotActivity(discord.Status.idle, "Restoring database.")

    history_poops = 0
    msg_cnt = 0

    doubles = 0
    triples = 0
    quadras = 0
    pentas = 0
    hexas = 0
    legends = 0

    history_members_srani = []
    history_members_double = []
    history_members_triple = []
    history_members_quadra = []
    history_members_penta = []
    history_members_hexa = []
    history_members_legend = []
    history_members_multi = []

    Found = False
    message_channel = bot.get_channel(channel_kgb)
    channel = bot.get_channel(channel_general)
    await message_channel.send(
        '[Obnova statistik] Prave jsem zacal pocitat pocet oznaceni @TymoveSrani;@TymovyDoubleKill a pocet zprav, od zacatku historie kanalu. Rychlost operace je zhruba **5 500 zprav za minutu** a ocekavana doba trvani je zrhuba **70 minut** pri 400 000 zpravach v kanalu. **Databazi je mozne v prubehu obnovy bezne pouzivat.**'
    )
    async for msg in channel.history(limit=None):
        msg_cnt = msg_cnt + 1
        Found = False
        if "<@&633366955855970343>" in msg.content or "<@&821810379952226396>" in msg.content or "<@&809477809772560435>" in msg.content or "<@&809477524828061721>" in msg.content or "<@&800082124009898064>" in msg.content or "<@&828916908413157417>" in msg.content or "<@&939151424963620937>" in msg.content:  #srani (pocita i multikilly)
            history_poops = history_poops + 1
            multikill = False
            await addSrani(msg.author.id)
            for member in history_members_srani:
                if member[0] == msg.author.id:
                    member[1] = member[1] + 1
                    Found = True
                    break
            if not Found:
                union_list = []
                union_list.append(msg.author.id)
                union_list.append(1)
                history_members_srani.append(union_list)
            Found = False
            srani_member = getSraniMember(msg.author.id)
            if "<@&821810379952226396>" in msg.content:  #double
                multikill = True
                doubles = doubles + 1
                selected_list = history_members_double
            if "<@&809477809772560435>" in msg.content:  #triple
                multikill = True
                triples = triples + 1
                selected_list = history_members_triple
            if "<@&809477524828061721>" in msg.content:  #quadra
                multikill = True
                quadras = quadras + 1
                selected_list = history_members_quadra
            if "<@&800082124009898064>" in msg.content:  #penta
                multikill = True
                pentas = pentas + 1
                selected_list = history_members_penta
                srani_member["pentakills"] = srani_member["pentakills"] + 1
            if "<@&828916908413157417>" in msg.content:  #hexa
                multikill = True
                hexas = hexas + 1
                selected_list = history_members_hexa
                srani_member["hexakills"] = srani_member["hexakills"] + 1
            if "<@&939151424963620937>" in msg.content:  #legendary
                multikill = True
                legends = legends + 1
                selected_list = history_members_legend
                srani_member[
                    "legendary kills"] = srani_member["legendary kills"] + 1
            if multikill:
                srani_member["multikills"] = srani_member["multikills"] + 1
                for member in selected_list:
                    if member[0] == msg.author.id:
                        member[1] = member[1] + 1
                        Found = True
                        break
                if not Found:
                    union_list = []
                    union_list.append(msg.author.id)
                    union_list.append(1)
                    selected_list.append(union_list)
                for member in history_members_multi:
                    if member[0] == msg.author.id:
                        member[1] = member[1] + 1
                        Found = True
                        break
                if not Found:
                    union_list = []
                    union_list.append(msg.author.id)
                    union_list.append(1)
                    history_members_multi.append(union_list)

        # progress
        if (msg_cnt == 75000):
            log_print('[DB] Stats recovery: prohledano 75 000 zprav')
        if (msg_cnt == 250000):
            log_print('[DB] Stats recovery: prohledano 250 000 zprav')

    await message_channel.send('[Obnova statistik] Operace uspesne dokoncena.')

    log_print('[DB] Stats recovery: Completed')
    DB_RECOVERY_RUNNING = False
    await changeBotActivity(discord.Status.online,
                            "Ready! Try '$help' for commands list.")
    #log_print('Aktualizovany pocet zprav v generalu: ' + str(msg_cnt))
    #log_print('Aktualizovany TymoveSrani count: ' + str(history_poops))
    #log_print('2/3/4/5/6/7: ' + str(doubles) + "/" + str(triples) + "/" +
    #          str(quadras) + "/" + str(pentas) + "/" + str(hexas) + "/" +
    #          str(legends))
    #log_print('\n\n')
    #log_print('Nove pocty srani clenu serveru:\n !<<<' +
    #          str(history_members_srani) + ">>>!")
    #log_print('Nove pocty doublekillu clenu serveru:\n !<<<' +
    #          str(history_members_double) + ">>>!")
    #log_print('Nove pocty triplekillu clenu serveru:\n !<<<' +
    #          str(history_members_triple) + ">>>!")
    #log_print('Nove pocty quadrakillu clenu serveru:\n !<<<' +
    #          str(history_members_quadra) + ">>>!")
    #log_print('Nove pocty multikillu clenu serveru:\n !<<<' +
    #          str(history_members_multi) + '>>>!')
    #log_print('Nove pocty pentakillu clenu serveru:\n !<<<' +
    #          str(history_members_penta) + ">>>!")
    #log_print('Nove pocty hexakillu clenu serveru:\n !<<<' +
    #          str(history_members_hexa) + ">>>!")
    #log_print('Nove pocty legendary killu clenu serveru:\n !<<<' +
    #          str(history_members_legend) + ">>>!")


async def checkSraniPosChanges(ctx, auth_id, auth_name):
    global srani_order
    old_srani_order = srani_order
    await refreshSraniOrder(ctx)
    i = 0
    j = 0
    while (i < len(old_srani_order)):
        j = 0
        while (j < len(srani_order)):
            if (old_srani_order[i][0] == srani_order[j][0]
                    and srani_order[j][0] == auth_id):
                if (i == j):
                    break
                else:
                    log_print('Member ' + auth_name + ' changes position (' +
                              str(i + 1) + '->' + str(j + 1) + ')')
                    return [i + 1, j + 1]
            j = j + 1
        i = i + 1
    return None


async def addBirthday(id, day, month, year):
    global birthday_list
    try:
        name = await bot.fetch_user(id)
    except Exception as e:
        print(str(e))
        return
    name = str(name.name)
    returnString = None
    if (year < 1900):
        log_print(
            'addBirthday(...): birth year is below 1900, setting empty value [1900]'
        )
        year = 1900
    try:
        date = datetime(day=day, month=month, year=year, tzinfo=timezone)
        print("try")
    except Exception as e:
        print("except")
        log_print(
            '[HANDLED EXCEPTION] raised exception in addBirthday(...): ' + e)
        returnString = "Neplatne datum (napriklad: 31.2.2008)"
    union = []
    union.append(id)

    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    union.append(day)
    union.append(month)
    union.append(year)
    birthday_list.append(union)
    log_print('addBirthday(...): member ' + name + ' added birthday on ' +
              str(day) + '/' + str(month))
    db_update()
    return returnString


def getBirthday(id):
    global birthday_list
    for people_data in birthday_list:
        if people_data[0] == id:
            return people_data
    return None


async def removeBirthday(id):
    global birthday_list
    name = await bot.fetch_user(id)
    for user in birthday_list:
        if user[0] == id:
            log_print('removeBirthday: ' + name.name + ' removed his birthday')
            birthday_list.remove(user)
            db_update()
            return True

    log_print('removeBirthday: not found birthday of user ' + name.name)
    return False


def updateBotRuns():
    if not DEVMODE:
        bot_data["bot_runs"] = bot_data["bot_runs"] + 1
        db_update()


async def recoveryBoot():
    global bot
    global recovery_attempts
    recovery_attempts = recovery_attempts + 1
    if recovery_attempts > 2:
        log_print(
            "[RECOVERY] Too many attempts (3) to re-run bot mercifully. Attempting to restart 'replit' via killing it."
        )
        await changeBotActivity(discord.Status.do_not_disturb,
                                "Disabled! Recovery failed.")
        subprocess.run("kill", "1")
        sys.exit(1)
    try:
        log_print(
            "[RECOVERY] Bot has crashed and is trying to start itself again. (attempt "
            + str(recovery_attempts) + ")")
        bot.run(os.environ['TOKEN'])
    except Exception as e:
        log_print("[EXCEPTION] " + str(e))
        return False

    log_print("[RECOVERY] Recovery successful.")
    await changeBotActivity(discord.Status.online,
                            "Ready in recovery mode! Try '$help'.")
    await handleShutdown()
    return True


async def handleShutdown():
    global proper_shutdown
    if (proper_shutdown):
        log_print("[SHUTDOWN] Bot has been shut down properly.")
        exit(0)
    else:
        await changeBotActivity(
            discord.Status.do_not_disturb,
            "Disabled! Cautious Auto-Recovery in progress.")
        log_print("[SHUTDOWN] Unexpected shutdown of bot.")
        result = await recoveryBoot()
        proper_shutdown = False
        if (result != True):
            sys.exit(1)


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
        log_print('[HANDLED EXCEPTION] ' + str(e))
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
        log_print('[HANDLED EXCEPTION] ' + str(e))
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


async def changeBotActivity(status, string):
    global bot
    activity = discord.Game(name=string)
    await bot.change_presence(status=status, activity=activity)


#########################

# Eventy


@bot.event
async def on_ready():
    start()
    additional = ""
    if (development_finished == 1):
        additional = "\n('-------------------------------- UPDATED [" + last_update_message + "]"
    await db_load()
    log_print('-------------------------------- BOT RUN [' +
              str(bot_data["bot_runs"] + 1) + ']' + additional)
    log_print('[INIT] Logged in as {0.user}'.format(bot))
    await db_member_refresh()
    log_print('[INIT] Database loaded.')
    load_svatky()
    log_print('[INIT] Svatky loaded.')
    randfacts_load()
    log_print('[INIT] Random facts loaded (' + str(len(random_facts)) + ").")
    start_periods()
    log_print('[INIT] All loop/periodical events started.')
    if MESSAGE_LOGGING_ENABLED:
        log_print("[INIT] Message logging into 'message_log.txt' file enabled")
    if not (DEVMODE):
        if (bot_data["banned"] == 0):
            await messageToChannel(
                random.choice([
                    "Priletel ten nejlepsi bot na svete!",
                    "Uz jsem zase tady!",
                    "Bee Storm bot je znovu pripraven k pouziti."
                ]) + "\n(Posledni zmeny: `" + last_update_message + "`)",
                channel_kgb)
        else:
            await messageToChannel(
                random.choice([
                    "Priletel ten nejlepsi bot na svete!",
                    "Uz jsem zase tady!",
                    "Bee Storm bot je znovu pripraven k pouziti."
                ]) +
                "\n(`Automaticke obnoveni behu pri vyjimce docasneho zakazu provozu (hosting problem).`)",
                channel_kgb)
            log_print('[RECOVERY] Recovery was successful.')
            bot_data["banned"] = 0
            db_update()
    log_print('[INIT] Bot is ready for use')
    updateBotRuns()
    await changeBotActivity(discord.Status.online,
                            "Ready! Try '$help' for commands list.")
    if DB_AUTO_RECOVERY and DB_EMPTY:
        await databaseStatsRecovery()


@bot.event
async def on_message(message):
    message_log(message.channel.name, str(message.author), message.content)
    if message.author == bot.user:
        return

    author_id = message.author.id
    srani_member = getSraniMember(author_id)
    change_check = None
    if (srani_member == None):
        log_print("on_message: unknown member " + str(message.author) +
                  " (NEW_MEMB_JOINED) added to list")
        await newSraniMember(message.author.id)
        srani_member = getSraniMember(author_id)

    # bot i
    if '<@!1023637883283841094>' in message.content or '<@1023637883283841094>' in message.content:
        await message.reply(random.choice(bot_tag))
        await addSrani(message.author.id)
        srani_member["multikills"] = srani_member["multikills"] + 1
        change_check = await checkSraniPosChanges(message.channel,
                                                  message.author.id,
                                                  str(message.author))
        countTagy()

    # tymoveSrani
    if '<@&633366955855970343>' in message.content:
        await message.reply(random.choice(tymovesrani))
        await addSrani(message.author.id)
        change_check = await checkSraniPosChanges(message.channel,
                                                  message.author.id,
                                                  str(message.author))

    # doubleKill
    if '<@&821810379952226396>' in message.content:
        await message.reply(random.choice(doublekill))
        await addSrani(message.author.id)
        srani_member["multikills"] = srani_member["multikills"] + 1
        change_check = await checkSraniPosChanges(message.channel,
                                                  message.author.id,
                                                  str(message.author))

    # tripleKill
    if '<@&809477809772560435>' in message.content:
        await message.reply(random.choice(triplekill))
        await addSrani(message.author.id)
        srani_member["multikills"] = srani_member["multikills"] + 1
        change_check = await checkSraniPosChanges(message.channel,
                                                  message.author.id,
                                                  str(message.author))

    # 4Kill
    if '<@&809477524828061721>' in message.content:
        await message.reply(random.choice(quadrakill))
        await addSrani(message.author.id)
        srani_member["multikills"] = srani_member["multikills"] + 1
        change_check = await checkSraniPosChanges(message.channel,
                                                  message.author.id,
                                                  str(message.author))

    # 5Kill
    if '<@&800082124009898064>' in message.content:
        await message.reply(random.choice(pentakill))
        await addSrani(message.author.id)
        srani_member["multikills"] = srani_member["multikills"] + 1
        srani_member["pentakills"] = srani_member["pentakills"] + 1
        change_check = await checkSraniPosChanges(message.channel,
                                                  message.author.id,
                                                  str(message.author))

    # 6Kill
    if '<@&828916908413157417>' in message.content:
        await message.reply(random.choice(hexakill))
        await addSrani(message.author.id)
        srani_member["multikills"] = srani_member["multikills"] + 1
        srani_member["hexakills"] = srani_member["hexakills"] + 1
        change_check = await checkSraniPosChanges(message.channel,
                                                  message.author.id,
                                                  str(message.author))

    # legendaryKill 7+
    if '<@&939151424963620937>' in message.content:
        await message.reply(random.choice(legendarykill))
        await addSrani(message.author.id)
        srani_member["multikills"] = srani_member["multikills"] + 1
        srani_member["legendary kills"] = srani_member["legendary kills"] + 1
        change_check = await checkSraniPosChanges(message.channel,
                                                  message.author.id,
                                                  str(message.author))

    if (change_check) != None and not DB_RECOVERY_RUNNING:
        await messageToChannel(
            "V zebricku ($sraniboard) se '" + str(message.author) +
            "' posunul z **" + str(change_check[0]) + ". mista** na **" +
            str(change_check[1]) + ".**!", channel_general)

    if not message.author.bot:
        if message.content.startswith('uh oh'):
            await message.channel.send('uh oh')
        if '69 ' in message.content or ' 69' in message.content or '69\n' in message.content or '(69' in message.content or '69)' in message.content:
            await message.channel.send('nice')
        if 'gde body' in message.content or 'gdebody' in message.content:
            await message.channel.send('body nigde')
        await bot.process_commands(message)
        if 'nazi mods' in message.content or 'nazi admin' in message.content or 'bad mods' in message.content:
            await message.reply(random.choice(antimod_text))


@bot.event
async def on_guild_channel_delete(channel):
    await messageToChannel("Kanal " + channel.name + " vypadl z okna!",
                           channel_kgb)


@bot.event
async def on_guild_channel_create(channel):
    await messageToChannel(
        "Buh nam pozehnal novym kanalem " + channel.name + "!", channel_kgb)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound) or isinstance(
            error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send(
            random.choice([
                'Neznamy prikaz! Zkus $help.',
                'Takovy prikaz urcite umet nemam. Co takhle zkusit $help?',
                'Nechapu, co po mne tedka chces.'
            ]))


#######################

# Prikazy


@bot.command()
async def github(ctx):
    await ctx.reply(text_github)


@bot.command()
async def git(ctx):
    await ctx.reply(text_github)


@bot.command(pass_context=True)
async def repeat(ctx, *args):
    if len(args) == 0:
        await ctx.send(
            random.choice([
                'Co mam jako opakovat?', 'Nejakej text k opakovani by se hodil'
            ]))
    elif len(args) == 1:
        await ctx.send(args[0])
    else:
        await ctx.send(args[0])
        await ctx.send(args[1])
        await ctx.send("Vic delat nebudu.")


@bot.command()
async def hello(ctx):
    await ctx.send(random.choice(hello_cmd))


@bot.command()
async def tagy(ctx):
    await ctx.send("Pocet otravnych tagu: " + str(tagy_count))


@bot.command()
async def sraniboard(ctx):
    if findHighestSrani() > 0:
        await refreshSraniOrder(ctx.channel)
        i = 0
        text = ""
        while (i < 5):
            id = srani_order[i][0]
            name = await bot.fetch_user(id)
            name = name.name
            count = str(srani_order[i][1])
            text = text + "\n **" + str(
                i + 1) + ".** " + name + " (" + count + " srani)"
            i = i + 1
        await ctx.send("** **\n**SRANIBOARD** - top 5 nejvetsich sracu:\n" +
                       text + "\n")
    else:
        await ctx.send("Nikdo jeste nesral.")
    if DB_RECOVERY_RUNNING:
        await ctx.send(
            "Upozorneni: Probiha obnova databaze - data se mohou menit a nemusi byt presna."
        )


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
async def time(ctx):
    await ctx.send(getDateTime())


@bot.command()
async def runtime(ctx):
    await ctx.send(getBotRuntimeString())


@bot.command()
async def help(ctx):
    await ctx.send(help_message)


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


# vypise zapsane narozeniny vsech clenu
@bot.command()
async def birthdays(ctx):
    global birthday_list
    text = "** **\n**Seznam zapsanych narozenin**\n\n"
    i = 1
    for people in birthday_list:
        name = await bot.fetch_user(people[0])
        name = name.name
        day = people[1]
        month = people[2]
        year = ". " + people[3]
        if (int(people[3]) <= 1900):
            year = " (rok neuveden)"
        date = day + ". " + month
        text = text + name + " dne " + date + year
        i = i + 1
        if (i < len(birthday_list)):
            text = text + ",\n"
        else:
            text = text + ".\n"
    if i == 1:
        text = "Zatim si nikdo narozeniny pomoci prikazu `$birthday add` nezapsal."
    await ctx.send(text)


# birthday {add,remove} {day} {month} [year]
@bot.command()
async def birthday(ctx, *args):
    global birthday_list
    author_name = str(ctx.author)
    author_id = ctx.author.id
    additional_text = ""
    if len(args) > 4 or len(args) == 0:
        await ctx.send(
            "Spatny pocet argumentu. Syntax: `birthday {add} {day} {month} [year]` nebo `$birthday {remove}`."
        )
        return
    else:
        if args[0] == "add":
            if len(args) < 3 or len(args) > 4:
                await ctx.send(
                    "Spatny pocet argumentu. Syntax: `birthday {add} {day} {month} [year]`"
                )
                return
            try:
                day = int(args[1])
                month = int(args[2])
                year = -1
                exception = False

                if (len(args) == 4):
                    year = int(args[3])
            except Exception as e:
                exception = True
                log_print(
                    '[HANDLED EXCEPTION] Raised exception at birthday(...): ' +
                    e)
            finally:
                if exception:
                    await ctx.send(
                        "Argumenty za argumentem `add` musi byt vsechny cela cisla!"
                    )
                    return
                if (day < 1) or (day > 31) or (month < 1) or (month > 12) or (
                        year == 0):
                    await ctx.send(
                        "Den a mesic musi byt v platnem rozmezi, narozeni v rok ukrizovani Jezise se take povazuje za neplatne."
                    )
                    return
                try:
                    datetime(day=day, month=month, year=1900)
                except Exception:
                    await ctx.send("Neplatne datum (napriklad 31.2.)")
                    return
                if year > int(datetime.now().year):
                    await ctx.send("Opravdu ses narodil v budoucnosti?")
                    return
                if year < int(datetime.now().year) - 150 and not year == -1:
                    additional_text = "Protoze jsi **starsi jak 150 let**, tvuj vek jsem radsi skryl."
                    year = 0
                if (getBirthday(author_id) == None):
                    print("none")
                    await addBirthday(author_id, day, month, year)
                    await ctx.send(
                        "Narozeniny pridany. V den narozenin budou ostatni upozorneni v kanalu `#general`. "
                        + additional_text)
                    print("after add")
                else:
                    await removeBirthday(author_id)
                    await addBirthday(author_id, day, month, year)
                    await ctx.send("Narozeniny byly upraveny. " +
                                   additional_text)
        elif args[0] == "remove":
            if len(args) != 1:
                await ctx.send(
                    "Spatny pocet argumentu. Pri `$birthday remove` nema byt zadny jiny argument."
                )
                return

            result = await removeBirthday(author_id)
            if (result):
                await ctx.send("Narozeniny byly smazany.")
            else:
                await ctx.send("Narozeniny uzivatele " + author_name +
                               " nenalezeny.")
            return
        else:
            await ctx.send(
                "Druhy argument ma byt bud `add` nebo `remove`, nic jineho!")
            return


@bot.command()
async def randomfact(ctx):
    global random_facts
    await ctx.reply(random.choice(random_facts))


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    global proper_shutdown
    global bot
    log_print('[SHUTDOWN] Executed command to shut down the bot')
    proper_shutdown = True
    async with ctx.typing():
        channel = bot.get_channel(channel_kgb)
        await channel.send("Bot je vypnut (na prikaz admina).")
        await bot.close()
        bot.destroy()
    sys.exit(0)


# to be done - nezavre session -> shutdown potom nefunguje a bugne bota
#@bot.command()
#@commands.is_owner()
#async def reboot(ctx):
#    global proper_shutdown
#    log_print('[REBOOT] Executed command to reboot the bot')
#    proper_shutdown = True
#    async with ctx.typing():
#        bot.clear()
#        await bot.login(os.environ['TOKEN'])
#        await on_ready()
#        log_print('[REBOOT] Bot rebooted!')
#        await ctx.reply("Restart kompletni!")


@bot.command()
@commands.is_owner()
async def refreshfacts(ctx):
    global random_facts_count
    old_cnt = random_facts_count
    async with ctx.typing():
        randfacts_load()
        new_cnt = random_facts_count - old_cnt
        log_print('[RELOAD] Random facts reloaded by admin. (new: ' +
                  str(new_cnt) + ")")
        channel = bot.get_channel(channel_kgb)
        await channel.send("Seznam nahodnych faktu byl aktualizovan. ")


@shutdown.error
async def shutdown_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("Pouze muj vlastnik me muze vypnout prikazem.")


#@reboot.error
#async def reboot_error(ctx, error):
#    if isinstance(error, commands.NotOwner):
#        await ctx.send("Pouze muj vlastnik me muze restartovat prikazem.")


@bot.command()
@commands.is_owner()
async def refreshdata(ctx):
    try:
        print('kua')
        log_print('[COMMAND] Admin started databse recovery.')
        await databaseStatsRecovery()
    except Exception as e:
        print(str(e))


@refreshdata.error
async def refreshdb_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send(
            "Pouze muj vlastnik muze aktualizovat nebo obnovovat databazi.")
    print(str(error))


@refreshfacts.error
async def refreshfacts_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send(
            "Pouze muj vlastnik muze aktualizovat seznam nahodnych faktu.")


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


# nahodny fakt kazde x h mezi 8-21 hodinou
@tasks.loop(hours=10)
async def random_facts_messages():
    global DEVMODE
    time_now = datetime.now(timezone)
    log_print('[TASKS.LOOP] random_facts_messages: looped ')
    if (int(time_now.hour) > 8 and int(time_now.hour) < 21) and not (DEVMODE):
        channel = bot.get_channel(channel_general)
        await channel.send(random.choice(random_facts))


# zprava kazdy den kolem poledne 11:30-12:29
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
    if (int(time_now.hour) == 11
            and int(time_now.minute) >= 30) or (int(time_now.hour) == 12
                                                and int(time_now.minute) < 30):
        channel = bot.get_channel(channel_general)
        if not DEVMODE:
            log_print(console_print_text)
            await channel.send(daily_message + daily_message_additional)


# kazdodenni check narozenin (3hrs)
@tasks.loop(hours=3)
async def birthday_check():
    global daily_message_birthday
    global birthday_list
    today = datetime.now()
    time_now = today
    log_print('[TASKS.LOOP] birthday_check: looped ')

    daily_message_birthday.clear()
    for people in birthday_list:
        if people[1] == str(int(today.day)) and people[2] == str(
                int(today.month)):
            name = await bot.fetch_user(people[0])
            name = name.name
            daily_message_birthday.append(name)
            if int(people[3]) <= 1900:
                daily_message_birthday.append(0)
            else:
                daily_message_birthday.append(int(people[3]))
            break


# kazdodenni check zda uz se blizi konec roku
@tasks.loop(hours=24)
async def end_of_year_prep():
    global end_of_year
    time_now = datetime.now(timezone)
    log_print('[TASKS.LOOP] end_of_year_prep: looped ')
    if (int(time_now.day) >= 15 and int(time_now.month) == 12
            and not end_of_year):
        end_of_year = True
        end_of_year_messages.start()


# v druhe polovine roku kazdou hodinu check Vanoc, Silvestru a podle toho uprava daily message
@tasks.loop(hours=1)
async def end_of_year_messages():
    global daily_message_christmas
    global daily_message_eoy
    time_now = datetime.now(timezone)
    log_print('[TASKS.LOOP] end_of_year_messages: looped ')
    if (int(time_now.day) == 24):
        daily_message_christmas = True
    if (int(time_now.day) >= 25):
        daily_message_christmas = False
    if (int(time_now.day) == 31):
        daily_message_eoy = True
        if (int(time_now.hour) > 20):
            daily_message_eoy = False
            new_year_message_prep_1.start()
            end_of_year_messages.cancel()
            log_print('[TASKS.LOOP] end_of_year_messages: end of loops ')


@tasks.loop(minutes=1)
async def new_year_message_prep_1():
    time_now = datetime.now(timezone)
    log_print('[TASKS.LOOP] new_year_message_prep_1: looped ')
    if (int(time_now.hour) >= 23 and int(time_now.minute) >= 30):
        new_year_message_prep_1.cancel()
        new_year_message_prep_2.start()
        log_print('[TASKS.LOOP] new_year_message_prep_1: end of loops ')


@tasks.loop(seconds=1)
async def new_year_message_prep_2():
    global end_of_year
    time_now = datetime.now(timezone)
    log_print('[TASKS.LOOP] new_year_message_prep_2: looped ')
    if (int(time_now.hour) == 0 and int(time_now.minute) == 0):
        channel = bot.get_channel(channel_general)
        await channel.send("Stastny novy rok " + str(time_now.year) + "!")
        log_print('new_year_message_prep_2: Happy New Year ' +
                  str(time_now.year))
        new_year_message_prep_2.cancel()
        log_print('[TASKS.LOOP] new_year_message_prep_2: end of loops ')
        end_of_year = False


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


@tasks.loop(hours=1)
async def member_name_check():
    global srani_list


# bot run
try:
    bot.run(os.environ['TOKEN'])
except:
    asyncio.run(
        changeBotActivity(discord.Status.do_not_disturb,
                          "Disabled! Process Auto-Recovery in progress"))
    log_print(
        "[RECOVERY] Exception raised while running bot - temporary ban. Restarting process ..."
    )
    bot_data["banned"] = bot_data["banned"] + 1
    if bot_data["banned"] >= 10:
        log_print("[RECOVERY] Process has been restarted " +
                  str(bot_data["banned"]) + " times without any success.")
        log_print("[RECOVERY] Recovery failed. Exiting ...")
        bot_data["banned"] = 0
        asyncio.run(
            changeBotActivity(discord.Status.do_not_disturb,
                              "Disabled! (Process Auto-Recovery failed)"))
        db_update()
        sys.exit(1)

    db_update()
    subprocess.run("kill", "1")
    sys.exit(1)
finally:
    asyncio.run(handleShutdown())

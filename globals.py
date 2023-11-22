# ---------- #
# ----------
#   GLOBALS.PY
# ----------   
#   Global variables
# ---------- #

import discord
from discord.ext import commands, tasks
import os
from datetime import datetime
import pytz

# Token
#BOT_TOKEN = os.environ["DISCORD_BOT"]
BOT_TOKEN = 'MTAyMzYzNzg4MzI4Mzg0MTA5NA.GbtqmT.KgEREPjGUkovWOXUdIPYhP9LwlWSmqCzgt-atY'

# Bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

# logovani zprav na serveru do souboru
MESSAGE_LOGGING_ENABLED = True

# automatic database recovery mode
#   - v pripade ztraty db bot zacne automatickou obnovu dat/statistik z cele historie [kanal general v AT]
#   - obnova trva vice jak hodinu, data se prubezne pridavaji jako pri beznych operacich, tudiz je mozne db bezne pouzivat i v prubehu obnovy
#   - zacne v pripade ze je promenna True a databaze 'db.json' je prazdna
DB_AUTO_RECOVERY = True

# nevypisuje zpravu pri zapnuti bota
NO_INIT_MSG = True

# mention-tag ownera pri spustemi v pripade ze dojde k neocekavanemu restartu
RESTART_MENTION = False

# ID ownera
OWNER_ID = 591643151668871168

# zona casu v datech
timezone = pytz.timezone("Europe/Prague")

# IDs kanalu v Annus Team dc
channel_karantena = 663452074893377546
channel_kgb = 988402540343361606
channel_general = 663806194598805504

help_message = "** **\n Nejlepsi bot na celem Discordu, hostovany zdarma na `fly.io`! Prikazy zacinaji znakem dolaru `$` , jinak je syntaxe stejna jako na jinem Discord botovi.\n\nPokud jde o tagy ci reakce na zpravy (napr. uh oh), zprava ci tag muze byt kdekoliv ve zprave (pokud nejde o vyjimku).\n\n\n**Reaguji na tyto zpravy:**\n```C\nuh oh      [pouze na zacatku zpravy]\n69         \ngdebody    \noznaceni srani (@TymoveSrani;@TymovyDoubleKill;...)  zapocita se do statistik\noznaceni bota (@Bee Storm)\n```\n\n**Momentalne rozumim temto prikazum**:\n```C\nhelp        zobrazi tuto zpravu\n\nhello       <no comment>\nrepeat text text2 text3 ...     zopakuje text\nrandomfact    napise nahodny fakt\ngit    github bota (lze taky pouzit: $github)\ntagy        pocet oznaceni bota od posledniho spusteni\n\nsraniboard  leaderboard clenu serveru ve srani\npentaboard  zebricek pentakilleru\nmultiboard  zebricek vsech, co dali Double Kill a vetsi\nsranistats  statistiky uzivatele\n\nruntime     datum a cas posledniho spusteni bota\ntime        soucasne datum a cas\nsvatek [den mesic]     vypise, kdo ma dnes (nebo v dany den) svatek\nbirthdays    vypise narozeniny clenu serveru, kteri si je zapsali\nbirthday {add/remove} {day month} [year]    zapis narozenin do databaze, bez uvedeneho roku neoznami vek\n\nreminder {add/remove/list/syntax}    prikaz pro pridani pripominky, pro vice informaci 'reminder syntax'```\n\n**Automaticky delam tyto veci:**\n```C\nNahodny fakt    kazdych 7 hodin v case 8-21 hodin napisu do generalu nahodny fakt\nDenni zprava    kazdy den kolem obeda napisu:\n  v beznem dni jeho datum a kdo ma svatek\n  v pripade zapsanych narozenin v $birthdays je oznamim ostatnim\n  neco navic v pripade, ze jsou Vanoce nebo Silvestr\nNovy rok    protoze si toho urcite nikdo nevsimne, dam vam vedet kdy zacne Novy rok\nObnova stats    v pripade ztraty obnovim veskere statistiky```\n"
text_github = "Muj zdrojovy kod je open source a najdes ho zde: https://github.com/horsecz/Bee-Storm-bot"
admin_help = "**Prikazy vlastnika:**\n\n```C\nshutdown        (opatrne) vypne bota\nreboot      restartuje bota (nasilnou cestou)\nrefreshfacts    obnovi seznam nahodnych faktu\nrefreshdata      zacne automatickou obnovu databaze\nnowelcome        vypne uvitaci zpravu pri zapnuti bota\nfiles          odesle na discord pracovni soubory bota\nmsg_remove [count]        smaze poslednich 'count' zprav v kanale\nrandfactt     zapne/vypne pravidelna nahodna fakta```"
    

# FILES
# log file
log_file_path = 'log.txt'

# JSON database file
db_file_path = 'db.json'

# Random facts file
randfacts_file_path = 'randfacts.txt'

# Message logging file
msg_logs_file_path = 'message_log.txt'

# Tags
tag_srani = "<@&633366955855970343>"
tag_doublekill = "<@&821810379952226396>"
tag_triplekill = "<@&809477809772560435>"
tag_quadrakill = "<@&809477524828061721>"
tag_pentakill = "<@&800082124009898064>"
tag_hexakill = "<@&828916908413157417>"
tag_legendarykill = "<@&939151424963620937>"
tag_bot_self = "<@1023637883283841094>"

#
#### Random messages
#

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
    'Uz zase na zachode?', 
    'Skvele!', 
    'Ja uz myslel, ze dnes nepujdes.',
    'Doufam, ze na zachode ...', 
    'Doufam, ze ne na podlahu ...'
    'Zrovna jdu taky!',
    'Podstatne vsak je ... stihls to?', 
    'Uz bylo na case.',
    'Vzhuru do nebes sraniboardu!', 
    'Bude i dalsi?',
    'Verim, ze mas na vic, dnes ta penta musi padnout! <3', 
    'At se dari!',
    'Budu ti drzet ~~palce~~ zihadlo.', 
    'Snad ti to pujde jako vcera.',
    'Muzu se pridat? Kralovna mi okupuje zachod uz nekolik hodin.',
    'Nemas tam misto i pro vcelu? Taky uz musim a zachod mame furt obsazeny.',
    'To je pekne, ale mas toaletak?',
    '*Information acknowledged and sent to USA successfully*',
    '@TymoveSrani! Aha vlastne, takhle ne ...',
    '<@&633366955855970343>! Nejsi v tom sam.', 
    'Preji mnoho uspechu!', 
    'Ok.',
    'Nezapomen splachnout.',
    'Kdyz mi nekdo rekl, ze dnes budou padat hovna, tak jsem fakt necekal, ze to myslel doslova.',
    'Citim te az sem, a to jsem jen 1500 radku kodu v Pythonu na serveru tisice kilometru od tebe ...',
    'Tak to lituju lidi blizko tebe.',
    'Nevim jak ty, ale ja to dnes na pentu nevidim.',
    'Dekuji za dodrzovani pravidel (3.) serveru!',
    'Hruza',
    'Zas?',
    'Pokyny pro srani:\n1. Sednout na zachod*\n2. @TymoveSrani\n3. Sundat kalhoty*\n4. Utrit zadek*\n5. Splachnout\n6. Pouzit stetku dle potreby\n\n*nepovinne',
    'Pokyny pro srani:\n1. Sundat kalhoty\n2. Sednout na zachod*\n3. @TymoveSrani\n4. Utrit zadek*\n5. Splachnout\n6. Pouzit stetku dle potreby\n\n*nepovinne, ale velmi doporucene',
    'Vynaset odpad znamena odnest obsah kose do popelnice, ne jit srat!',
    'Sikulka',
    'Nezapomen spravne dychat!',
    'Nadech. Vydech. Poradny nadech a tlac!',
    'To zas bude porod.',
    'Je az nemozne jak casto chodis srat ...',
    'Prosim hlavne ne na podlahu, zrovna je vytrena.',
    '||Mmmmmm cokoladka||',
    '||Mmmmmm nutella||',
    '||Mmmmmm hovado!||',
    'No tak to je konec sveta.',
    'Bud tvrdy a dnes pouzij smirkovaci papir misto toaletaku!'
]
doublekill = [
    'Dvojzarez je tam!', 
    'DoubleKill!', 
    'Tady se nekdo rozjizdi!',
    'Jen tak dal!', 
    'Bude triple? Dva jsou fajn, ale 3 > 2!',
    'Jenom pokracuj, pentakill je jeste daleko.',
    'Dnes mam dobrou naladu, takze jsem ti zapsal doublekill jako pentu. *kappaPeek*',
    'Nezastavuj se, cim vic tim lip!', 
    'O dvojzarez vic ve $sranistats!',
    'A je to tam!',
    'Double je fajn, ale co teprve triple!',
    'Pokracuj!'
]
triplekill = [
    'Trojzarez!', 
    'Triplekill!', 
    'Dneska skorujes!', 
    'Bude dnes penta? Jestli ne, tak budu zklamany.',
    'Bude quadra?', 
    'Pentakill blize nez si myslis! Nevzdavej se!',
    'Three done, two more to go.', 
    'Party zacina!', 
    'Bomba!',
    'Dnes mas v sobe spostu vlakniny!',
    'Do par hodin je vitezstvi tvoje!',
]
quadrakill = [
    'Ctyrzarez!', 
    'Neboli te brisko?', 
    'Delas i neco jineho?',
    'Jsi i jinde nez na zachode?', 
    'Jeste jednou a jsi mezi mistry.',
    'Quadrakill!', 
    'Verim, ze dnes ta penta padne!',
    'Jde ti to dobre, ale nezapomen delat i neco jineho.',
    'Co takhle s tou vlakninou ubrat?',
    'Nech taky vyhrat jednou i ostatni.',
    'Skvele! Jeste jednou a je to tam.'
]
pentakill = [
    'PENTAKILL!!!!!!!!!', 
    'Gratuluji k dnesnimu prujmu!',
    'Blahopreji k dnesnimu velkemu uspechu!',
    'Pentakill! O krok blize do $pentaboard!',
    'A mame tu dalsiho pentakillera!', 
    'A ted si dej pauzu.',
    'Budeme slavit nebo jeste pokracujes?',
    'Obcas je fajn delat i neco jineho.',
    'A ted uz muzes jit spat.',
    'Uz neni potreba dal pit to projimadlo.'
]
hexakill = [
    'Neni cas zajit k lekari?', 
    'Nepotrebujes spunt?',
    'Dnes tu zrejme nekdo pil projimadlo misto vody ...', 
    'HEXAKILL!!!',
    'Takova udalost se nestava kazdy den! Toto musime oslavit!',
    'Neuveritelna udalost!',
    'Guinessova kniha rekordu ma novy zaznam!',
    'Neuveritelne co se dnes deje!'
]
legendarykill = [
    'Nemam volat 155?', 
    'Je cas si dat pauzu ...',
    'A mame tu noveho rekordmana!',
    'Co takhle s tim pokracovat zitra? Ve dne se daji delat i jine veci ...',
    'Legendarni.'
]
antimod_text = [
    'Takova slova se tu nepouziva!', 
    'Okamzite si zklidni svuj slovnik.',
    'Jazyk vyslovujici tyto nevhodne fraze muze byt brzy eliminovan!',
    'Slovni spojeni takoveho druhu se zde nesmi pouzivat!',
    'Prestan takto mluvit!', 
    'Jeste jednou a vymazu te z databaze. :-)',
    'Pravidlo 6 vole.'
]

################### Unsorted global variables ## TODO

randfacts_enabled = False
REBOOT_CMD = False

DB_EMPTY = False
DB_RECOVERY_RUNNING = False
DB_LOADED = False
DB_ERROR_SLEEP_TIME = 10
DB_UPDATE_DISABLED = False

RF_STARTED_NOW = True

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
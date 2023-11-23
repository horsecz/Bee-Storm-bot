# ---------- #
# ----------
#   UTILITY.PY
# ----------   
#   Other and utility functions
# ---------- #

import globals
import logs
import database
import discord
import random

async def bot_recovery_warning(discord_context):
    if globals.DB_RECOVERY_RUNNING:
        await discord_context.send("Upozorneni: Probiha obnova databaze - data se mohou menit a nemusi byt presna.")

async def bot_predefined_message_reply(message):
    if message.author.bot:  # dont reply if the message was sent by bot
        return None
    if message.content.startswith('uh oh'):
        await message.channel.send('uh oh')
    if '69 ' in message.content or ' 69' in message.content or '69\n' in message.content or '(69' in message.content or '69)' in message.content:
        await message.channel.send('nice')
    if 'gde body' in message.content or 'gdebody' in message.content:
        await message.channel.send('body nigde')
    if 'nazi mods' in message.content or 'nazi admin' in message.content or 'bad mods' in message.content:
        await message.reply(random.choice(globals.antimod_text))

async def bot_message_to_channel(message, channel_id):
    channel = globals.bot.guilds[0].get_channel(channel_id)
    await channel.send(message)

def start_periods():
    try:
        #daily_message.start()      # TODO
        #reminders_check.start()    # TODO
        pass
    except Exception as e:
        logs.exception(e, 'Periodical events')

async def change_bot_activity(status, string):
    activity = discord.Game(name=string)
    await globals.bot.change_presence(status=status, activity=activity)

def update_bot_runs():
    globals.bot_data["bot_runs"] = globals.bot_data["bot_runs"] + 1
    database.update(True)

def load_svatky():
    # leden
    globals.mesice.append([
        "Nový rok, Den obnovy samostatného českého státu", "Karina", "Radmila",
        "Diana", "Dalimil", "Tři králové", "Vilma", "Čestmír", "Vladan",
        "Břetislav", "Bohdana", "Pravoslav", "Edita", "Radovan", "Alice",
        "Ctirad", "Drahoslav", "Vladislav", "Doubravka", "Ilona", "Běla",
        "Slavomír", "Zdeněk", "Milena", "Miloš", "Zora", "Ingrid", "Otýlie",
        "Zdislava", "Robin", "Marika"
    ])
    # únor
    globals.mesice.append([
        "Hynek", "Nela", "Blažej", "Jarmila", "Dobromila", "Vanda", "Veronika",
        "Milada", "Apolena", "Mojmír", "Božena", "Slavěna", "Věnceslav",
        "Valentýn", "Jiřina", "Ljuba", "Miloslava", "Gizela", "Patrik",
        "Oldřich", "Lenka", "Petr", "Svatopluk", "Matěj", "Liliana", "Dorota",
        "Alexandr", "Lumír", "Horymír"
    ])
    # březen
    globals.mesice.append([
        "Bedřich", "Anežka", "Kamil", "Stela", "Kazimír", "Miroslav", "Tomáš",
        "Gabriela", "Františka", "Viktorie", "Anděla", "Řehoř", "Růžena",
        "Rút, Matylda", "Ida", "Elena, Herbert", "Vlastimil", "Eduard",
        "Josef", "Světlana", "Radek", "Leona", "Ivona", "Gabriel", "Marián",
        "Emanuel", "Dita", "Soňa", "Taťána", "Arnošt", "Kvido"
    ])
    # duben
    globals.mesice.append([
        "Hugo", "Erika", "Richard", "Ivana", "Miroslava", "Vendula",
        "Heřman, Hermína", "Ema", "Dušan", "Darja", "Izabela", "Julius",
        "Aleš", "Vincenc", "Anastázie", "Irena", "Rudolf", "Valérie",
        "Rostislav", "Marcela", "Alexandra", "Evženie", "Vojtěch", "Jiří",
        "Marek", "Oto", "Jaroslav", "Vlastislav", "Robert", "Blahoslav"
    ])
    # květen
    globals.mesice.append([
        "Svátek práce", "Zikmund", "Alexej", "Květoslav", "Klaudie",
        "Radoslav", "Stanislav", "Den vítězství", "Ctibor", "Blažena",
        "Svatava", "Pankrác", "Servác", "Bonifác", "Žofie", "Přemysl", "Aneta",
        "Nataša", "Ivo", "Zbyšek", "Monika", "Emil", "Vladimír", "Jana",
        "Viola", "Filip", "Valdemar", "Vilém", "Maxmilián", "Ferdinand",
        "Kamila"
    ])
    # červen
    globals.mesice.append([
        "Laura", "Jarmil", "Tamara", "Dalibor", "Dobroslav", "Norbert",
        "Iveta, Slavoj", "Medard", "Stanislava", "Gita", "Bruno", "Antonie",
        "Antonín", "Roland", "Vít", "Zbyněk", "Adolf", "Milan", "Leoš",
        "Květa", "Alois", "Pavla", "Zdeňka", "Jan", "Ivan", "Adriana",
        "Ladislav", "Lubomír", "Petr a Pavel", "Šárka"
    ])
    # červenec
    globals.mesice.append([
        "Jaroslava", "Patricie", "Radomír", "Prokop", "Cyril, Metoděj",
        "Den upálení mistra Jana Husa", "Bohuslava", "Nora", "Drahoslava",
        "Libuše, Amálie", "Olga", "Bořek", "Markéta", "Karolína", "Jindřich",
        "Luboš", "Martina", "Drahomíra", "Čeněk", "Ilja", "Vítězslav",
        "Magdaléna", "Libor", "Kristýna", "Jakub", "Anna", "Věroslav",
        "Viktor", "Marta", "Bořivoj", "Ignác"
    ])
    # srpen
    globals.mesice.append([
        "Oskar", "Gustav", "Miluše", "Dominik", "Kristián", "Oldřiška", "Lada",
        "Soběslav", "Roman", "Vavřinec", "Zuzana", "Klára", "Alena", "Alan",
        "Hana", "Jáchym", "Petra", "Helena", "Ludvík", "Bernard", "Johana",
        "Bohuslav", "Sandra", "Bartoloměj", "Radim", "Luděk", "Otakar",
        "Augustýn", "Evelína", "Vladěna", "Pavlína"
    ])
    # září
    globals.mesice.append([
        "Linda, Samuel", "Adéla", "Bronislav", "Jindřiška", "Boris",
        "Boleslav", "Regína", "Mariana", "Daniela", "Irma", "Denisa", "Marie",
        "Lubor", "Radka", "Jolana", "Ludmila", "Naděžda", "Kryštof", "Zita",
        "Oleg", "Matouš", "Darina", "Berta", "Jaromír", "Zlata", "Andrea",
        "Jonáš", "Václav, Den české státnosti", "Michal", "Jeroným"
    ])
    # říjen
    globals.mesice.append([
        "Igor", "Olivie, Oliver", "Bohumil", "František", "Eliška", "Hanuš",
        "Justýna", "Věra", "Štefan, Sára", "Marina", "Andrej", "Marcel",
        "Renáta", "Agáta", "Tereza", "Havel", "Hedvika", "Lukáš", "Michaela",
        "Vendelín", "Brigita", "Sabina", "Teodor", "Nina", "Beáta", "Erik",
        "Šarlota, Zoe", "Den vzniku samostatného československého státu",
        "Silvie", "Tadeáš", "Štěpánka"
    ])
    # listopad
    globals.mesice.append([
        "Felix", "Památka zesnulých (dušičky)", "Hubert", "Karel", "Miriam",
        "Liběna", "Saskie", "Bohumír", "Bohdan", "Evžen", "Martin", "Benedikt",
        "Tibor", "Sáva", "Leopold", "Otmar",
        "Mahulena, Den boje za svobodu a demokracii", "Romana", "Alžběta",
        "Nikola", "Albert", "Cecílie", "Klement", "Emílie", "Kateřina",
        "Artur", "Xenie", "René", "Zina", "Ondřej"
    ])
    # prosinec
    globals.mesice.append([
        "Iva", "Blanka", "Svatoslav", "Barbora", "Jitka", "Mikuláš",
        "Benjamín", "Květoslava", "Vratislav", "Julie", "Dana", "Simona",
        "Lucie", "Lýdie", "Radana", "Albína", "Daniel", "Miloslav", "Ester",
        "Dagmar", "Natálie", "Šimon", "Vlasta", "Adam, Eva, Štědrý den",
        "1. svátek vánoční", "Štěpán, 2. svátek vánoční", "Žaneta", "Bohumila",
        "Judita", "David", "Silvestr"
    ])
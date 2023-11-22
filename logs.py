# ---------- #
# ----------
#   LOGS.PY
# ----------   
#   Logging module
# ---------- #
 
import globals
from datetime import datetime

# log user messages (if enabled)
def user_message(channel, author, text):
    if not globals.MESSAGE_LOGGING_ENABLED:
        return
    
    timedata = datetime.now(globals.timezone)
    log_time = timedata.strftime("%d/%m/%Y %H:%M.%S")
    with open(globals.msg_logs_file_path, 'a') as logfile:
        logfile.write("[" + log_time + "] [#" + channel + "] " + author + " <<'" + text + "'>>\n")

# info log
def info(description, topic=None):
    log('I', description, topic)

# warning log
def warning(description, topic=None):
    log('W', description, topic)

# error log
def error(description, topic=None):
    log('E', description, topic)

# exception log
def exception(description, topic=None):
    log('EX', description, topic)

# standard log message, saved into logfile and printed to console
def log(type, description, topic=None):
    if type == 'E':
        type = 'ERROR'
    elif type == 'I':
        type = 'INFO'
    elif type == 'W':
        type = 'WARNING'
    elif type == 'EX':
        type = 'EXCEPTION'
    else:
        type = '?'

    if topic:
        topic = str.upper(topic)
        save_print('[' + type + ':' + topic + '] ' + str(description))
    else:    
        save_print('[' + type + '] ' + str(description))

# save log into logfile
def save(text):
    if globals.DB_RECOVERY_RUNNING:
        return
    
    timedata = datetime.now(globals.timezone)
    log_time = timedata.strftime("%d/%m/%Y %H:%M.%S")
    with open(globals.log_file_path, 'a') as logfile:
        logfile.write("[" + log_time + "]: " + text + "\n")

# print and save log
def save_print(text):
    print(text)
    save(text)
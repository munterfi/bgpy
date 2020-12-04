from datetime import datetime
from os import getpid

LOG_FILE = "bgp.log"

def clear_log(log_file):
    open(log_file, 'w').close()

def write_log(log_file, message):
    with open(log_file, 'a') as log:
        log.write(f'{datetime.now().replace(microsecond=0)} - {getpid()}: {message}\n')

from log import write_log, clear_log, LOG_FILE
from time import sleep
from subprocess import Popen
from sys import  executable

clear_log(LOG_FILE)
write_log(LOG_FILE, "Main process: Started")

#sleep(1)
#Popen([executable, "background_plain.py"])
#sleep(1)
#Popen([executable, "background_graceful.py"])
#sleep(0.5)
#Popen([executable, "background_threading.py"])
#sleep(0.5)

sleep(1)
Popen([executable, "background_worker.py"])

write_log(LOG_FILE, "Main process: Ended normally")



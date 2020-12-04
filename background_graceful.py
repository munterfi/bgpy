from log import write_log, LOG_FILE
from time import sleep
import signal

write_log(LOG_FILE, "Background process: Graceful started")

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True

killer = GracefulKiller()
i = 0
while not killer.kill_now:
    sleep(2)
    write_log(LOG_FILE, f"Background process: Graceful iteration {i}")
    i = i + 1

write_log(LOG_FILE, "Background process: Graceful ended normally")



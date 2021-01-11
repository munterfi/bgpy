from pathlib import Path


BG_HOME = Path("bgpy")
BG_HOME.mkdir(parents=True, exist_ok=True)
BG_LOG_FILE = BG_HOME / "bgpy.log"

BG_HOST = "127.0.0.1"  # IP adress of the Server
BG_PORT = 5001  # Port used by server
BG_MSG_LEN = 4096 * 4
BG_BACKLOG = 0

# INIT : Pass function (fun_init, fun_exec, func_exit) and execcute fun_init
# EXEC : Execute fun_exec
# EXIT : Execute fun_exit

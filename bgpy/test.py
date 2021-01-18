from interface import initialize, execute, terminate
from tasks import init_task, exec_task, exit_task


# Start background process
initialize(init_task, exec_task, exit_task)

# Increase value
execute({"command": "increase", "value_change": 10})

# Decrease value
execute({"command": "decrease", "value_change": 100})

# Terminate
args = terminate(await_response=True)
print(args)

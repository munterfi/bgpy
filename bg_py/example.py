from communication import receive_command, send_response, Message
from log import write_log
from environment import BG_INTERVAL
from threading import Event

example_init_args = {"count_start": 100, "name": "Hello world!"}


def example_background_loop(exit: Event, init_args: dict) -> Message:
    # init_args = {"count_start": 100, "name": "Hello world!"}
    # Namespace of parent: BG_INTERVAL, receive_command, send_response, write_log

    # Perform setup task
    i = init_args["count_start"]
    write_log(f"Background process: Got an important setup message! {init_args['name']}")

    # Enter the background loop
    while not exit.is_set():

        # Sleep
        exit.wait(BG_INTERVAL)

        # Increment iteration
        i = i + 1
        write_log(f"Background process: Iteration {i}")

        # Listen to commands and skip if None
        command = receive_command()
        if command is None:
            continue

        # Check for commands and exit loop
        if command in [Message.EXIT, Message.KILL]:
            break
        
        # Receive execute commands excure respond (important)
        if command is Message.EXECUTE:
            send_response(Message.OK.set_args({"Response": f"{command.name} OK"}))
            write_log(f"Received command: {command.name} with arguments '{command.args_to_json()}'")

    # Perform any cleanup here
    write_log(f"Background process: Userdefined cleanup")
    
    # Return exit command (only EXIT and KILL are handled)
    return command
from modules.listener import listen
from modules.commands import handle_command

def main():
    print("Orbit Assistant is online.")
    while True:
        command = listen()
        handle_command(command)

main()
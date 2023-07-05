from terminal import Terminal

def main():
    terminal = Terminal()
    print(' -----------------------------------------------------------------------------------------')
    print("|                                Welcome to Linux Emulator                                 |")
    print(' -----------------------------------------------------------------------------------------')
    print("| . Now you are in the regular mode.                                                      |")
    print("| . If you want to start the exam, please choose the exam mode by typing just 'exam'      |")
    print("| . You can terminate the exam mode and return to the regular interface by entering 'exit'|")
    print("| . To exit the terminal,  type 'exit'                                                    |")
    print(' -----------------------------------------------------------------------------------------')
    print('                                                                                ©riasagman')
    while True:

        command = input(f"{terminal.owner}@Picsart-Academy ~ $ ")
        continue_loop = terminal.run_command(command)
        if not continue_loop:
            break
if __name__ == "__main__":
    main()

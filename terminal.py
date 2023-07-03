import datetime
import re
import getpass
import calendar
from directory import Directory, File, SymbolicLink

class Terminal:
    def __init__(self, owner=input("Enter your username: ")):
        self.owner = owner
        self.root_directory = Directory("/", None)
        self.current_directory = self.root_directory
        self.opened_files = {}
        self.connected_server = False
        self.server_ip = '192.168.1.2'
        self.server_username = 'test'
        self.server_password = '1111'
        self.ssh_command_used = False


    def run_command(self, command):
        command_parts = command.split()
        if not command_parts:
            pass
        elif command_parts[0] == 'done':
            pass
        elif command_parts[0] == "ls":
            if len(command_parts) > 1:
                if command_parts[1] == "-l":
                    self.ls(option="-l")
                else:
                    self.ls(command_parts[1])
            else:
                self.ls()
        elif command_parts[0] == "cd":
            if len(command_parts) > 1:
                self.cd(command_parts[1])
            else:
                self.cd()
        elif command == "clear":
            self.clear()
        elif command_parts[0] == "rmdir":
            if len(command_parts) < 2:
                print("Invalid command.")
            else:
                directory_name = command_parts[1]
                self.rmdir(directory_name)
        elif command_parts[0] == "pwd":
            self.pwd()
        elif command_parts[0] == "echo":
            if len(command_parts) > 1:
                message = " ".join(command_parts[1:])
                print(message)
            else:
                print()
        elif command_parts[0] == "mkdir":
            if len(command_parts) > 1:
                directories = " ".join(command_parts[1:])
                self.mkdir(directories)
        elif command_parts[0] == "touch":
            if len(command_parts) > 1:
                self.touch(command_parts[1])
        elif command_parts[0] == "vim":
            if len(command_parts) > 1:
                self.vim(command_parts[1])
        elif command_parts[0] == "chmod":
            if len(command_parts) > 2:
                self.chmod(command_parts[1], command_parts[2])
            else:
                print("Invalid command. Usage: chmod <mode> <item>")
        elif command_parts[0] == "connect":
            if len(command_parts) > 1:
                self.connect_to_server(command_parts[1])
        elif command_parts[0] == "cat":
            if len(command_parts) > 1:
                self.cat_file(command_parts[1])
        elif command_parts[0] == "sort":
            if len(command_parts) > 1:
                self.sort_file(command_parts[1])
        elif command_parts[0] == "exam":
            self.conduct_exam()
        elif command_parts[0] == "uniq":
            if len(command_parts) > 1:    
                self.uniq_file(command_parts[1])
        elif command_parts[0] == "grep":
            if len(command_parts) > 1:    
                self.grep_file(command_parts[1])
        elif command_parts[0] == "wc":
            if len(command_parts) > 1:
                self.word_count(command_parts[1])
        elif command_parts[0] == "head":
            if len(command_parts) > 1:
                self.head_file(command_parts[1])
        elif command_parts[0] == "tail":
            if len(command_parts) > 1:
                self.tail_file(command_parts[1])
        elif command_parts[0] == "tee" or command_parts[0] == ">":
            if len(command_parts) > 1:
                self.tee_file(command_parts[1])
        elif command_parts[0] == "cp":
            if len(command_parts) > 1:
                self.copy_file(command_parts[1])
        elif command_parts[0] == "cal":
            self.cal()
        elif command_parts[0] == "date":
            self.date()
        elif command_parts[0] == "man":
            if len(command_parts) > 1:
                self.man(command_parts[1])
            else:
                print("Usage: man [COMMAND]")
        elif command_parts[0] == "whoami":
            self.whoami()
        elif command_parts[0] == "mv":
            if len(command_parts) < 3:
                print("Invalid command.")
                return True
            source_path = command_parts[1]
            target_path = command_parts[2]
            self.mv(source_path, target_path)
        elif command_parts[0] == "ssh":
            self.ssh_command_used = self.check_ssh_command(command)

            if len(command_parts) != 2:
                print("Invalid ssh command. Usage: ssh serverusername@ipaddress")
            else:
                server_info = command_parts[1]
                if "@" not in server_info:
                    print("Invalid ssh command. Usage: ssh serverusername@ipaddress")
                else:
                    server_username, server_address = server_info.split("@", 1)
                    server_password = getpass.getpass("Enter password: ")
                    self.ssh(server_address, server_username, server_password)
        elif command_parts[0] == "rm":
            if len(command_parts) > 1:
                if command_parts[1] == "-r" or command_parts[1] == "-rf":
                    self.rm_recursive(command_parts[2])
                else:
                    self.rm(command_parts[1])
            else:
                print("Invalid command.")
        elif command_parts[0] == "ln":
            if len(command_parts) < 3:
                print("Invalid command.")
                return True

            source_path = command_parts[1]
            target_path = command_parts[2]

            if len(command_parts) > 3 and command_parts[3] == "-s":
                self.ln(source_path, target_path, symbolic=True)
            else:
                self.ln(source_path, target_path)

        elif command_parts[0] == "exit":
            print("")
            return False
        else:
            print("Command not found.")
        return True

    def pwd(self):
        path = self.get_current_directory_path()
        print('/'+path)

    def get_current_directory_path(self):
        path = ""
        current_directory = self.current_directory
        while current_directory:
            path = '/' + current_directory.name + path
            current_directory = current_directory.parent
        return path.lstrip('/')
    
    def whoami(self):
        print(self.owner)

    def ls(self, path=None, option=None):
        if path is None or path == "":
            directories = self.current_directory.subdirectories
            files = self.current_directory.files
        elif path.startswith("./"):
            path = path[2:]
            directories, files = self.get_directories_and_files_in_path(path)
            if directories is None or files is None:
                return
            directories = [directories[-1]] if directories else []
            files = []
        else:
            directories, files = self.get_directories_and_files_in_path(path)
            if directories is None or files is None:
                return

        for directory in directories:
            if option == "-l":
                creation_date = directory.creation_date
                permissions = directory.permissions  
                print(f"d{permissions}\t{self.owner}\t{creation_date}\t{directory.name}/")
            else:
                print(directory.name + "/")

        for file in files:
            if option == "-l":
                creation_date = file.creation_date
                permissions = file.permissions  
                print(f"-{permissions}\t{self.owner}\t{creation_date}\t{file.name}")
            else:
                print(file.name)
                
    def clear(self):
        print("\033[2J\033[H", end='')


    def cd(self, directory=None):
        if directory is None or directory == "":
            self.current_directory = self.root_directory
        elif directory == "..":
            if self.current_directory.parent:
                self.current_directory = self.current_directory.parent
        elif directory == "./":
            return
        elif directory.startswith("./"):
            directory = directory[2:]
            self.cd(directory)
        elif directory.startswith("../"):
            path_parts = directory.split("/")
            for part in path_parts:
                if part == "..":
                    if self.current_directory.parent:
                        self.current_directory = self.current_directory.parent
                else:
                    for subdirectory in self.current_directory.subdirectories:
                        if subdirectory.name == part:
                            self.current_directory = subdirectory
                            break
                    else:
                        return
        else:
            path_parts = directory.split("/")
            for part in path_parts:
                for subdirectory in self.current_directory.subdirectories:
                    if subdirectory.name == part:
                        self.current_directory = subdirectory
                        break
                else:
                    return

    def cal(self):
        now = datetime.datetime.now()
        month = now.month
        year = now.year
        cal_output = calendar.month(year, month)
        print(cal_output)

    def date(self):
        now = datetime.datetime.now()
        print(now.strftime("%a %b %d %H:%M:%S %Z %Y"))

    def man(self, command):
        if command == "pwd":
            print("pwd - Print the current working directory.")
            print("Usage: pwd")
        elif command == "ls":
            print("ls - List directory contents.")
            print("Usage: ls [OPTION] [PATH]")
            print("")
            print("Options:")
            print("-l    Use a long listing format to display additional details.")
            print("")
            print("Arguments:")
            print("PATH  Optional. The path to the directory for which to list contents. If not provided, the current directory is used.")
        elif command == "cd":
            print("cd - Change the current working directory.")
            print("Usage: cd [DIRECTORY]")
            print()
            print("If no DIRECTORY is provided, it changes the current directory to the root directory.")
            print("If DIRECTORY is '..', it changes the current directory to its parent directory.")
            print("If DIRECTORY is './', it does nothing.")
            print("If DIRECTORY starts with './', it changes the current directory to the specified subdirectory.")
            print("If DIRECTORY starts with '../', it changes the current directory to the parent directory and then to the specified subdirectory.")
            print("Otherwise, it tries to find the specified subdirectory within the current directory and changes to it if found.")
            print("If the specified subdirectory is not found, it prints 'Directory not found.'")
        elif command == "mkdir":
            print("mkdir - Create a new directory.")
            print("Usage: mkdir DIRECTORY")
            print()
            print("Creates a new directory with the specified name in the current directory.")
            print("If a directory with the same name already exists, an error message is displayed.")
            print("The directory's permissions are set to 'rwxr-xr-x', and the creation date is recorded.")
        elif command == "touch":
            print("touch - Create a new file.")
            print("Usage: touch FILENAME")
            print()
            print("Creates a new file with the specified name in the current directory.")
            print("If a file with the same name already exists, an error message is displayed.")
            print("The file's permissions are set to '-rw-r--r--', and the creation date is recorded.")
        elif command == "echo":
            print("echo - Display a line of text")
            print("Usage: echo [MESSAGE]")
            print()
            print("Description:")
            print("The echo command is used to display a line of text on the terminal.")
            print("It takes a MESSAGE argument which is the text to be displayed.")
        elif command == "whoami":
            print("whoami - Print the current user.")
            print("Usage: whoami")
        elif command == "clear":
            print("clear - Clear the terminal screen.")
            print("Usage: clear")
            print()
            print("Clears the contents of the terminal screen and moves the cursor to the top-left corner.")
            print("This provides a clean slate for displaying new output and improves readability.")
        elif command == "cal":
            print("cal - Display a calendar for the current month.")
            print("Usage: cal")
            print()
            print("Displays a calendar for the current month and year.")
            print("The calendar is printed using the calendar module's 'month' function.")
        elif command == "date":
            print("date - Display the current date and time.")
            print("Usage: date")
            print()
            print("Displays the current date and time in the format: 'Day Month DayOfMonth Hour:Minute:Second Timezone Year'.")
            print("The current date and time are obtained using the datetime module's 'now' function and formatted using 'strftime'.")
        elif command == "vim":
            print("vim - Text editor for modifying files.")
            print("Usage: vim FILENAME")
            print()
            print("Opens the specified file in the Vim text editor for modification.")
            print("If the file exists, Vim is launched, and the contents of the file are displayed.")
            print("Use 'exit' to return to the terminal. Changes made in Vim are saved.")
            print("If the file does not exist, it will be created")
        elif command == "chmod":
            print("chmod - Change permissions of a file or directory.")
            print("Usage: chmod MODE FILENAME")
            print()
            print("Changes the permissions of the specified file or directory.")
            print("MODE must be a valid octal value representing the new permissions.")
            print("If the file or directory exists, its permissions are updated accordingly.")
            print("If the file or directory does not exist, a 'File not found' error message is displayed.")
        elif command == "mv":
            print("mv - Move or rename a file or directory.")
            print("Usage: mv SOURCE_PATH TARGET_PATH")
            print()
            print("Moves or renames the file or directory at SOURCE_PATH to the location specified by TARGET_PATH.")
            print("If the SOURCE_PATH is a file, it is moved or renamed accordingly.")
            print("If the SOURCE_PATH is a directory, it is moved or renamed along with its contents.")
            print("If the TARGET_PATH is an existing directory, the item is moved to that directory.")
            print("If the TARGET_PATH is a new name, the item is renamed accordingly.")
            print("If the SOURCE_PATH or TARGET_PATH does not exist, a 'Source item not found' or 'Target directory not found' error message is displayed, respectively.")
        elif command == "rm":
            print("rm - Remove a file or directory.")
            print("Usage: rm [-r|-rf] ITEM_NAME")
            print()
            print("Removes the file or directory with the specified ITEM_NAME.")
            print("If the ITEM_NAME is a file, it is removed from the current directory.")
            print("If the ITEM_NAME is a directory, the '-r' or '-rf' option can be used to remove the directory and its contents recursively.")
            print("Options:")
            print("  -r       Remove directories and their contents recursively.")
            print("  -rf      Remove directories and their contents forcefully without confirmation.")
            print("If the ITEM_NAME does not exist, a 'Item not found' error message is displayed.")
        elif command == "rmdir":
            print("rmdir - Remove an empty directory.")
            print("Usage: rmdir DIRECTORY_NAME")
            print()
            print("Removes the empty directory with the specified DIRECTORY_NAME.")
            print("The DIRECTORY_NAME must be an empty directory; otherwise, an error message will be displayed.")
            print("If the specified directory is successfully removed, a success message will be displayed.")
            print("If the DIRECTORY_NAME does not exist or is not an empty directory, an appropriate error message will be displayed.")
        elif command == "ln":
            print("ln - Create a link to a file or directory.")
            print("Usage: ln [-s] SOURCE_PATH TARGET_PATH")
            print()
            print("Creates a link to the file or directory at SOURCE_PATH in the current directory.")
            print("The link is created at TARGET_PATH.")
            print("Options:")
            print("  -s       Create a symbolic link instead of a hard link.")
            print("If the SOURCE_PATH does not exist, a 'Source item not found' error message is displayed.")
            print("If the SOURCE_PATH is a directory, a 'ln: SOURCE_PATH: Is a directory' error message is displayed.")
            print("If the TARGET_PATH is not a directory or does not exist, a 'Target directory not found' error message is displayed.")
        elif command == "ssh":
            print("ssh - Connect to a remote server via SSH.")
            print("Usage: ssh SERVER_ADDRESS SERVER_USERNAME SERVER_PASSWORD")
            print()
            print("Connects to the remote server specified by SERVER_ADDRESS using the SSH protocol.")
            print("The connection is authenticated using the username and password specified by SERVER_USERNAME and SERVER_PASSWORD, respectively.")
            print("If the connection is successful, a new SSH session is established.")
            print("Commands can be executed on the remote server within the SSH session.")
            print("After executing the commands, the SSH session is closed and the connection to the remote server is terminated.")
            print("If the connection is already established, a 'Already connected to a server' error message is displayed.")
            print("If any of the authentication parameters (SERVER_ADDRESS, SERVER_USERNAME, SERVER_PASSWORD) are incorrect, a 'Cannot connect to a server. Incorrect <parameter>' error message is displayed.")
        elif command == "cat":
            print("cat - Display the contents of a file.")
            print("Usage: cat FILE_NAME")
            print()
            print("Displays the contents of the file with the specified FILE_NAME.")
            print("If the file is found in the current directory, its contents are printed.")
            print("If the file is not found, a 'File 'FILE_NAME' not found.' error message is displayed.")
        elif command == "sort":
            print("sort - Sort the lines of a file.")
            print("Usage: sort FILE_NAME")
            print()
            print("Sorts the lines of the file with the specified FILE_NAME in lexicographic order.")
            print("If the file is found in the current directory, its contents are sorted and updated.")
            print("If the file is not found, a 'File 'FILE_NAME' not found.' error message is displayed.")
        elif command == "uniq":
            print("uniq - Remove duplicate lines from a file.")
            print("Usage: uniq FILE_NAME")
            print()
            print("Removes duplicate lines from the file with the specified FILE_NAME.")
            print("If the file is found in the current directory, its contents are updated to contain only unique lines.")
            print("If the file is not found, a 'File 'FILE_NAME' not found.' error message is displayed.")
        elif command == "grep":
            print("grep - Search for a pattern in files.")
            print("Usage: grep PATTERN")
            print()
            print("Searches for the specified PATTERN in the contents of files in the current directory.")
            print("Prints the lines in the files that contain the matching pattern.")
            print("If no matching lines are found, a 'No matching lines found' message is displayed.")
        elif command == "wc":
            print("wc - Count the number of lines, words, and characters in a file.")
            print("Usage: wc FILE_NAME")
            print()
            print("Counts the number of lines, words, and characters in the specified FILE_NAME.")
            print("Prints the line count, word count, and character count.")
            print("If the file is not found, a 'File FILE_NAME not found' message is displayed.")
        elif command == "head":
            print("head - Display the first few lines of a file.")
            print("Usage: head FILE_NAME [NUM_LINES]")
            print()
            print("Displays the first few lines of the specified FILE_NAME.")
            print("By default, the first 10 lines are displayed.")
            print("The optional NUM_LINES argument can be used to specify the number of lines to display.")
            print("If the file is not found, a 'File FILE_NAME not found' message is displayed.")
        elif command == "tail":
            print("tail - Display the last few lines of a file.")
            print("Usage: tail FILE_NAME [NUM_LINES]")
            print()
            print("Displays the last few lines of the specified FILE_NAME.")
            print("By default, the last 10 lines are displayed.")
            print("The optional NUM_LINES argument can be used to specify the number of lines to display.")
            print("If the file is not found, a 'File FILE_NAME not found' message is displayed.")
        elif command == "tee":
            print("tee - Append content to a file.")
            print("Usage: tee FILE_NAME")
            print()
            print("Reads input from the user and appends it to the specified FILE_NAME.")
            print("The user can enter multiple lines of content, which are appended to the file.")
            print("Press Ctrl + D to finish entering content.")
            print("If the file is not found, a 'File FILE_NAME not found' message is displayed.")
        elif command == "cp":
            print("cp - Create a copy of a file.")
            print("Usage: cp FILE_NAME")
            print()
            print("Creates a copy of the specified FILE_NAME with the prefix 'copy_' added to the copy's name.")
            print("The contents of the original file are copied to the new file.")
            print("If the file is not found, a 'File FILE_NAME not found' message is displayed.")
        else:
            print("Command not found.")

    def get_directories_and_files_in_path(self, path):
        directories = []
        files = []
        current_directory = self.current_directory

        if path == "..":
            if current_directory.parent is not None:
                current_directory = current_directory.parent
        elif path != ".":
            path_parts = path.split("/")
            for part in path_parts:
                found = False
                for directory in current_directory.subdirectories:
                    if directory.name == part:
                        current_directory = directory
                        found = True
                        break
                if not found:
                    return None, None

        directories = current_directory.subdirectories
        files = current_directory.files

        return directories, files

    def mkdir(self, directories):
        dir_names = directories.split()
        for dir_name in dir_names:
            if dir_name.startswith('./'):
                dir_name = dir_name[2:]  
            if dir_name.endswith('/'):
                dir_name = dir_name[:-1]  

            nested_dirs = dir_name.split('/')

            current_directory = self.current_directory
            for nested_dir in nested_dirs:
                for subdirectory in current_directory.subdirectories:
                    if subdirectory.name == nested_dir:
                        current_directory = subdirectory
                        break
                else:
                    new_directory = Directory(nested_dir, current_directory)
                    now = datetime.datetime.now()
                    new_directory.creation_date = now.strftime("%b %d %H:%M")
                    new_directory.permissions = "rwxr-xr-x"  
                    a = new_directory.permissions
                    current_directory.add_subdirectory(new_directory)
                    print(f"Directory '{nested_dir}' created. Permissions: d{a}, Creation Date: {new_directory.creation_date}")

                    current_directory = new_directory


    def touch(self, filename):
        file_exists = False

        for file in self.current_directory.files:
            if file.name == filename:
                file_exists = True
                break

        if file_exists:
            print("File already exists.")
        else:
            directory_path, file_name = self.split_directory_path(filename)
            target_directory = self.current_directory

            if directory_path:
                target_directory = self.traverse_directory_path(directory_path)

                if not target_directory:
                    print("Invalid directory path.")
                    return

            if isinstance(target_directory, File):
                print("Cannot create file inside a file.")
                return

            new_file = File(file_name)
            target_directory.add_file(new_file)
            now = datetime.datetime.now()
            new_file.creation_date = now.strftime("%b %d %H:%M")
            new_file.permissions = "rw-r--r--"  
            a = new_file.permissions
            print(f"File created. Permissions: -{a}, Creation Date: {new_file.creation_date}")

    def split_directory_path(self, path):
        """Split the directory path into the directory and file name."""
        parts = path.split("/")
        directory = "/".join(parts[:-1])
        file_name = parts[-1]
        return directory, file_name

    def traverse_directory_path(self, path):
        """Traverse the directory path and return the target directory."""
        current_directory = self.current_directory

        for directory_name in path.split("/"):
            if directory_name == "..":
                if current_directory.parent:
                    current_directory = current_directory.parent
                else:
                    return None
            else:
                for subdirectory in current_directory.subdirectories:
                    if subdirectory.name == directory_name:
                        current_directory = subdirectory
                        break
                else:
                    return None

        return current_directory

    def vim(self, filename):
        for file in self.current_directory.files:
            if file.name == filename:
                if filename in self.opened_files:
                    print("Resuming Vim. Use ':wq' to return to the terminal.")
                    print("".join(self.opened_files[filename].contents))
                    while True:
                        line = input()
                        if line == ":wq":
                            break
                        self.opened_files[filename].append(line + "\n")
                else:
                    print("Entering Vim. Use ':wq' to return to the terminal.")
                    print("".join(file.contents))
                    while True:
                        line = input()
                        if line == ":wq":
                            break
                        file.append(line + "\n")
                    self.opened_files[filename] = file
                break
        else:
            new_file = File(filename, self.current_directory)
            self.current_directory.add_file(new_file)
            print(f"Entering Vim. Use ':wq' to return to the terminal.")
            while True:
                line = input()
                if line == ":wq":
                    break
                new_file.append(line + "\n")
            self.opened_files[filename] = new_file

    def chmod(self, mode, filename):
        file = self.find_item_in_current_directory(filename)
        if file is None:
            print("File not found.")
            return

        if isinstance(file, File):
            permissions = file.permissions  
        elif isinstance(file, Directory):
            permissions = file.permissions  
        else:
            print("Invalid file or directory.")
            return

        if re.match(r"^[0-7]{3}$", mode):
            new_permissions = self.apply_octal_mode(permissions, mode)
            if new_permissions is not None:
                if isinstance(file, File):
                    file.permissions = new_permissions  
                    print(f"Permissions updated: -{file.permissions}")
                elif isinstance(file, Directory):
                    file.permissions = new_permissions  
                    print(f"Permissions updated: d{file.permissions}")
            else:
                print("Invalid octal mode.")
        else:
            print("Invalid mode.")

    def apply_octal_mode(self, permissions, mode):
        user_mode = mode[0]
        group_mode = mode[1]
        other_mode = mode[2]

        permission_map = {
            "0": "---",
            "1": "--x",
            "2": "-w-",
            "3": "-wx",
            "4": "r--",
            "5": "r-x",
            "6": "rw-",
            "7": "rwx",
        }

        if (
            user_mode not in permission_map
            or group_mode not in permission_map
            or other_mode not in permission_map
        ):
            print("Invalid octal mode.")
            return None

        new_permissions = ""
        for digit in mode:
            new_permissions += permission_map[digit]

        return new_permissions

    def find_item_in_current_directory(self, name):
        for item in self.current_directory.subdirectories + self.current_directory.files:
            if item.name == name:
                return item
        return None
    
    def find_item_in_directory(self, directory, name):
        for item in directory.subdirectories + directory.files:
            if item.name == name:
                return item
        return None

    def connect_to_server(self, server_ip):
        if self.server_connected:
            print("Already connected to a server.")
            return
        if not re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", server_ip):
            print("Invalid server IP address.")
            return
        self.server_connected = True
        self.server_ip = server_ip
        print(f"Connected to server at {server_ip}.")

    def cat_file(self, file_name):
        for file in self.current_directory.files:
            if file.name == file_name:
                print(file.contents)
                return
        print(f"File '{file_name}' not found.")

    def sort_file(self, file_name):
        for file in self.current_directory.files:
            if file.name == file_name:
                lines = file.contents.split("\n")
                sorted_lines = sorted(lines)
                sorted_content = "\n".join(sorted_lines)
                file.contents = sorted_content
                print(f"Sorted contents of '{file_name}'.")
                return
        print(f"File '{file_name}' not found.")

    def uniq_file(self, file_name):
        for file in self.current_directory.files:
            if file.name == file_name:
                lines = file.contents.split("\n")
                unique_lines = list(set(lines))
                unique_content = "\n".join(unique_lines)
                file.contents = unique_content
                print(f"Removed duplicate lines from '{file_name}'.")
                return
        print(f"File '{file_name}' not found.")

    def grep_file(self, pattern):
        for file in self.current_directory.files:
            lines = file.contents.split("\n")
            matched_lines = [line for line in lines if pattern in line]
            matched_content = "\n".join(matched_lines)
            if matched_content:
                print(f"Matching lines in '{file.name}':")
                print(matched_content)
                return
        print("No matching lines found.")

    def word_count(self, file_name):
        for file in self.current_directory.files:
            if file.name == file_name:
                lines = file.contents.split("\n")
                line_count = len(lines)
                word_count = sum(len(line.split()) for line in lines)
                character_count = sum(len(line) for line in lines)
                print(f"Lines: {line_count}")
                print(f"Words: {word_count}")
                print(f"Characters: {character_count}")
                return
        print(f"File '{file_name}' not found.")

    def head_file(self, file_name, num_lines=10):
        for file in self.current_directory.files:
            if file.name == file_name:
                lines = file.contents.split("\n")
                head_lines = lines[:num_lines]
                head_content = "\n".join(head_lines)
                print(f"Head of '{file_name}':")
                print(head_content)
                return
        print(f"File '{file_name}' not found.")

    def tail_file(self, file_name, num_lines=10):
        for file in self.current_directory.files:
            if file.name == file_name:
                lines = file.contents.split("\n")
                tail_lines = lines[-num_lines:]
                tail_content = "\n".join(tail_lines)
                print(f"Tail of '{file_name}':")
                print(tail_content)
                return
        print(f"File '{file_name}' not found.")

    def tee_file(self, file_name):
        for file in self.current_directory.files:
            if file.name == file_name:
                print("Enter content to append (press Ctrl + D to finish):")
                content = []
                while True:
                    try:
                        line = input()
                        content.append(line)
                    except EOFError:
                        break
                file.contents += "\n".join(content)
                print(f"Appended content to '{file_name}'.")
                return
        print(f"File '{file_name}' not found.")

    def copy_file(self, file_name):
        for file in self.current_directory.files:
            if file.name == file_name:
                copy_name = f"copy_{file_name}"
                copy = File(copy_name)
                copy.contents = file.contents
                self.current_directory.add_file(copy)
                print(f"Copied '{file_name}' as '{copy_name}'.")
                return
        print(f"File '{file_name}' not found.")

    def echo(self, message):
        print(message)

    def find_item_by_path(self, path):
        if path.startswith("/"):
            current_directory = self.root_directory
            path_parts = path.split("/")[1:]
        else:
            current_directory = self.current_directory
            path_parts = path.split("/")

        item = current_directory
        for part in path_parts:
            if isinstance(item, Directory):
                found = False
                for directory in item.subdirectories:
                    if directory.name == part:
                        item = directory
                        found = True
                        break
                if not found:
                    return None
            elif isinstance(item, SymbolicLink): 
                item = item.target
                continue
            else:
                return None

        return item

    def mv(self, source_path, target_path):
        source_item = self.find_item_in_current_directory(source_path)
        if source_item is None:
            print("Source item not found.")
            return
        target_directory = self.find_item_in_current_directory(target_path)
        if target_directory is None or not isinstance(target_directory, Directory):
            source_item.name = target_path
        else:
            if isinstance(source_item, File):
                self.current_directory.files.remove(source_item)
                target_directory.add_file(source_item)
            else:
                source_item.parent.subdirectories.remove(source_item)
                target_directory.add_subdirectory(source_item)

            source_item.parent = target_directory


    def rm(self, item_name):
        item = self.find_item_in_current_directory(item_name)
        if item is None:
            print("Item not found.")
            return
        if isinstance(item, File):
            if item.name == item_name:
                self.current_directory.files.remove(item)
                item.contents = ''
                print(f"Removed '{item_name}'.")
        elif isinstance(item, Directory):
            print(f"rm: {item_name}: is a directory")
        else:
            print("Invalid file or directory.")

    def rm_recursive(self, item_name):
        item = self.find_item_in_current_directory(item_name)
        if item is None:
            return
        if isinstance(item, File):
            if item.name == item_name:
                try:
                    self.current_directory.files.remove(item)
                except ValueError:
                    pass
                print(f"Removed '{item_name}'.")
        elif isinstance(item, Directory):
            if item.name == item_name:
                try:
                    self.current_directory.subdirectories.remove(item)
                except ValueError:
                    pass
                print(f"Removed '{item_name}'.")
                print("Removing contents of directory...")
                for subdirectory in item.subdirectories:
                    self.rm_recursive(subdirectory.name)
                for file in item.files:
                    try:
                        self.current_directory.files.remove(file)
                        print(f"Removed '{file.name}' from '{item_name}'.")
                    except ValueError:
                        pass
        else:
            print("Invalid file or directory.")

    def rmdir(self, directory_name):
        directory = self.find_item_in_current_directory(directory_name)
        if directory is None:
            print("Directory not found.")
            return
        if not isinstance(directory, Directory):
            print(f"rmdir: {directory_name}: Not a directory")
            return
        if directory.subdirectories or directory.files:
            print(f"rmdir: {directory_name}: Directory not empty")
            return
        self.current_directory.subdirectories.remove(directory)
        print(f"Directory '{directory_name}' removed.")

    def ln(self, source_path, target_path, symbolic=False):
        source_item = self.find_item_in_current_directory(source_path)
        if source_item is None:
            print("Source item not found.")
            return
        if isinstance(source_item, Directory):
            print(f"ln: {source_path}: Is a directory")
            return
        target_directory_name = target_path.split("/")[-1]
        target_directory = self.find_item_in_current_directory(target_directory_name)
        if target_directory is None or not isinstance(target_directory, Directory):
            print("Target directory not found.")
            return
        link_name = source_item.name
        if symbolic:
            link = SymbolicLink(link_name, source_item)
            target_directory.add_subdirectory(link)
            self.symbolic_links[link_name] = link
        else:
            link_file = File(link_name)
            link_file.contents = source_item.contents
            target_directory.add_file(link_file)

    def ssh(self, server_address, server_username, server_password):
        if self.connected_server:
            print("Already connected to a server.")
            return
        address = self.server_ip
        username = self.server_username
        password = self.server_password
        if server_username != username:
            print(("Cannot connect to a server. Incorrect username."))
            return
        elif server_password != password:
            print("Cannot connect to a server. Incorrect password.")
            return
        elif server_address != address:
            print(("Cannot connect to a server. Incorrect address."))
            return
        self.connected_server = SSHServer(address, username, password)
        self.connected_server.connect()
        self.connected_server.run_command_loop()
        self.connected_server.disconnect()
        self.connected_server = None

    def conduct_exam(self):
        questions = {
            '1': 'Question 1: Make a directory named "hello".',
            '2': 'Question 2: Create a file named "world.txt" inside the "hello" directory.',
            '3': 'Question 3: Change the permissions of the "world.txt" file to "-rwxrw-r--" using OCTAL mode.',
            '4': "Question 4: Open print working directory command's manual page, copy the output, and past that output inside world.txt file",
            '5': 'Question 5: Create a folder inside the "hello" folder and name it "folder1". Inside that folder, create a file named "file1.txt". Use a command to calculate the number of words, lines, and characters in the "world.txt" file. Then, within the "file1.txt" file, write ONLY the number of characters.',
            '6': 'Question 6: Change file1.txt  name to new_file.txt',
            '7': 'Question 7: Create a file named "root_file.txt" in the root directory, inside that file writ the command name with wich you can search for matching patterns in a file.Then move "root_file.txt" file inside the "hello" folder.',
            '8': 'Question 8: Create a hard link for the "root_file.txt" file inside the "folder1" folder.', 
            '9': 'Question 9: In the hello directory, create a folder named "home". Inside the "home" folder, create three folders named "dir1", "dir2", and "dir3". Additionally, create two files named "file1" and "file2" within the "home" folder. Then, remove the "hello" folder along with all its contents.', 
            '10':'Question 10: Connect to a server at 192.168.1.2 using the username "test" and password "1111". Create a folder named "user". After disconnecting, please remember to type "done" to see your grade.'
        }
        answers = {
            '1': '/hello',
            '2': '/hello/world.txt',
            '3': 'rwxrw-r--',
            '4': 'pwd - Print the current working directory.\nUsage: pwd',
            '5': '52',
            '6': '/hello/folder1/new_file.txt',
            '7': '/hello/root_file.txt',
            '8': '/hello/folder1/root_file.txt',
            '9': '/',
            '10': 'ssh test@192.168.1.2'

        }
        current_question_index = 1
        command = ''
        print('You got this! Crush that exam!')

        start_command = input("Type 'start' to begin the exam: ")
        if start_command.lower() == "start":
            print(' -----------------------------------------------------------------------------------------------------')
            print("|   If you have finished answering the question, please type 'done' to proceed to the next question.  |")
            print(' -----------------------------------------------------------------------------------------------------')

            question = questions.get(str(current_question_index))
            if question is not None:
                print()
                print(question)
                print()
            correct_answers = 0
            while True:
                command = input(f"{self.owner}MasterMode@Picsart-Academy ~ $ ")
                if command == 'done':
                    answer = answers.get(str(current_question_index))
                    if answer is not None and self.check_file_system(str(current_question_index), answer):
                        correct_answers += 1

                    current_question_index += 1
                    question = questions.get(str(current_question_index))
                    if question is not None:
                        print()
                        print(question)
                        print()
                    else:
                        break  
                self.run_command(command)
                if command == 'exit':
                    print("Exiting exam mode...")
                    break
            grade = f"{correct_answers}/{len(answers)}"
            print("Grade:", grade)
        else:
            print("Exam not started. Good luck!")

    def check_answers(self, answers):
        correct_answers = 0
        for question_index, answer in answers.items():
            if self.check_file_system(question_index, answer):
                correct_answers += 1
        return correct_answers

    def check_file_system(self, question_index, answer):
        root_directory = self.root_directory

        if question_index == '1':
            directory_name = answer.lstrip('/')
            for subdirectory in root_directory.subdirectories:
                if subdirectory.name == directory_name:
                    return True
            return False

        if question_index == '2':
            file_path = answer.lstrip('/')
            source_item = self.find_item_in_directory(root_directory, file_path)
            if source_item is None:
                return False
            if isinstance(source_item, File):
                return True
            return False

        if question_index == '3':
            source_item = self.find_item_in_directory(root_directory, 'hello/world.txt')
            if source_item is None:
                return False
            elif source_item.permissions == "rwxrw-r--":
                    return True
            return False
        if question_index == '4':
            source_item = self.find_item_in_directory(root_directory, 'hello/world.txt')
            if source_item is None:
                return False
            expected_contents = "pwd - Print the current working directory.\nUsage: pwd"
            if source_item.contents.strip() == expected_contents:
                return True
            return False
        if question_index == '5':
            source_item = self.find_item_in_directory(root_directory, 'hello/folder1/file1.txt')
            if source_item is None:
                return False
            expected_contents = "52"
            if source_item.contents.strip() == expected_contents:
                return True
            return False
        if question_index == '6':
            file_path = answer.lstrip('/')
            source_item = self.find_item_in_directory(root_directory, file_path)
            if source_item is None:
                return False
            if isinstance(source_item, File):
                new_file_path = 'hello/folder1/new_file.txt'
                new_file = self.find_item_in_directory(root_directory, new_file_path)
                if new_file is None:
                    return False
                expected_contents = "52"
                if new_file.contents.strip() == expected_contents:
                    return True
            return False
        if question_index == '7':
            file_path = answer.lstrip('/')
            source_item = self.find_item_in_directory(root_directory, file_path)
            if source_item is None:
                return False
            if isinstance(source_item, File):
                source_item_path = 'hello/root_file.txt'
                source_item = self.find_item_in_directory(root_directory, source_item_path)
                if source_item is None:
                    return False
                expected_contents = "grep"
                if source_item.contents.strip() == expected_contents:
                    return True
            return False
        if question_index =='8':
            file_path = answer.lstrip('/')
            source_item = self.find_item_in_directory(root_directory, file_path)
            if source_item is None:
                return False
            expected_contents = "grep"
            if source_item.contents.strip() == expected_contents: 
                if isinstance(source_item, File):
                    source_item_path = 'hello/root_file.txt'
                    source_item = self.find_item_in_directory(root_directory, source_item_path)
                    if source_item is None:
                        return False
                    expected_contents = "grep"
                    if source_item.contents.strip() == expected_contents:
                        return True
                return False
        if question_index == '9':
            source_item_path = 'hello'
            source_item = self.find_item_in_directory(root_directory, source_item_path)
            if source_item is None:
                return True
            return False
        if question_index == '10':
            return self.check_ssh_command()


    def find_item_in_directory(self, directory, path):
        path_parts = path.split("/")
        current_directory = directory

        for part in path_parts:
            if part == "..":
                if current_directory.parent:
                    current_directory = current_directory.parent
            else:
                found = False
                for subdirectory in current_directory.subdirectories:
                    if subdirectory.name == part:
                        current_directory = subdirectory
                        found = True
                        break
                if not found:
                    for file in current_directory.files:
                        if file.name == part:
                            return file
                    return None
        return current_directory
    
    def check_ssh_command(self, command=None):
        expected_command = "ssh test@192.168.1.2"
        return command == expected_command
    
class SSHServer(Terminal, File, Directory):
    def __init__(self, address, username, password):
        super().__init__()
        self.address = address
        self.username = username
        self.password = password

    def connect(self):
        
        print(f"Connecting to {self.address}...")
        self.connected = True
        print(f"Connected to {self.address}.")
    
    def disconnect(self):
        if self.connected:
            print(f"Disconnecting from {self.address}...")
            self.connected = False
            print(f"Disconnected from {self.address}.")
        else:
            print("Not connected to any server.")
    
    def run_command_loop(self):
        while True:
            command = input(f"{self.username}@{self.address}$ ")
            continue_loop = self.run_command(command)
            if not continue_loop:
                break

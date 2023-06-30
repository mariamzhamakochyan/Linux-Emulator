import datetime
import re
import getpass

class Directory:
    def __init__(self, name, parent=None, permissions = None):
        self.name = name
        self.parent = parent
        self.subdirectories = []
        self.files = []
        self.permissions = permissions

    def add_subdirectory(self, directory):
        self.subdirectories.append(directory)
        now = datetime.datetime.now()
        directory.creation_date = now.strftime("%b %d %H:%M")

    def add_file(self, file):
        self.files.append(file)

class File:
    def __init__(self, name, permissions = None):
        self.name = name
        self.contents = ""
        now = datetime.datetime.now()
        self.creation_date = now.strftime("%b %d %H:%M")
        self.permissions = permissions

    def append(self, content):
        self.contents += content

class Terminal:
    def __init__(self):
        self.root_directory = Directory("/", None)
        self.current_directory = self.root_directory
        self.opened_files = {}
        # self.server_connected = False
        # self.server_ip = '192.168.1.2'
        # self.server_username = 'test'
        # self.server_password = '1111'

    def run_command(self, command):
        
        command_parts = command.split()
        if command_parts[0] == "ls":
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
        elif command_parts[0] == "pwd":
            self.pwd()
        elif command_parts[0] == "mkdir":
            if len(command_parts) > 1:
                self.mkdir(command_parts[1])
        elif command_parts[0] == "touch":
            if len(command_parts) > 1:
                self.touch(command_parts[1])
        elif command_parts[0] == "vim":
            if len(command_parts) > 1:
                self.vim(command_parts[1])
        elif command_parts[0] == "chmod":
            if len(command_parts) > 2:
                self.chmod(command_parts[1], command_parts[2])
        elif command_parts[0] == "connect":
            if len(command_parts) > 1:
                self.connect_to_server(command_parts[1])
        elif command_parts[0] == "cat":
            if len(command_parts) > 1:
                self.cat_file(command_parts[1])
        elif command_parts[0] == "sort":
            if len(command_parts) > 1:
                self.sort_file(command_parts[1])
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
        elif command_parts[0] == "tee":
            if len(command_parts) > 1:
                self.tee_file(command_parts[1])
        elif command_parts[0] == "cp":
            if len(command_parts) > 1:
                self.copy_file(command_parts[1])
        elif command_parts[0] == "mv":
            if len(command_parts) > 1:
                self.move_file(command_parts[1])
        elif command_parts[0] == "rm":
            if len(command_parts) > 1:
                self.remove_file(command_parts[1])
        elif command_parts[0] == "ln":
            if len(command_parts) > 1:
                self.create_link(command_parts[1])
        elif command_parts[0] == "exit":
            print("Exiting terminal...")
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
                permissions = Directory.permissions 
                print(f"d{permissions}\t{owner}\t{creation_date}\t{directory.name}/")
            else:
                print(directory.name + "/")

        for file in files:
            if option == "-l":

                creation_date = file.creation_date  
                permissions = File.permissions
                print(f"-{permissions}\t{owner}\t{creation_date}\t{file.name}")
            else:
                print(file.name)



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
            self.cd("..")
            directory = directory[3:]
            self.cd(directory)
        else:
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
                        print("Directory not found.")
                        return

    def get_directories_and_files_in_path(self, path):
        directories = []
        files = []
        current_directory = self.current_directory

        if path == "/":
            return [self.root_directory], []

        path_parts = path.split("/")
        for part in path_parts:
            if part == "":
                continue

            found_directory = False
            for directory in current_directory.subdirectories:
                if directory.name == part:
                    current_directory = directory
                    directories.append(directory)
                    found_directory = True
                    break

            if not found_directory:
                return None, None

        files = current_directory.files

        return directories, files

    def mkdir(self, directory):
        for subdirectory in self.current_directory.subdirectories:
            if subdirectory.name == directory:
                print("Directory already exists.")
                break
        else:
            new_directory = Directory(directory, self.current_directory)
            now = datetime.datetime.now()
            new_directory.creation_date = now.strftime("%b %d %H:%M")
            Directory.permissions = "rwxr-xr-x"  
            a = Directory.permissions
            self.current_directory.add_subdirectory(new_directory)
            print(
                f"Directory created. Permissions: d{a}, Creation Date: {new_directory.creation_date}"
            )

    def touch(self, filename):
        for file in self.current_directory.files:
            if file.name == filename:
                print("File already exists.")
                break
        else:
            new_file = File(filename)
            self.current_directory.add_file(new_file)
            now = datetime.datetime.now()
            new_file.creation_date = now.strftime("%b %d %H:%M")
            File.permissions = '-rw-r--r--'  
            a = File.permissions
            print(f"File created. Permissions: {a}, Creation Date: {new_file.creation_date}")

    def vim(self, filename):
        for file in self.current_directory.files:
            if file.name == filename:
                if filename in self.opened_files:
                    print("Resuming Vim. Use 'exit' to return to the terminal.")
                    print("".join(self.opened_files[filename].contents))
                    while True:
                        line = input()
                        if line == "exit":
                            break
                        self.opened_files[filename].append(line + "\n")
                else:
                    print("Entering Vim. Use 'exit' to return to the terminal.")
                    print("".join(file.contents))
                    while True:
                        line = input()
                        if line == "exit":
                            break
                        file.append(line + "\n")
                    self.opened_files[filename] = file
                break
        else:
            print("File not found.")

    def chmod(self, mode, filename):
        file = self.find_file_in_current_directory(filename)
        if file is None:
            print("File not found.")
            return
        #etet file e uremn
        permissions = File.permissions
        # ete dir e uremn
        #permissions = Directory.permissions
        
        if re.match(r"^[0-7]{3}$", mode):
            new_permissions = self.apply_octal_mode(permissions, mode)
            if new_permissions is not None:
                #ete file a uremn es
                File.permissions = new_permissions
                print(f"Permissions updated: -{File.permissions}")
            else:
                print("Invalid octal mode.")
                # ete file che uremn stex

        else:
            new_permissions = self.apply_symbolic_mode(permissions, mode)
            if new_permissions is not None:
                File.permissions = new_permissions
                print(f"Permissions updated: {File.permissions}")
            else:
                print("Invalid mode.")

    def find_file_in_current_directory(self, filename):
        for file in self.current_directory.files:
            if file.name == filename:
                return file
        return None
        

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

    def apply_symbolic_mode(self, permissions, mode):
        operations = re.findall(r"[ugoa]*[-+=][rwx]+", mode)

        for operation in operations:
            target = operation[:-3] if operation[:-3] != "" else "a"
            operator = operation[-2]
            permissions_to_change = operation[-1]

            if target == "u":
                permission_set = permissions[:3]
            elif target == "g":
                permission_set = permissions[3:6]
            elif target == "o":
                permission_set = permissions[6:]
            else:
                permission_set = permissions

            new_permission_set = self.apply_operator(permission_set, operator, permissions_to_change)

            if new_permission_set is None:
                return None

            if target == "u":
                permissions = new_permission_set + permissions[3:]
            elif target == "g":
                permissions = permissions[:3] + new_permission_set + permissions[6:]
            elif target == "o":
                permissions = permissions[:6] + new_permission_set
            else:
                permissions = new_permission_set

        return permissions
    
    def apply_operator(self, permission_set, operator, permissions_to_change):
        operator_map = {
            "+": lambda a, b: a | b,
            "-": lambda a, b: a & ~b,
            "=": lambda a, b: b,
        }
    
        permission_map = {
            "r": 4,
            "w": 2,
            "x": 1,
        }
    
        new_permission_set = list(permission_set)
        for permission in permissions_to_change:
            if permission not in permission_map:
                print(f"Invalid permission: {permission}")
                return None
    
            permission_value = permission_map[permission]
            permission_index = permission_value // 3
            current_permission = new_permission_set[permission_index]
            new_permission_value = operator_map[operator](current_permission, permission_value)
    
            new_permission_set[permission_index] = permission if new_permission_value else "-"
    
        return "".join(new_permission_set)
    

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

    def move_file(self, file_name):
        for file in self.current_directory.files:
            if file.name == file_name:
                destination_directory = input("Enter destination directory: ")
                for directory in self.current_directory.subdirectories:
                    if directory.name == destination_directory:
                        directory.add_file(file)
                        self.current_directory.files.remove(file)
                        print(f"Moved '{file_name}' to '{destination_directory}'.")
                        return
                print(f"Directory '{destination_directory}' not found.")
                return
        print(f"File '{file_name}' not found.")

    def remove_file(self, file_name):
        for file in self.current_directory.files:
            if file.name == file_name:
                self.current_directory.files.remove(file)
                print(f"Removed '{file_name}'.")
                return
        print(f"File '{file_name}' not found.")

    def create_link(self, file_name):
        for file in self.current_directory.files:
            if file.name == file_name:
                link_name = input("Enter link name: ")
                link = File(link_name)
                link.contents = file.contents
                self.current_directory.add_file(link)
                print(f"Created link '{link_name}' for '{file_name}'.")
                return
        print(f"File '{file_name}' not found.")




class SSHServer:
    def __init__(self, address, username, password):
        self.address = address
        self.username = username
        self.password = password
        self.current_directory = Directory("/")
        self.connected = False

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

    def run_command(self, command):
        if not self.connected:
            if command.startswith("ssh "):
                _, server_info = command.split("ssh ", 1)
                username, address = server_info.split("@", 1)
                password = getpass.getpass("Enter password: ")
                self.connect_ssh_server(address, username, password)
                return True
            elif command == "exit":
                return False
            else:
                print("Not connected to any server. Use 'ssh' command to connect.")
                return True
        else:
            if command == "exit":
                self.disconnect()
                return True
            else:
                print("Unknown command.")
                return True

    def connect_ssh_server(self, address, username, password):
        self.disconnect()
        self.current_directory = Directory("/")
        self.address = address
        self.username = username
        self.password = password
        self.connect()



terminal = Terminal()
owner = input("Enter your username: ")
while True:
    
    command = input("$ ")
    continue_loop = terminal.run_command(command)
    if not continue_loop:
        break

# Terminal Emulator Project

"This project is a terminal emulator that simulates the behavior of a command-line interface and provides an exam environment. It allows users to navigate through directories, create and delete files and directories, change permissions, and perform various other operations, while also offering a dedicated exam mode for students to take tests."

## Features

- Directory navigation: Users can navigate through directories using commands like `cd`, `ls`, and `pwd`.
- File and directory creation: Users can create files and directories using the `mkdir` and `touch` commands.
- File and directory deletion: Users can delete files and empty directories using the `rm` and `rmdir` commands.
- Permission management: Users can change the permissions of files and directories using the `chmod` command.
- Symbolic and hard linking: Users can create symbolic and hard links between files and directories using the `ln` command.
- SSH server connection: Users can connect to a remote server using the `ssh` command.
- Additional commands: The terminal emulator also supports additional commands such as `cat`, `sort`, `uniq`, `grep`, `wc`, `head`, `tail`, `tee` (and `>`), `cp`, `cal`, `date`, `man`, `whoami`, `mv`, and `rm`.
- Clearing the terminal screen using `clean`
- Exam mode: Students can take a test using the built-in exam mode by typing `exam`.

## Usage

1. Clone the repository: `git clone https://github.com/mariamzhamakochyan/Linux-Emulator.git`
2. Navigate to the project directory: `cd Linux-Emulator`
3. Run the terminal emulator: `python3 main.py`

## Available Commands

The terminal emulator supports the following commands:

- `cd <directory>`: Change the current directory.
- `ls [-l]`: List the contents of the current directory. The `-l` option displays detailed information.
- `pwd`: Print the current working directory.
- `mkdir <directory>`: Create a new directory.
- `touch <filename>`: Create a new file.
- `rm [-r|-rf] <filename>`: Delete a file. The `-r` or `-rf` options allow recursive deletion.
- `rmdir <directory>`: Delete an empty directory.
- `chmod <permissions> <filename>`: Change the permissions of a file or directory.
- `ln [-s] <source> <target>`: Create a symbolic or hard link between files or directories.
- `ssh <username>@<hostname>`: Connect to a remote server via SSH.
- `cat <filename>`: Display the contents of a file.
- `sort <filename>`: Sort the lines of a file in alphabetical order.
- `uniq <filename>`: Remove duplicate lines from a file.
- `grep <pattern> <filename>`: Search for a pattern in a file.
- `wc <filename>`: Count the number of words, lines, and characters in a file.
- `head <filename>`: Display the first few lines of a file.
- `tail <filename>`: Display the last few lines of a file.
- `tee <filename>`: Read from standard input and write to a file.
- `> <filename>`: Redirect standard output to a file (similar to `tee` command).
- `cp <source> <destination>`: Copy a file to a new location.
- `cal`: Display a calendar for the current month.
- `date`: Display the current date and time.
- `man <command>`: Display the manual page for a command.
- `whoami`: Display the current user.
- `mv <source> <destination>`: Move or rename a file or directory.
- `vim <filename>`: Open a file in the Vim text editor.
- `echo <message>`: Print a message to the terminal.
- `clear`: Clear the terminal screen.
- `exam`: Enter exam mode to take a test.

## Contributing

Contributions to the terminal emulator project are welcome! If you find any issues or have suggestions for improvements, please create a new issue or submit a pull request.

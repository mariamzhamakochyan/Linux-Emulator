import datetime

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
        
    def clear_contents(self):
        self.contents = []

    def delete_line(self, line_number):
        if line_number < 1 or line_number > len(self.contents):
            print("Invalid line number.")
            return
        del self.contents[line_number - 1]
class SymbolicLink:
    def __init__(self, name, target):
        self.name = name
        self.target = target
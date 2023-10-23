import os
import subprocess
import sys

'''
I don't think this function is robust to the line number. It just appends the line too. I've made a test file called test.txt and and the function could fail if the line number being specified to be added to does not exist. How do we make sure we can read the total number of lines and 
'''
class Controller:
    def __init__(self):
        pass

    def create_directory(self, dir_name):
        """Create a directory."""
        try:
            os.makedirs(dir_name)
            return f"Directory {dir_name} created successfully!"
        except FileExistsError:
            return f"Directory {dir_name} already exists!"

    def change_directory(self, dir_name):
        """Change the current directory."""
        try:
            os.chdir(dir_name)
            return f"Changed to directory {dir_name}!"
        except FileNotFoundError:
            return f"Directory {dir_name} not found!"

    def print_working_directory(self):
        """Get the current working directory."""
        return os.getcwd()

    def execute_command(self, command):
        """Execute a bash command."""
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            return error.decode('utf-8')
        return output.decode('utf-8')

    def read_file(self, file_path):
        """Read the contents of a file."""
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return f"File {file_path} not found!"

    def list_directory_contents(self, dir_path="."):
        """List the contents of a directory."""
        return os.listdir(dir_path)

    def write_to_file(self, file_path, content, mode='w'):
        """Write content to a file. By default, it overwrites the file."""
        with open(file_path, mode) as file:
            file.write(content)
        return f"Content written to {file_path}!"

    def insert_into_file(self, file_path, content, line_num=None):
        """Insert content into a specific section of a file."""
        with open(file_path, 'r') as file:
            lines = file.readlines()

        if line_num is None or line_num > len(lines):
            # Append new lines to reach the desired line number
            lines.extend(['\n'] * (line_num - len(lines) - 1))
            lines.append(content + '\n')
        else:
            lines.insert(line_num - 1, content + '\n')

        with open(file_path, 'w') as file:
            file.writelines(lines)
        return f"Content inserted into {file_path}!"

    def delete_lines(self, file_path, lines):
        """Delete specified lines from a file."""
        with open(file_path, 'r') as file:
            content = file.read().split('\n')
        
        if isinstance(lines, int):
            lines = [lines]
        
        for line_num in lines:
            if 0 < line_num <= len(content):
                content[line_num - 1] = ''  # Replace the line with a blank space
        
        with open(file_path, 'w') as file:
            file.write('\n'.join(content))
        return f"Lines {lines} replaced with blank space in {file_path}!"


    def rewrite_lines(self, file_path, lines_content):
        """Replace specified lines with provided content."""
        with open(file_path, 'r') as file:
            content = file.read().split('\n')
        
        for line_num, new_content in lines_content.items():
            if 0 < line_num <= len(content):
                content[line_num - 1] = new_content
        
        with open(file_path, 'w') as file:
            file.write('\n'.join(content))
        return f"Lines rewritten in {file_path}!"


def main():
    controller = Controller()
    
    command = sys.argv[1]
    if command == "create_directory":
        print(controller.create_directory(sys.argv[2]))
    elif command == "change_directory":
        print(controller.change_directory(sys.argv[2]))
    elif command == "print_working_directory":
        print(controller.print_working_directory())
    elif command == "execute_command":
        print(controller.execute_command(' '.join(sys.argv[2:])))
    elif command == "read_file":
        print(controller.read_file(sys.argv[2]))
    elif command == "list_directory_contents":
        print(controller.list_directory_contents(sys.argv[2]))
    elif command == "write_to_file":
        print(controller.write_to_file(sys.argv[2], sys.argv[3]))
    elif command == "insert_into_file":
        print(controller.insert_into_file(sys.argv[2], sys.argv[3], int(sys.argv[4])))
    elif command == "delete_lines":
        print(controller.delete_lines(sys.argv[2], list(map(int, sys.argv[3:]))))
    elif command == "rewrite_lines":
        # For simplicity, this command takes line and content as two subsequent arguments.
        # Example: python controller.py rewrite_lines sample.txt 2 "New content for line 2"
        print(controller.rewrite_lines(sys.argv[2], {int(sys.argv[3]): sys.argv[4]}))

if __name__ == "__main__":
    main()
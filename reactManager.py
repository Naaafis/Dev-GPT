from controller import Controller
import os
import subprocess
import time
import sys
import json
import ast
import re

class ReactAppManager:
    def __init__(self, app_name):
        self.controller = Controller()
        self.react_app_name = app_name
        
        '''
        The root directory is always where the ReactManager is instantiated in the first place, 
        as in where the controller and agents are located. This directory is the higher level directory 
        where the React app directory contents are manipulated.
        '''
        
        self.root_directory = self.controller.print_working_directory()
        # self.create_react_app()
        #self.setup_react_directory()

    def setup_react_directory(self):
        """Enforced file structure"""
        src_dir = os.path.join(self.get_react_app_directory(), "/src")
        self.create_directory(src_dir, "/assets")
        self.create_directory(src_dir, "/components")
        self.create_directory(src_dir, "/hooks")
        self.create_directory(src_dir, "/context")
        self.create_directory(src_dir, "/data")
        self.create_directory(src_dir, "/pages")
        self.create_directory(src_dir, "/util")

    def exec_tests(self):
        # Run the Jest tests
        os.chdir(self.get_react_app_directory())
        try:
            process = subprocess.Popen("npm test -- --json --watchAll=false", stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.get_react_app_directory(), shell=True)
            output, error = process.communicate()
            match = re.search(r'"numFailedTests":(\d+),', output.strip().decode('utf-8'))
            num_tests_failed = 0
            if match:
                num_tests_failed = int(match.group(1))
        except subprocess.CalledProcessError as e:
            return ("An error occurred while running the tests." + str(e))
        
        return num_tests_failed, output.strip().decode('utf-8')
    
    def lint(self):
        # Run the eslint
        os.chdir(self.get_react_app_directory())
        try:
            result = subprocess.run("npx eslint src", stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.get_react_app_directory(), shell=True)
            match = re.search(r'(\d+) problems', result.stdout.strip().decode('utf-8'))
            num_tests_failed = 0
            if match:
                num_tests_failed = int(match.group(1))
        except subprocess.CalledProcessError as e:
            return ("An error occurred while linting.")
        
        return num_tests_failed, result.stdout

    # def lint(self, file_paths=None):
    #     report = []
    #     # js_file_paths = os.path.join(self.get_react_app_directory(), js_file_paths) 
    #     if not file_paths:

    #     for file_path in file_paths:
    #         # Check if the provided JavaScript file exists
    #         file_path = os.path.join(self.get_react_app_directory(), file_path) 
    #         if not os.path.exists(file_path):
    #             print(f"Error: File '{file_path}' does not exist.")
    #             continue  # Skip to the next file if it doesn't exist

    #         try:
    #             # Run ESLint on the JavaScript file
    #             result = subprocess.run(f"npx eslint {file_path}", capture_output=True, text=True, check=True, cwd=self.get_react_app_directory(), shell=True)

    #             # Check if ESLint reported any issues
    #             if result.returncode == 0:
    #                 report.append(f"Linting passed for {file_path}: No issues found.")
    #             else:
    #                 report.append(result.stdout)
    #         except subprocess.CalledProcessError as e:
    #             report.append(f"Linting failed for {file_path} with error: {e}")
    #         except FileNotFoundError:
    #             report.append("Error: ESLint not found. Make sure ESLint is installed and in your PATH.")
    #     return '\n'.join(report)
    

    '''
    The set of functions below is used by the PlanningAgent to get a sense of its surrounding environment.
    '''
    
    def set_react_app_name(self, app_name):
        """Set the React app name."""
        self.react_app_name = app_name
        
    def get_react_app_directory(self):
        """Get the React app directory."""
        if self.react_app_name:
            return os.path.join(self.root_directory, self.react_app_name)
        else:
            return "No React app name set. Please create a React app or set its name."
        
    def get_react_app_name(self):
        """Get the React app name."""
        if self.react_app_name:
            return self.react_app_name
        else:
            return "No React app name set. Please create a React app or set its name."
    
    def get_root_directory(self):
        """Get the root directory."""
        return self.root_directory
    
    def list_react_files(self, directory=None):
        """List the files in the React app directory."""
        if not self.react_app_name:
            return "No React app name set. Please create a React app or set its name."
        
        if not directory:
            directory = self.get_react_app_directory()
        else:
            directory = os.path.join(self.get_react_app_directory(), directory)    
        
        return self.controller.list_directory_contents(directory)
    
    def list_react_directory_contents(self):
        """Recursively list the contents of sub directories in the React app directory."""
        if not self.react_app_name:
            return "No React app name set. Please create a React app or set its name."
        
        directory_structure = {}

        for root, dirs, files in os.walk(self.get_react_app_directory()):
            current = directory_structure
            path_parts = root.replace(self.get_react_app_directory(), '').split(os.sep)
            for part in path_parts:
                if not part:
                    continue
                if part not in current:
                    current[part] = {}
                current = current[part]
            for f in files:
                current[f] = None

        return directory_structure

    def pretty_print_react_directory_contents(self, directory=None, indent=0):
        """
        Pretty prints a nested dictionary representing a directory structure.
        """
        if not directory:
            directory = self.list_react_directory_contents()
        output = ""
        for key, value in directory.items():
            output += ' ' * indent + key + "\n"
            if isinstance(value, dict):
                output += self.pretty_print_react_directory_contents(value, indent + 4)
        return output

    def get_plan_items(self):
        file_path = os.path.join(self.get_react_app_directory(), 'plan.txt')
        steps = []  # Initialize an empty list to store grouped steps
        current_group = []  # Initialize the current group of items as an empty list
        print(file_path)
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        # Check if the line starts with a numerical step (e.g., "1. ", "2. ", etc.)
                        if line[0].isdigit() and line[1] == '.':
                            # If a new numerical step is encountered, add the current group to the list
                            if current_group:
                                steps.append(current_group)
                            current_group = []  # Initialize a new group for this step
                        # Add the line to the current group of items
                        current_group.append(line)

                # Append the last group of items to the list
                if current_group:
                    steps.append(current_group)
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        return steps

    
    ####################################################################################################################
        
    '''
    Below are higher level shell commands that can be used to interact with the hosting OS environment.
    The ExecutorAgent will use these functions to execute the plan of tasks generated by the PlanningAgent.
    '''

    def check_os(self):
        """Check the operating system."""
        os_type = os.name
        if os_type == 'posix':
            return "Unix-like"
        elif os_type == 'nt':
            return "Windows"
        else:
            return os_type

    def check_node_version(self):
        """Check the installed node version."""
        cmd = "node -v"
        version = self.controller.execute_command(cmd)['message']
        return "success" in version.lower()

    def install_node_based_on_os(self):
        """Install Node.js based on the OS."""
        os_type = self.check_os()
        if os_type == 'Unix-like':
            return self.controller.execute_command("sudo apt-get install nodejs")
        elif os_type == 'Windows':
            return {"status": "info", "message": "Please download the Node.js installer for Windows."}
        else:
            return {"status": "error", "message": f"OS type {os_type} not supported for automatic Node.js installation."}

    def check_for_common_package_installers(self):
        """Check for common package managers like npm and yarn."""
        npm_version = self.controller.execute_command("npm -v")['message']
        yarn_version = self.controller.execute_command("yarn -v")['message']
        return {"npm": npm_version, "yarn": yarn_version}
    
    def check_react_version(self):
        """Check if React is installed."""
        cmd = "npx -v"
        version = self.controller.execute_command(cmd)['message']
        return "success" in version.lower()

    def install_npm_packages(self, packages):
        """Install npm packages."""
        cmd = f"npm install {' '.join(packages)}"
        return self.controller.execute_command(cmd)
    
    def create_react_app(self):
        """Create a new React app."""
        cmd = f"npx create-react-app {self.react_app_name}"
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.getcwd(), shell=True)
        
    def npm_start(self):
        """Start the React app using npm and check if it compiles successfully."""
        if not self.react_app_name:
            return "No React app name set. Please create a React app or set its name."

        # Navigate to the React app directory
        app_directory = os.path.join(self.controller.print_working_directory(), self.react_app_name)

        try:
            # Start the npm process
            process = subprocess.Popen(['npm', 'start'], cwd=app_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Check the real-time output for the "Compiled successfully!" string
            for line in iter(process.stdout.readline, ''):
                print(line)  # print the real-time output (optional)
                if "Compiled successfully!" in line:
                    # Optionally stop the server here if you don't need it running
                    # process.terminate()
                    return "React app compiled successfully!"

            # If the loop completes without finding the string, there might have been an error
            return "There might have been an error starting the React app."

        except Exception as e:
            return f"Error starting React app: {e}"
        
    def stop_react_app(self):
        try:
            # Get list of processes listening on port 3000
            result = subprocess.check_output(["lsof", "-i", ":3000"]).decode("utf-8")
            lines = result.split("\n")[1:]  # Exclude the header line

            for line in lines:
                print("Line: ", line)
                if not line:
                    continue
                parts = line.split()
                pid = parts[1]
                name = parts[-2]

                # Check if 'localhost' is in the name
                if "localhost" in name:
                    # Kill the process
                    os.kill(int(pid), 9)
                    print(f"Killed process with PID: {pid}")

        except Exception as e:
            print(f"Error stopping React app: {e}")
    
    ####################################################################################################################
    
    '''
    The set of functions below is used by the CodeWritingAgent to generate code snippets. They can create new files,
    edit existing files, or delete files. They can also create new directories within the React app directory.
    '''
    
    # execute any command for the manager
    def execute_command(self, command):
        """Allow the user to app Manager to execute any command."""
        self.controller.execute_command(command)
        
    def create_directory(self, dir_path, dir_name):
        """Create a directory within the React app directory."""
        self.controller.create_directory(os.path.join(self.get_react_app_directory(), dir_path, dir_name))
    
        
    def read_file(self, file_path, file_name):
        """Read a file in the React app directory."""
        if not self.react_app_name:
            return "No React app name set. Please create a React app or set its name."
        
        return self.controller.read_file(os.path.join(self.get_react_app_directory(), file_path, file_name))


    def create_new_file(self, file_path, file_name, content):
        """
        Create a new file within the React app directory.
        
        :param file_name: Name of the file to be created.
        :param content: Content to be written to the new file.
        :param directory: Directory within the React app directory where the file should be created.
        :return: Success or error message.
        """
        if not self.react_app_name:
            return "No React app name set. Please create a React app or set its name."

        # If directory is provided, check if it exists or create it.
        path = os.path.join(self.get_react_app_directory(), file_path)
        
        # Check if the file already exists using list_react_files
        if file_name in self.list_react_files(file_path):
            return f"File '{file_name}' already exists in the directory '{file_path}'."
        
        if not os.path.exists(path):
            os.makedirs(path)

        file_path = os.path.join(path, file_name)

        return self.controller.write_to_file(file_path, content)

    def write_to_file(self, file_path, file_name, content):
        """Write to a specified file in the React app directory."""
        if not self.react_app_name:
            return "No React app name set. Please create a React app or set its name."

        if not file_path:
            file_path = ""
        path = os.path.join(self.get_react_app_directory(), file_path, file_name)
        
        print("path: ", path, "content: ", content)
        if not os.path.exists(path):
            return self.create_new_file(file_path, file_name, content)


        return self.controller.write_to_file(path, content)

    def insert_into_file(self, file_path, file_name, content, line_num):
        """Insert content at a specified line in a specified file in the React app directory."""
        if not self.react_app_name:
            return "No React app name set. Please create a React app or set its name."

        # Check if file exists.
        path = os.path.join(self.get_react_app_directory(), file_path, file_name)
        if not os.path.exists(path):
            return "Invalid path: " + path
        
        print("path: ", path, "content: ", content, "line_num: ", line_num)

        return self.controller.insert_into_file(path, content, int(line_num))

    def delete_lines(self, file_path, file_name, line_nums):
        """Delete lines from a specified file in the React app directory."""
        if not self.react_app_name:
            return "No React app name set. Please create a React app or set its name."

        # Check if file exists.
        path = os.path.join(self.get_react_app_directory(), file_path, file_name)
        if not os.path.exists(path):
            return "Invalid path: " + path

        return self.controller.delete_lines(path, int(line_nums))

    def rewrite_lines(self, file_path, file_name, content):
        """Rewrite specified lines to a specified file in the React app directory."""
        if not self.react_app_name:
            return "No React app name set. Please create a React app or set its name."

        # Check if file exists.
        path = os.path.join(self.get_react_app_directory(), file_path, file_name)
        if not os.path.exists(path):
            return "Invalid path: " + path

        if isinstance(content, dict):
            return self.controller.rewrite_lines(path, content)
        else:
            return "Content is not a dictionary in the format {line_number(int): content(string)}"

    # The remaining functions will use the default 'replace' mode for editing
    def edit_json_file(self, filename, content_str):
        """
        Edit a specified JSON file in the React app directory.
        
        :param filename: Name of the JSON file to be edited.
        :param content_str: String representation of the content to be updated.
        :return: Success or error message.
        """
        content = ast.literal_eval(content_str)  # Convert string to dictionary
        if not self.react_app_name:
            return "No React app name set. Please create a React app or set its name."
        
        file_path = os.path.join(self.controller.print_working_directory(), self.react_app_name, filename)

        # Identify the key to search for based on the provided content
        key_to_search = list(content.keys())[0]
        search_str = f'"{key_to_search}":'

        # Read the file and determine the line number of the field to edit
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Find the line number for the specified key
        for i, line in enumerate(lines):
            if search_str in line:
                line_num = i + 1
                break
        else:
            return f"Field {key_to_search} not found in {filename}"

        # Construct the new content for the specified line
        new_content = f'  "{key_to_search}": "{content[key_to_search]}",'

        # Replace the line
        return self.controller.rewrite_lines(file_path, {line_num: new_content})

#     def edit_package_json(self, content_str):
#         return self.edit_json_file("package.json", content_str)

#     def edit_manifest_json(self, content_str):
#         return self.edit_json_file("public/manifest.json", content_str)

#     def edit_gitignore(self, content, mode='replace', line_num=None):
#         return self.edit_file(".gitignore", content, mode, line_num)

#     def edit_README(self, content, mode='replace', line_num=None):
#         return self.edit_file("README.md", content, mode, line_num)

#     def edit_index_html(self, content, mode='replace', line_num=None):
#         return self.edit_file("public/index.html", content, mode, line_num)

#     def edit_manifest_json(self, content, mode='replace', line_num=None):
#         return self.edit_file("public/manifest.json", content, mode, line_num)

#     def edit_index_js(self, content, mode='replace', line_num=None):
#         return self.edit_file("src/index.js", content, mode, line_num)

#     def edit_app_js(self, content, mode='replace', line_num=None):
#         return self.edit_file("src/App.js", content, mode, line_num)

#     def edit_app_css(self, content, mode='replace', line_num=None):
#         return self.edit_file("src/App.css", content, mode, line_num)
    
# def main():
#     manager = ReactAppManager()

#     command = sys.argv[1]
#     if command == "check_os":
#         print(manager.check_os())
#     elif command == "check_node_version":
#         print(manager.check_node_version())
#     elif command == "install_node_based_on_os":
#         print(manager.install_node_based_on_os())
#     elif command == "check_for_common_package_installers":
#         print(manager.check_for_common_package_installers())
#     elif command == "install_npm_packages":
#         packages = sys.argv[2:]
#         print(manager.install_npm_packages(packages))
#     elif command == "create_react_app":
#         print(manager.create_react_app(sys.argv[2]))
#     elif command == "edit_package_json":
#         content = sys.argv[2]
#         print(manager.edit_package_json(content))
#     elif command == "edit_gitignore":
#         content = sys.argv[2]
#         print(manager.edit_gitignore(content))
#     elif command == "edit_README":
#         content = sys.argv[2]
#         print(manager.edit_README(content))
#     elif command == "edit_index_html":
#         content = sys.argv[2]
#         print(manager.edit_index_html(content))
#     elif command == "edit_manifest_json":
#         content = sys.argv[2]
#         print(manager.edit_manifest_json(content))
#     elif command == "edit_index_js":
#         content = sys.argv[2]
#         print(manager.edit_index_js(content))
#     elif command == "edit_app_js":
#         content = sys.argv[2]
#         print(manager.edit_app_js(content))
#     elif command == "edit_app_css":
#         content = sys.argv[2]
#         print(manager.edit_app_css(content))
#     elif command == "create_new_file":
#         filename = sys.argv[2]
#         content = sys.argv[3] if len(sys.argv) > 3 else ""
#         directory = sys.argv[4] if len(sys.argv) > 4 else None
#         print(manager.create_new_file( directory, filename, content))
#     elif command == "write_to_file":
#         filename = sys.argv[2]
#         content = sys.argv[3] if len(sys.argv) > 3 else ""
#         directory = sys.argv[4] if len(sys.argv) > 4 else ""
#         print(manager.write_to_file(directory, filename, content))
#     elif command == "insert_into_file":
#         filename = sys.argv[2]
#         content = sys.argv[3] if len(sys.argv) > 3 else ""
#         line_num = sys.argv[4] if len(sys.argv) > 4 else 0
#         directory = sys.argv[5] if len(sys.argv) > 5 else ""
#         print("directory: ", directory, "filename: ", filename, "content: ", content, "line_num: ", line_num)
#         print(manager.insert_into_file(directory, filename, content, line_num))
#     elif command == "delete_lines":
#         filename = sys.argv[2]
#         line_nums = sys.argv[3] if len(sys.argv) > 3 else ""
#         directory = sys.argv[4] if len(sys.argv) > 4 else ""
#         print(manager.delete_lines(directory, filename, line_nums))
#     elif command == "npm_start":
#         print(manager.npm_start())
#     elif command == "stop_react_app":
#         manager.stop_react_app()
#     elif command == "list_react_files":
#         directory = sys.argv[2] if len(sys.argv) > 2 else None
#         print(manager.list_react_files(directory))
#     elif command == "read_file":
#         filename = sys.argv[2]
#         directory = sys.argv[3] if len(sys.argv) > 3 else ""
#         print(manager.read_file(directory, filename))

def main():
    manager = ReactAppManager(app_name='new-app')
    print(manager.exec_tests())

if __name__ == "__main__":
    main()


'''
# To check OS
python reactManager.py check_os

# To check Node version
python reactManager.py check_node_version

# To install Node based on OS
python reactManager.py install_node_based_on_os

# To check for common package installers
python reactManager.py check_for_common_package_installers

# To install npm packages
python reactManager.py install_npm_packages package1 package2

# To create a React app
python reactManager.py create_react_app my_app

# To edit package.json with new content
python reactManager.py edit_package_json "{'name': 'new-app-name'}"

# To edit .gitignore with new content
python reactManager.py edit_gitignore "# New ignore rule"

# To edit README.md with new content
python reactManager.py edit_README "# New README content"

# To edit public/index.html with new content
python reactManager.py edit_index_html "<!DOCTYPE html><html>...</html>"

# To edit public/manifest.json with new content
python reactManager.py edit_manifest_json "{'name': 'new-manifest-name'}"

# To edit src/index.js with new content
python reactManager.py edit_index_js "import React from 'react';..."

# To edit src/App.js with new content
python reactManager.py edit_app_js "function App() {...}"

# To edit src/App.css with new content
python reactManager.py edit_app_css "body { background-color: red; }"

python reactManager.py create_new_file sample.txt "Hello World"

python reactManager.py npm_start

python reactManager.py stop_react_app

# to write to a file
python reactManager.py write_to_file sample.txt "Hello World"


'''
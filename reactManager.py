from controller import Controller
import os
import subprocess
import sys
import json
import ast

class ReactAppManager:
    def __init__(self, app_name='my_app'):
        self.controller = Controller()
        self.react_app_name = app_name

    def set_react_app_name(self, app_name):
        """Set the React app name."""
        self.react_app_name = app_name

    def get_react_app_name(self):
        """Get the React app name."""
        if self.react_app_name:
            return self.react_app_name
        else:
            return "No React app name set. Please create a React app or set its name."

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
        return self.controller.execute_command(cmd)['message']

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

    def install_npm_packages(self, packages):
        """Install npm packages."""
        cmd = f"npm install {' '.join(packages)}"
        return self.controller.execute_command(cmd)

    def create_react_app(self, app_name):
        """Create a new React app."""
        cmd = f"npx create-react-app {app_name}"
        output = self.controller.execute_command(cmd)
        if "success" in output['message'].lower():
            return f"React app {app_name} created successfully!"
        else:
            return output
        
    def create_new_file(self, filename, content="", directory=None):
        """
        Create a new file within the React app directory.
        
        :param filename: Name of the file to be created.
        :param content: Content to be written to the new file.
        :param directory: Directory within the React app directory where the file should be created.
        :return: Success or error message.
        """
        if not self.react_app_name:
            return "No React app name set. Please create a React app or set its name."

        # If directory is provided, check if it exists or create it.
        if directory:
            dir_path = os.path.join(self.controller.print_working_directory(), self.react_app_name, directory)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        else:
            dir_path = os.path.join(self.controller.print_working_directory(), self.react_app_name)

        file_path = os.path.join(dir_path, filename)

        return self.controller.write_to_file(file_path, content)

    def edit_file(self, filename, content, mode='replace', line_num=None):
        """Edit specified file in the React app directory."""
        if not self.react_app_name:
            return "No React app name set. Please create a React app or set its name."

        file_path = os.path.join(self.controller.print_working_directory(), self.react_app_name, filename)

        if mode == 'replace':
            return self.controller.write_to_file(file_path, content)
        elif mode == 'insert':
            return self.controller.insert_into_file(file_path, content, line_num)
        elif mode == 'delete':
            return self.controller.delete_lines(file_path, [line_num])
        elif mode == 'rewrite':
            if isinstance(line_num, dict):
                return self.controller.rewrite_lines(file_path, line_num)
            else:
                return self.controller.rewrite_lines(file_path, {line_num: content})

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

    def edit_package_json(self, content_str):
        return self.edit_json_file("package.json", content_str)

    def edit_manifest_json(self, content_str):
        return self.edit_json_file("public/manifest.json", content_str)

    def edit_gitignore(self, content, mode='replace', line_num=None):
        return self.edit_file(".gitignore", content, mode, line_num)

    def edit_README(self, content, mode='replace', line_num=None):
        return self.edit_file("README.md", content, mode, line_num)

    def edit_index_html(self, content, mode='replace', line_num=None):
        return self.edit_file("public/index.html", content, mode, line_num)

    def edit_manifest_json(self, content, mode='replace', line_num=None):
        return self.edit_file("public/manifest.json", content, mode, line_num)

    def edit_index_js(self, content, mode='replace', line_num=None):
        return self.edit_file("src/index.js", content, mode, line_num)

    def edit_app_js(self, content, mode='replace', line_num=None):
        return self.edit_file("src/App.js", content, mode, line_num)

    def edit_app_css(self, content, mode='replace', line_num=None):
        return self.edit_file("src/App.css", content, mode, line_num)
    
def main():
    manager = ReactAppManager()

    command = sys.argv[1]
    if command == "check_os":
        print(manager.check_os())
    elif command == "check_node_version":
        print(manager.check_node_version())
    elif command == "install_node_based_on_os":
        print(manager.install_node_based_on_os())
    elif command == "check_for_common_package_installers":
        print(manager.check_for_common_package_installers())
    elif command == "install_npm_packages":
        packages = sys.argv[2:]
        print(manager.install_npm_packages(packages))
    elif command == "create_react_app":
        print(manager.create_react_app(sys.argv[2]))
    elif command == "edit_package_json":
        content = sys.argv[2]
        print(manager.edit_package_json(content))
    elif command == "edit_gitignore":
        content = sys.argv[2]
        print(manager.edit_gitignore(content))
    elif command == "edit_README":
        content = sys.argv[2]
        print(manager.edit_README(content))
    elif command == "edit_index_html":
        content = sys.argv[2]
        print(manager.edit_index_html(content))
    elif command == "edit_manifest_json":
        content = sys.argv[2]
        print(manager.edit_manifest_json(content))
    elif command == "edit_index_js":
        content = sys.argv[2]
        print(manager.edit_index_js(content))
    elif command == "edit_app_js":
        content = sys.argv[2]
        print(manager.edit_app_js(content))
    elif command == "edit_app_css":
        content = sys.argv[2]
        print(manager.edit_app_css(content))
    elif command == "create_new_file":
        filename = sys.argv[2]
        content = sys.argv[3] if len(sys.argv) > 3 else ""
        directory = sys.argv[4] if len(sys.argv) > 4 else None
        print(manager.create_new_file(filename, content, directory))


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

'''
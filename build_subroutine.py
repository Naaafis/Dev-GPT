from reactManager import ReactAppManager

from routines.subroutines.file_find import FileFindRoutine
from routines.subroutines.stub_write import StubWriteRoutine
from routines.subroutines.code_write import CodeWriteRoutine
from routines.subroutines.debug import DebugRoutine

from config.functions import *


class SubroutineBuilder:
    def __init__(self, api_key, app_name, high_level_task):
        self.app_name = app_name
        self.high_level_task = high_level_task
        self.api_key = api_key
        self.config_list = [{'model': 'gpt-4', 'api_key': self.api_key}]
        self.base_config = {
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        self.react_manager = ReactAppManager(self.app_name)
        self.app_directory = self.react_manager.get_react_app_directory()

        # Initialize other necessary components.
        self.init_subroutines()

    def perform_subroutines(self):
        # Perform routines for file finding, stub writing, code writing, and debugging.
        # Each of these routines will correspond to a phase in the development process.
        # These will interact with reactManager to perform tasks.
        
        print("FIND FILES ROUTINE")
        file_names = self.find_files.find_files(self.app_directory, self.high_level_task)
        print("List of files found: ", file_names)
        
        for file in file_names:
            print("STUB WRITING ROUTINE")
            print("File: ", file)
            self.stub_writing.stub_write(file)
            
            print("CODE WRITING ROUTINE")
            self.code_writing.code_write(file)
            
            print("DEBUGGING ROUTINE")
            self.debugging.debug(file)
            
        print("DONE")
        
    
    def find_files_routine(self):
        # Define the routine for finding relevant files based on the high_level_task.
        # This will likely involve interaction with the ReactAppManager to list files and search for relevant ones.
        self.file_contents_function_map = {
            "read_file": self.react_manager.read_file,
        }
        
        self.file_contents_config = {
            "functions": file_contents_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        
        self.ls_function_map = {
            "list_directory_contents": self.react_manager.list_directory_contents,
        }
        
        self.ls_config = {
            "functions": ls_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        
        self.file_creating_function_map = {
            "create_new_file": self.react_manager.create_new_file,
        }
        
        self.file_creating_config = {
            "functions": flie_creating_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
              
        self.find_files = FileFindRoutine(self.base_config, self.file_contents_config, self.file_contents_function_map, self.ls_config, self.ls_function_map, self.file_creating_config, self.file_creating_function_map)
        
    def stub_writing_routine(self):
        # Define the routine for writing stubs to the files found in the find_files_routine.
        # This will involve reading file contents and adding 'TODO' comments or function stubs.
        self.stub_writing_function_map = {
            "write_to_file": self.react_manager.write_to_file,
            "insert_into_file": self.react_manager.insert_into_file,
            "delete_lines": self.react_manager.delete_lines,
        }
        
        self.stub_writing_config = {
            "functions": stub_writing_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        
        self.stub_reading_function_map = {
            "read_file": self.react_manager.read_file,
        }
        
        self.stub_reading_config = {
            "functions": stub_reading_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        
        self.stub_writing = StubWriteRoutine(self.base_config, self.stub_reading_config, self.stub_reading_function_map, self.stub_writing_config, self.stub_writing_function_map)
        
    def code_writing_routine(self):
        # Define the routine for writing the actual code based on the stubs added in the stub_writing_routine.
        # This routine will turn the stubs into executable code.
        self.code_writing_function_map = {
            "read_file": self.react_manager.read_file,
            "write_to_file": self.react_manager.write_to_file,
            "insert_into_file": self.react_manager.insert_into_file,
            "delete_lines": self.react_manager.delete_lines,
        }
        
        self.code_writing_config = {
            "functions": code_writing_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        
        self.code_reading_function_map = {
            "read_file": self.react_manager.read_file,
        }
        
        self.code_reading_config = {
            "functions": code_reading_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        
        self.code_writing = CodeWriteRoutine(self.base_config, self.code_reading_config, self.code_reading_function_map, self.code_writing_config, self.code_writing_function_map)

    def debugging_routine(self):
        # Define the routine for debugging the code written in the code_writing_routine.
        # This will check for errors and ensure the code meets the high_level_task requirements.
        self.debugging_function_map = {
            "read_file": self.react_manager.read_file,
            "write_to_file": self.react_manager.write_to_file,
            "insert_into_file": self.react_manager.insert_into_file,
            "delete_lines": self.react_manager.delete_lines,
        }
        
        self.debugging_config = {
            "functions": debugging_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        
        self.debugging_reading_function_map = {
            "read_file": self.react_manager.read_file,
        }
        
        self.debugging_reading_config = {
            "functions": debug_reading_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
            
        
        self.debugging = DebugRoutine(self.base_config, self.debugging_reading_config, self.debugging_reading_function_map, self.debugging_config, self.debugging_function_map)


# The following are stubs and will need to be filled in with the actual logic.
def main():
    # Entry point for the script.
    # Parse arguments and create an instance of SubroutineBuilder.
    # Start the routines for the development process.
    subroutineBuilder = SubroutineBuilder("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", "subroutine-app", "Add firebase signin functionality to the specified app name. My google API key is _____.")
    subroutineBuilder.perform_subroutines()

if __name__ == "__main__":
    main()

from reactManager import ReactAppManager

# import subroutine classes
from routines.subroutines.file_find import FileFindRoutine
from routines.subroutines.stub_write import StubWriteRoutine
from routines.subroutines.code_write import CodeWriteRoutine
from routines.subroutines.debug import DebugRoutine

# import subroutine function configs
from config.functions import *

class SubroutineBuilder:
    def __init__(self, api_key, app_name, high_level_task):
        self.app_name = app_name
        self.high_level_task = high_level_task
        self.api_key = api_key
        
        # set up configurations for all none-function executing assitants
        self.config_list = [{'model': 'gpt-4', 'api_key': self.api_key}]
        self.base_config = {
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        self.react_manager = ReactAppManager(self.app_name)

        # Initialize config and function maps for each routine.
        self.init_subroutine_configs()
        self.find_files = FileFindRoutine(self.base_config, high_level_task, self.file_contents_config, self.file_creating_config, self.find_files_function_map)
        self.stub_writing = StubWriteRoutine(self.base_config, high_level_task, self.stub_reading_config, self.stub_writing_config, self.stub_writing_function_map)
        self.code_writing = CodeWriteRoutine(self.base_config, high_level_task, self.code_reading_config, self.code_writing_config, self.code_writing_function_map)
        self.debugging = DebugRoutine(self.base_config, high_level_task, self.debugging_reading_config, self.debugging_config, self.debugging_function_map)
        
    def perform_subroutines(self):
        # Perform routines for file finding, stub writing, code writing, and debugging.
        # Each of these routines will correspond to a phase in the development process.
        # These will interact with reactManager to perform tasks.
        
        print("FIND FILES ROUTINE")
        file_names = self.find_files.find_files()
        print("List of files found: ", file_names)
        
        for file in file_names:
            print("STUB WRITING ROUTINE")
            print("File: ", file)
            print(self.stub_writing.stub_write(file))
            
            print("CODE WRITING ROUTINE")
            print(self.code_writing.code_write(file))
            
            print("DEBUGGING ROUTINE")
            print(self.debugging.debug(file))
            
        print("DONE")
        
    
    def init_subroutine_configs(self):
        # Define the groupchat's configs for finding relevant files based on the high_level_task.
        # This will likely involve interaction with the ReactAppManager to read files and create relevant ones.
        self.find_files_function_map = {
            "read_file": self.react_manager.read_file,
            "create_new_file": self.react_manager.create_new_file,
            "list_react_files": self.react_manager.list_react_files,
        }
        
        self.file_contents_config = {
            "functions": file_contents_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        
        self.file_creating_config = {
            "functions": flie_creating_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        
        # Define the groupchat's configs for writing stubs to the files found in the find_files_routine.
        # This will involve reading file contents and adding 'TODO' comments or function stubs.
        self.stub_writing_function_map = {
            "read_file": self.react_manager.read_file,
            "write_to_file": self.react_manager.write_to_file,
        }
        
        self.stub_writing_config = {
            "functions": stub_writing_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        
        
        self.stub_reading_config = {
            "functions": stub_reading_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        
        # Define the groupchat's configs for writing the actual code based on the stubs added in the stub_writing_routine.
        # This routine will turn the stubs into executable code.
        self.code_writing_function_map = {
            "read_file": self.react_manager.read_file,
            "write_to_file": self.react_manager.write_to_file,
        }
        
        self.code_writing_config = {
            "functions": code_writing_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        
        self.code_reading_config = {
            "functions": code_reading_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        

        # Define the groupchat's configs for debugging the code written in the code_writing_routine.
        # This will check for errors and ensure the code meets the high_level_task requirements.
        self.debugging_function_map = {
            "read_file": self.react_manager.read_file,
            "write_to_file": self.react_manager.write_to_file,
        }
        
        self.debugging_config = {
            "functions": debugging_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        
        self.debugging_reading_config = {
            "functions": debug_reading_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
            


# The following are stubs and will need to be filled in with the actual logic.
def main():
    # Entry point for the script.
    # Parse arguments and create an instance of SubroutineBuilder.
    # Start the routines for the development process.
    subroutineBuilder = SubroutineBuilder("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", "subroutine-app", "Add firebase signin functionality to the specified app name. My google API key is _____.")
    subroutineBuilder.perform_subroutines()


if __name__ == "__main__":
    main()

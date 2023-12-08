from reactManager import ReactAppManager

# import subroutine classes
from routines.frontend.prompt_enhance import PromptEnhanceRoutine
from routines.frontend.image_create import ImageCreateRoutine
#from routines.frontend.chatbot_routie import ChatBotRoutine
from config.functions import *
from config.prompts import *

# import subroutine function configs

class FrontendBuilder:
    def __init__(self, api_key, app_name, high_level_task):
        self.app_name = app_name
        self.high_level_task = high_level_task
        self.api_key = api_key
        
        # set up configurations for all none-function executing assitants
        self.config_list = [{'model': 'gpt-4-1106-preview', 'api_key': self.api_key}]
        self.text_config_list = [{'model': 'gpt-4-vision-preview', 'api_key': self.api_key}]
        self.image_config_list = [{'model': 'dall-e-3', 'api_key': self.api_key}]
        self.base_config = {
            "timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        self.react_manager = ReactAppManager(self.app_name)

        # Initialize config and function maps for each routine.
        self.init_frontend_configs()
        #
        #self.chatbot_routine = ChatBotRoutine(self.base_config, self.chatbot_read_config, self.chatbot_write_config, self.chatbot_function_map)
        self.prompt_enhance = PromptEnhanceRoutine(self.base_config, self.prompt_read_config, self.prompt_write_config, self.prompt_writing_function_map)
        self.image_create = ImageCreateRoutine(self.base_config, self.imgcreate_prompt_write_config, self.imgcreate_read_config, self.imgcreate_write_config, self.img_create_function_map)
        
    def append_files_to_task_description(self, high_level_task, file_names):
        file_list_str = ", ".join(file_names)
        return f"{high_level_task}. Involved files: {file_list_str}"
    
        '''
        # Example usage:
        high_level_task = "Create a service worker component"
        file_names = ["src/App.js", "src/components/Component.js", "src/utils/helpers.js"]
        updated_task_description = append_files_to_task_description(high_level_task, file_names)
        '''

    
    def perform_frontend(self):
        # For assurance, we will read in file names from a file that the file creator wrote to.
        file_names_str = self.react_manager.read_file("", "relevant_files.txt")
        print("List of relevant files: ", file_names_str)
        
        file_names = file_names_str.split(", ")
        for file in file_names:
            print("PROMPT ENHANCING ROUTINE")
            print("File: ", file)
            #user_input = self.react_manager.read_file(".", "./saves/user_input.txt")
            #design_status = self.chatbot_routine.user_decision(user_input)
            #if design_status == "design":
            prompt = self.react_manager.read_file(".", "./saves/user_prompt.txt")
            self.prompt_enhance.prompt_enhance(file, prompt)
            enhanced_prompt = self.react_manager.read_file(".", "./saves/user_prompt.txt")
            #create_image = self.image_create.image_create(file, enhanced_prompt)
            
            #if design_status == "design"
            # design_status = readfile from "user_status.txt"
            user_feedback = self.react_manager.read_file(".", "./saves/user_feedback.txt")
            image_improve = self.image_create.image_create(file, enhanced_prompt, user_feedback)
            
            #if design_status == "satisfied"
            #PASS TO NAFIS STUFF
        print("DONE")
        
    
    def init_frontend_configs(self):
        self.temp_prompt = TEMP_PROMPT_PLACEHOLDER
        # Define the groupchat's configs for finding relevant files based on the high_level_task.
        # This will likely involve interaction with the ReactAppManager to read files and create relevant ones.
        self.find_files_function_map = {
            "read_file": self.react_manager.read_file,
            "create_new_file": self.react_manager.create_new_file,
            "list_react_files": self.react_manager.list_react_files,
        }
        
        self.file_contents_config = {
            "functions": file_contents_functions,
            "timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        
        self.file_creating_config = {
            "functions": flie_creating_functions,
            "timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        
        # Define the groupchat's configs for prompt enhancement for frontend
        # This will likely involve interaction with the ReactAppManager to read files and create relevant ones.
        self.prompt_writing_function_map = {
            "read_file": self.react_manager.read_file, #from reactManager.py
            "create_new_file": self.react_manager.create_new_file,
            "write_to_file": self.react_manager.write_to_file,
        }
        
        self.prompt_write_config = {
            "functions": prompt_writing_functions,
            "timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        
        self.prompt_read_config = {
            "functions": prompt_reading_functions,
            "timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        
        self.img_create_function_map = {
            "read_file": self.react_manager.read_file, #from reactManager.py
            "create_new_file": self.react_manager.create_new_file,
            "write_to_file": self.react_manager.write_to_file,
        }
        
        self.imgcreate_prompt_write_config = {
            "functions": prompt_writing_functions,
            "timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        
        self.imgcreate_write_config = {
            #"functions": imgcreate_writing_functions,
            "timeout": 600,
            "seed": 42,
            "config_list": self.image_config_list,
            "temperature": 0,
        }
        
        self.imgcreate_read_config = {
            "timeout": 600,
            "seed": 42,
            "config_list": self.text_config_list,
            "temperature": 0,
            "max_tokens": 4096,
        }
        
            

# The following are stubs and will need to be filled in with the actual logic.
def main():
    # Entry point for the script.
    # Parse arguments and create an instance of FrontendBuilder.
    # Start the routines for the development process.
    frontendBuilder = FrontendBuilder("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", "front_end", "Convert my web design prompt into an image")
    frontendBuilder.perform_frontend()
    
    # ReactAppManager = ReactAppManager("subroutine-app")
    # list_of_files = ReactAppManager.get_react_app_directory()

if __name__ == "__main__":
    main()
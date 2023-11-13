from autogen import *
from config.functions import *
from config.prompts import *

from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

class FileFindRoutine:
    """Routine to find relevant files in the React app directory."""
    def __init__(self, base_config, file_contents_config, file_contents_function_map, ls_config, ls_function_map, file_creating_config, file_creating_function_map):
        self.base_config = base_config
        self.file_contents_config = file_contents_config
        self.file_contents_function_map = file_contents_function_map
        self.ls_config = ls_config
        self.ls_function_map = ls_function_map
        self.file_creating_config = file_creating_config
        self.file_creating_function_map = file_creating_function_map
        self.termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()
        self.files_found = []
        self.all_sub_directories_in_components_directory = []
        self.sub_directories_visited = []
        self.files_left_to_visit = []

        # Agents for reading file contents, listing directory contents, and creating new files
        self.file_contents_agent = UserProxyAgent(
            name="file_contents_agent",
            max_consecutive_auto_reply=3,
            is_termination_msg=self.termination_msg,
            function_map=self.file_contents_function_map,
            human_input_mode="NEVER",
            default_auto_reply=FILE_CONTENTS_AUTO_REPLY,
            code_execution_config=False,
        )

        self.ls_agent = UserProxyAgent(
            name="ls_agent",
            max_consecutive_auto_reply=3,
            is_termination_msg=self.termination_msg,
            function_map=self.ls_function_map,
            human_input_mode="NEVER",
            default_auto_reply=LS_AUTO_REPLY,
            code_execution_config=False,
        )

        self.file_creating_agent = UserProxyAgent(
            name="file_creating_agent",
            max_consecutive_auto_reply=3,
            is_termination_msg=self.termination_msg,
            function_map=self.file_creating_function_map,
            human_input_mode="NEVER",
            default_auto_reply=FILE_CREATING_AUTO_REPLY,
            code_execution_config=False,
        )
        

    def find_files(self, app_directory, high_level_task):
        # Logic to find files based on the high_level_task
        # Use the agents to list directory contents, read file contents, and create new files as needed.
        # Return the list of relevant file paths.
        self.app_directory = app_directory

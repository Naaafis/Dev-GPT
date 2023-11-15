from autogen import *
from config.functions import *
from config.prompts import *

class FileFindRoutine:
    """
        Routine to find relevant files in the React app directory.
        Sample output: ['src/App.js', 'src/App.test.js', 'src/index.css', 'src/index.js', 'src/logo.svg', 'src/serviceWorker.js', 'src/setupTests.js']
        Sample high_level_task: ['create a service worker component']
        Sample function call: found_files = FileFindRoutine(self.base_config, app_directory, high_level_task, self.file_contents_config, self.file_creating_config, self.find_files_function_map)
    """
    def __init__(self, base_config, high_level_task, file_contents_config, file_creating_config, find_files_function_map):
        self.base_config = base_config
        self.high_level_task = high_level_task
        self.file_contents_config = file_contents_config
        self.file_creating_config = file_creating_config
        self.find_files_function_map = find_files_function_map

        FILE_FIND_CLIENT_AUTO_REPLY = """
        
            ~ Need to fill in the auto reply here ~
        
        """

        self.client = UserProxyAgent(
            name="client",
            max_consecutive_auto_reply=3,
            is_termination_msg=self.termination_msg,
            function_map=find_files_function_map,
            human_input_mode="NEVER",
            default_auto_reply=FILE_FIND_CLIENT_AUTO_REPLY,
            code_execution_config=False,
        )
        
        FILE_FIND_AGENT_SYSTEM_MESSAGE = """
        
            ~ Need to fill in the system message here ~
        
        """
        
        self.file_finder = AssistantAgent(
            name="file_finder",
            llm_config=self.file_contents_config,
            system_message=FILE_FIND_AGENT_SYSTEM_MESSAGE
        )
        
        
        FILE_CONTENTS_REVIEWER_SYSTEM_MESSAGE = """
        
            ~ Need to fill in the system message here ~
            
        """
        
        self.file_find_reviewer = AssistantAgent(
            name="file_find_reviewer",
            llm_config=self.base_config,
            system_message=FILE_CONTENTS_REVIEWER_SYSTEM_MESSAGE
        )
        
        FILE_CREATE_AGENT_SYSTEM_MESSAGE = """
        
            ~ Need to fill in the system message here ~
            
        """
        
        self.file_creator = AssistantAgent(
            name="file_creator",
            llm_config=self.file_creating_config,
            system_message=FILE_CREATE_AGENT_SYSTEM_MESSAGE
        )
        
        FILE_CREATE_REVIEWER_SYSTEM_MESSAGE = """
        
            ~ Need to fill in the system message here ~
            
        """
        
        self.file_create_reviewer = AssistantAgent(
            name="file_create_reviewer",
            llm_config=self.base_config,
            system_message=FILE_CREATE_REVIEWER_SYSTEM_MESSAGE
        )
    
    
    def find_files(self):
        # Logic to find files based on the high_level_task
        # Use the agents to list directory contents, read file contents, and create new files as needed.
        # Return the list of relevant file paths.
        
        # need two groupchats here, one for finding files and one for creating files
        
        # need to create the groupchat for finding files
        self.find_files_groupchat = GroupChat(
            agents=[self.client, self.file_finder, self.file_find_reviewer], messages=[], max_round=20
        )
        
        manager = GroupChatManager(groupchat=self.find_files_groupchat, llm_config=self.base_config)
        
        FILE_FIND_PROMPT = """
        
            ~ Need to fill in the prompt here ~
            
        """
        
        self.client.initiate_chat(
            manager,
            message=FILE_FIND_PROMPT.format(high_level_task=self.high_level_task)
        )
        
        # need to create the groupchat for creating files
        self.create_files_groupchat = GroupChat(
            agents=[self.client, self.file_creator, self.file_create_reviewer], messages=[], max_round=20
        )
        
        manager = GroupChatManager(groupchat=self.create_files_groupchat, llm_config=self.base_config)
        
        FILE_CREATE_PROMPT = """
        
            ~ Need to fill in the prompt here ~
            
        """
        
        self.client.initiate_chat(
            manager,
            message=FILE_CREATE_PROMPT.format(high_level_task=self.high_level_task, files_found=self.client.last_message()["content"])
        )
        
        # need to return the list of relevant file paths
        return self.client.last_message()["content"]

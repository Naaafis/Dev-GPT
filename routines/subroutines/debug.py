from autogen import *
from config.functions import *
from config.prompts import *

class DebugRoutine:
    """
    Routine for debugging the code written in the code_writing_routine.
    Checks for errors and ensures the code meets the high_level_task requirements.
    """
    def __init__(self, base_config, high_level_task, debug_reading_config, debug_writing_config, debugging_function_map):
        self.base_config = base_config
        self.high_level_task = high_level_task
        self.debug_reading_config = debug_reading_config
        self.debug_writing_config = debug_writing_config
        self.debugging_function_map = debugging_function_map

        DEBUG_CLIENT_AUTO_REPLY = """
            ~ Need to fill in the auto reply here ~
        """

        self.client = UserProxyAgent(
            name="client",
            max_consecutive_auto_reply=3,
            is_termination_msg=self.termination_msg,
            function_map=debugging_function_map,
            human_input_mode="NEVER",
            default_auto_reply=DEBUG_CLIENT_AUTO_REPLY,
            code_execution_config=False,
        )

        DEBUG_READING_AGENT_SYSTEM_MESSAGE = """
        
            ~ Need to fill in the system message here ~
            
        """
        
        self.debug_reader = AssistantAgent(
            name="debug_reader",
            llm_config=self.debug_reading_config,
            system_message=DEBUG_READING_AGENT_SYSTEM_MESSAGE
        )

        DEBUG_WRITING_AGENT_SYSTEM_MESSAGE = """
            ~ Need to fill in the system message here ~
        """

        self.debug_writer = AssistantAgent(
            name="debug_writer",
            llm_config=self.debug_writing_config,
            system_message=DEBUG_WRITING_AGENT_SYSTEM_MESSAGE
        )

        DEBUG_REVIEW_AGENT_SYSTEM_MESSAGE = """
            ~ Need to fill in the system message here ~
        """

        self.debug_reviewer = AssistantAgent(
            name="debug_reviewer",
            llm_config=self.base_config,
            system_message=DEBUG_REVIEW_AGENT_SYSTEM_MESSAGE
        )
    
    def debug(self, file_path):
        # Logic for debugging the written code
        # Use the agents to read file contents, identify and fix errors, and review the debugged code.
        
        self.debug_groupchat = GroupChat(
            agents=[self.client, self.debug_reader, self.debug_writer, self.debug_reviewer], messages=[], max_round=20
        )
        
        manager = GroupChatManager(groupchat=self.debug_groupchat, llm_config=self.base_config)
        
        DEBUG_PROMPT = """
            ~ Need to fill in the prompt here ~
        """
        
        self.client.initiate_chat(
            manager,
            message=DEBUG_PROMPT.format(high_level_task=self.high_level_task, file_path=file_path)
        )
        
        # Return success message or any relevant output
        return "Debugging completed successfully for " + file_path

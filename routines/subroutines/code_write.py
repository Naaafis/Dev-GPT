from autogen import *
from config.functions import *
from config.prompts import *

class CodeWriteRoutine:
    """
    Routine to write the actual code based on the stubs added in the stub_writing_routine.
    This routine will turn the stubs into executable code.
    """
    def __init__(self, base_config, high_level_task, code_reading_config, code_writing_config, code_writing_function_map):
        self.base_config = base_config
        self.high_level_task = high_level_task
        self.code_reading_config = code_reading_config
        self.code_writing_config = code_writing_config
        self.code_writing_function_map = code_writing_function_map

        CODE_WRITE_CLIENT_AUTO_REPLY = """
            ~ Need to fill in the auto reply here ~
        """

        self.client = UserProxyAgent(
            name="client",
            max_consecutive_auto_reply=3,
            is_termination_msg=self.termination_msg,
            function_map=code_writing_function_map,
            human_input_mode="NEVER",
            default_auto_reply=CODE_WRITE_CLIENT_AUTO_REPLY,
            code_execution_config=False,
        )

        CODE_READING_AGENT_SYSTEM_MESSAGE = """
        
            ~ Need to fill in the system message here ~
            
        """
        
        self.code_reader = AssistantAgent(
            name="code_reader",
            llm_config=self.code_reading_config,
            system_message=CODE_READING_AGENT_SYSTEM_MESSAGE
        )

        CODE_WRITE_AGENT_SYSTEM_MESSAGE = """
            ~ Need to fill in the system message here ~
        """

        self.code_writer = AssistantAgent(
            name="code_writer",
            llm_config=self.code_writing_config,
            system_message=CODE_WRITE_AGENT_SYSTEM_MESSAGE
        )

        CODE_REVIEW_AGENT_SYSTEM_MESSAGE = """
            ~ Need to fill in the system message here ~
        """

        self.code_reviewer = AssistantAgent(
            name="code_reviewer",
            llm_config=self.base_config,
            system_message=CODE_REVIEW_AGENT_SYSTEM_MESSAGE
        )
    
    def code_write(self, file_path):
        # Logic to write code based on the high_level_task and stubs
        # Use the agents to read file contents and write code as needed.
        
        self.code_write_groupchat = GroupChat(
            agents=[self.client, self.code_reader, self.code_writer, self.code_reviewer], messages=[], max_round=20
        )
        
        manager = GroupChatManager(groupchat=self.code_write_groupchat, llm_config=self.base_config)
        
        CODE_WRITE_PROMPT = """
            ~ Need to fill in the prompt here ~
        """
        
        self.client.initiate_chat(
            manager,
            message=CODE_WRITE_PROMPT.format(high_level_task=self.high_level_task, file_path=file_path)
        )
        
        # Return success message or any relevant output
        return "Code written successfully for " + file_path

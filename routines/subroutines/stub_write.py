from autogen import *
from config.functions import *
from config.prompts import *

class StubWriteRoutine:
    """
    Routine to write stubs to files found in the React app directory.
    This routine will read file contents and add 'TODO' comments or function stubs as needed.
    """
    def __init__(self, base_config, high_level_task, stub_reading_config, stub_writing_config, stub_writing_function_map):
        self.base_config = base_config
        self.high_level_task = high_level_task
        self.stub_reading_config = stub_reading_config
        self.stub_writing_config = stub_writing_config
        self.stub_writing_function_map = stub_writing_function_map

        STUB_WRITE_CLIENT_AUTO_REPLY = """
            ~ Need to fill in the auto reply here ~
        """

        self.client = UserProxyAgent(
            name="client",
            max_consecutive_auto_reply=3,
            is_termination_msg=self.termination_msg,
            function_map=stub_writing_function_map,
            human_input_mode="NEVER",
            default_auto_reply=STUB_WRITE_CLIENT_AUTO_REPLY,
            code_execution_config=False,
        )
        
        STUB_READING_AGENT_SYSTEM_MESSAGE = """
        
            ~ Need to fill in the system message here ~
            
        """
        
        self.stub_reader = AssistantAgent(
            name="stub_reader",
            llm_config=self.stub_reading_config,
            system_message=STUB_READING_AGENT_SYSTEM_MESSAGE
        )

        STUB_WRITE_AGENT_SYSTEM_MESSAGE = """
            ~ Need to fill in the system message here ~
        """

        self.stub_writer = AssistantAgent(
            name="stub_writer",
            llm_config=self.stub_writing_config,
            system_message=STUB_WRITE_AGENT_SYSTEM_MESSAGE
        )

        STUB_REVIEW_AGENT_SYSTEM_MESSAGE = """
            ~ Need to fill in the system message here ~
        """

        self.stub_creator = AssistantAgent(
            name="stub_reviewer",
            llm_config=self.base_config,
            system_message=STUB_REVIEW_AGENT_SYSTEM_MESSAGE
        )
    
    def stub_write(self, file_path):
        # Logic to write stubs based on the high_level_task
        # Use the agents to read file contents and write stubs as needed.
        
        self.stub_write_groupchat = GroupChat(
            agents=[self.client, self.stub_reader, self.stub_writer, self.stub_creator], messages=[], max_round=20
        )
        
        manager = GroupChatManager(groupchat=self.stub_write_groupchat, llm_config=self.base_config)
        
        STUB_WRITE_PROMPT = """
            ~ Need to fill in the prompt here ~
        """
        
        self.client.initiate_chat(
            manager,
            message=STUB_WRITE_PROMPT.format(high_level_task=self.high_level_task, file_path=file_path)
        )
        
        # Return success message or any relevant output
        return "Stub written successfully for " + file_path

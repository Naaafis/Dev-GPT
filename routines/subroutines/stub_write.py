from autogen import *
from config.functions import *
from config.prompts import *

class StubWriteRoutine:
    """
    Routine to write stubs to files found in the React app directory.
    This routine will read file contents and add 'TODO' comments or function stubs as needed.
    """
    def __init__(self, base_config, stub_reading_config, stub_writing_config, stub_writing_function_map):
        self.base_config = base_config
        self.stub_reading_config = stub_reading_config
        self.stub_writing_config = stub_writing_config
        self.stub_writing_function_map = stub_writing_function_map
        termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

        STUB_WRITE_CLIENT_AUTO_REPLY = """
            Ensure that all necessary stubs have been written to the relevant file. Reflect on the current stubs added. 
            Are there any parts of the high-level task that might need more detailed stubs or have been overlooked? 
            Consider re-evaluating the stubs for completeness and accuracy. Remember there are other files involved in this stub 
            writing process. If you are satisfied with the stubs, please reply with 'done'.
        """

        self.client = UserProxyAgent(
            name="client",
            max_consecutive_auto_reply=5,
            function_map=stub_writing_function_map,
            human_input_mode="NEVER",
            default_auto_reply=STUB_WRITE_CLIENT_AUTO_REPLY,
            code_execution_config=False,
        )
        
        STUB_READING_AGENT_SYSTEM_MESSAGE = """
            You are responsible for reading and analyzing the content of the file at the provided file path. Your goal is to identify where stubs or 'TODO' comments are needed. 
            Use the 'read_file' function, splitting 'file_path' into the directory and file name. For instance, if 'file_path' is 'src/utils/helper.js', 
            your read_file call should be with 'src/utils' as the directory and 'helper.js' as the file name. Look for areas that require further development or clarification.   
            
            Remember as a stub reader, you are not responsible for writing the stubs. But because you know the other relevant files, you can provide guidance on what stubs are needed.
            To this end, you can consider reading the other files and provide guidance for the stub writer on what the contents of the other relevant files are so the stub writer can
            accurately write the stubs.       
        """
        
        self.stub_reader = AssistantAgent(
            name="stub_reader",
            llm_config=self.stub_reading_config,
            system_message=STUB_READING_AGENT_SYSTEM_MESSAGE
        )

        STUB_WRITE_AGENT_SYSTEM_MESSAGE = """
            Your task is to add stubs and 'TODO' comments to the file at the provided path. These should align with our high-level task. 
            You only work with the provided file path but you gain insight from the stub_reader about the contents of the other relevant files.
            Remember when writing stubs that certain js functionalities with comments do not allow you to write inline comments next to the code.
            When using the 'write_to_file' function, remember to split 'file_path' into the directory and file name. 
            Ensure that your stubs are clear and provide a solid foundation for the subsequent coding phase.
        """

        self.stub_writer = AssistantAgent(
            name="stub_writer",
            llm_config=self.stub_writing_config,
            system_message=STUB_WRITE_AGENT_SYSTEM_MESSAGE
        )

        STUB_REVIEW_AGENT_SYSTEM_MESSAGE = """
            As a reviewer, critically evaluate the stubs added to the file at the file path. They should be coherent, relevant to our high-level task, and easy for developers to understand and act upon. 
    
            Use the 'read_file' function to access the updated content, splitting 'file_path' as needed. Provide feedback or suggest improvements to ensure high-quality stubs. Make sure that the written
            stubs do not conflate and halluciate on the contents of the other relevant files. To this end, you may want to look into the contents of the other files. Provide suggestions to the stub_writer
            to ensure that the stubs are accurate and relevant to the high-level task.
            
            If you think all the files are good to go, reply with 'done'. Tell the other agents to do the same.
        """

        self.stub_creator = AssistantAgent(
            name="stub_reviewer",
            llm_config=self.stub_reading_config,
            system_message=STUB_REVIEW_AGENT_SYSTEM_MESSAGE
        )
    
    def stub_write(self, file_path, high_level_task):
        # Logic to write stubs based on the high_level_task
        # Use the agents to read file contents and write stubs as needed.
        
        self.stub_write_groupchat = GroupChat(
            agents=[self.client, self.stub_reader, self.stub_writer, self.stub_creator], messages=[], max_round=20
        )
        
        manager = GroupChatManager(groupchat=self.stub_write_groupchat, llm_config=self.base_config)
        
        STUB_WRITE_PROMPT = """
            Our high-level task, '{high_level_task}', involves working across multiple files included in the high level task description. 
            Currently, focus on adding stubs to '{file_path}'. Identify sections requiring further development or placeholders. 
            Update this file with detailed 'TODO' comments or function stubs, and ensure they provide clear guidance for future coding.
        """
        
        self.client.initiate_chat(
            manager,
            message=STUB_WRITE_PROMPT.format(high_level_task=high_level_task, file_path=file_path)
        )
        
        # Return success message or any relevant output
        return "Stub written successfully for " + file_path

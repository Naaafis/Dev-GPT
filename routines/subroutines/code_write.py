from autogen import *
from config.functions import *
from config.prompts import *

class CodeWriteRoutine:
    """
    Routine to write the actual code based on the stubs added in the stub_writing_routine.
    This routine will turn the stubs into executable code.
    """
    def __init__(self, base_config, code_reading_config, code_writing_config, code_writing_function_map):
        self.base_config = base_config
        self.code_reading_config = code_reading_config
        self.code_writing_config = code_writing_config
        self.code_writing_function_map = code_writing_function_map

        CODE_WRITE_CLIENT_AUTO_REPLY = """
            Reflect on the current coding progress. Consider if any additional adjustments or enhancements are needed to meet our objectives. 
            Ensure all aspects of the implementation are thorough and aligned with the broader goals of our project. 
            If you believe the coding task is complete, reply with 'done'.
        """

        self.client = UserProxyAgent(
            name="client",
            max_consecutive_auto_reply=4,
            function_map=code_writing_function_map,
            human_input_mode="NEVER",
            default_auto_reply=CODE_WRITE_CLIENT_AUTO_REPLY,
            code_execution_config=False,
        )

        CODE_READING_AGENT_SYSTEM_MESSAGE = """
            You are responsible for understanding the current state of the code in the file we are working on. 
            Your insights are crucial for guiding the code writing process. 
            Utilize the 'read_file' function to review the code, and ensure that it aligns with the objectives outlined at the beginning of our chat. 
            Pay attention to how the existing code and stubs contribute to the overall project goals.   
            To use the function properly, you will have to split the given 'file_path' into the directory and file name. This will 
            be the input argued for the 'read_file' function. For instance, if 'file_path' is 'src/utils/helper.js', 
            your read_file call should be with 'src/utils' as the directory and 'helper.js' as the file name. 
            
            Remember as a code reader, you are not responsible for writing the code. But because you know the other relevant files, you can provide guidance on what code are needed.
            To this end, you can consider reading the other files and provide guidance for the code writer on what the contents of the other relevant files are so the code writer can
            accurately write the code. Additionally, you can provide guidance based on the stubs present in the file we are working on. You can of course also do the same for the stubs
            in the other relevant files.  
        """
        
        self.code_reader = AssistantAgent(
            name="code_reader",
            llm_config=self.code_reading_config,
            system_message=CODE_READING_AGENT_SYSTEM_MESSAGE
        )

        CODE_WRITE_AGENT_SYSTEM_MESSAGE = """
            Your primary task is to develop functional and efficient code based on the stubs and current implementation in the file we are focusing on. 
            Apply your expertise to write code that addresses the requirements and objectives outlined in our group chat. 
            Use the 'write_to_file' function for updating the code, ensuring it is clear, maintainable, and adheres to the project's standards.
            
            To use the function properly, you will have to split the given 'file_path' into the directory and file name. This will
            be the input argued for the 'write_to_file' function. For instance, if 'file_path' is 'src/utils/helper.js',
            your write_to_file call should be with 'src/utils' as the directory and 'helper.js' as the file name. You will 
            have to provide the content to be written to the file as the third argument to the function.
            
            When given suggestions from the code reader, you should adjust the contents of the code file accordingly. 
        """

        self.code_writer = AssistantAgent(
            name="code_writer",
            llm_config=self.code_writing_config,
            system_message=CODE_WRITE_AGENT_SYSTEM_MESSAGE
        )

        CODE_REVIEW_AGENT_SYSTEM_MESSAGE = """
            Your role involves critically assessing the code that is being developed. Ensure that it aligns with the project objectives and high-level task goals mentioned at the start of our chat. 
            Use the 'read_file' function to review the code. Provide feedback to improve functionality, efficiency, and adherence to coding best practices.
            To use the function properly, you will have to split the given 'file_path' into the directory and file name. This will
            be the input argued for the 'read_file' function. For instance, if 'file_path' is 'src/utils/helper.js', 
            your read_file call should be with 'src/utils' as the directory and 'helper.js' as the file name.
            
            Make sure that the written
            code does not conflate and halluciate on the contents of the other relevant files. To this end, you may want to look into the contents of the other files. Provide suggestions to the stub_writer
            to ensure that the stubs are accurate and relevant to the high-level task. You are working with the code reader to make sure all necessary contents have been properly defined in all the files, but make sure 
            that the writer writes the code only to the file we are working on.
            
            If you believe the code is complete, reply with 'done'. Tell the other agents to do the same.
        """

        self.code_reviewer = AssistantAgent(
            name="code_reviewer",
            llm_config=self.code_reading_config,
            system_message=CODE_REVIEW_AGENT_SYSTEM_MESSAGE
        )
    
    def code_write(self, file_path, high_level_task):
        # Logic to write code based on the high_level_task and stubs
        # Use the agents to read file contents and write code as needed.
        
        self.code_write_groupchat = GroupChat(
            agents=[self.client, self.code_reader, self.code_writer, self.code_reviewer], messages=[], max_round=20
        )
        
        manager = GroupChatManager(groupchat=self.code_write_groupchat, llm_config=self.base_config)
        
        CODE_WRITE_PROMPT = """
            We are focusing on '{file_path}' as part of our high-level task: '{high_level_task}'. Your task is to turn the existing stubs in this file into functional code. 
            Ensure your implementation is thorough and aligns with the task objectives. Update the file with your code, aiming for clarity, maintainability, and optimal performance.
        """
        
        self.client.initiate_chat(
            manager,
            message=CODE_WRITE_PROMPT.format(high_level_task=high_level_task, file_path=file_path)
        )
        
        # Return success message or any relevant output
        return "Code written successfully for " + file_path

from autogen import *
from config.functions import *
from config.prompts import *

class DebugRoutine:
    """
    Routine for debugging the code written in the code_writing_routine.
    Checks for errors and ensures the code meets the high_level_task requirements.
    """
    def __init__(self, base_config, debug_reading_config, debug_writing_config, debugging_function_map):
        self.base_config = base_config
        self.debug_reading_config = debug_reading_config
        self.debug_writing_config = debug_writing_config
        self.debugging_function_map = debugging_function_map

        DEBUG_CLIENT_AUTO_REPLY = """
            Reflect on the debugging process. Are there areas in the code that might still have issues or not fully align with the project's goals? 
            Ensure all potential bugs are addressed. Once you believe the debugging is thorough and complete, reply with 'done'.
        """


        self.client = UserProxyAgent(
            name="client",
            max_consecutive_auto_reply=3,
            function_map=debugging_function_map,
            human_input_mode="NEVER",
            default_auto_reply=DEBUG_CLIENT_AUTO_REPLY,
            code_execution_config=False,
        )

        DEBUG_READING_AGENT_SYSTEM_MESSAGE = """
            Your role is to meticulously review the code to identify any bugs or issues. Use the 'read_file' function as needed to examine the code thoroughly. 
            Pay close attention to any parts that might be problematic or misaligned with the project's objectives. Your detailed review is crucial for successful debugging.
            Remember to split 'file_path' into the directory and file name. For instance, if 'file_path' is 'src/utils/helper.js',
            your read_file call should be with 'src/utils' as the directory and 'helper.js' as the file name.
            
            Remember as a reader, you are not responsible for writing the code. But because you know the other relevant files, you can provide guidance on what debugging are needed.
            To this end, you can consider reading the other files and provide guidance for the debug writer on what the contents of the other relevant files are so the debug writer can
            accurately write the code. 
            
            You can also do some planning for the debugging process and provide additional filepaths to the debug writer to edit based on the plan. 
            This would only be the case if you think crucial pieces of the code are missing or need to be changed in order to meet the project's objectives.
            Refrain from doing this as we want to focus on one file at a time, but you can do this if you feel it is necessary. You should communicate with the reviwer before instructing 
            the debug writer to edit files outside of the current file we are working on.
        """

        
        self.debug_reader = AssistantAgent(
            name="debug_reader",
            llm_config=self.debug_reading_config,
            system_message=DEBUG_READING_AGENT_SYSTEM_MESSAGE
        )

        DEBUG_WRITING_AGENT_SYSTEM_MESSAGE = """
            As a debugger, your task is to address and fix any issues identified in the code. Utilize the 'write_to_file' function for making corrections. 
            Focus on enhancing the code's functionality and ensuring it meets the project's requirements and objectives.
            Remember to split 'file_path' into the directory and file name. For instance, if 'file_path' is 'src/utils/helper.js',
            your write_to_file call should be with 'src/utils' as the directory and 'helper.js' as the file name. You will
            have to provide the content to be written to the file as the third argument to the function.
        """


        self.debug_writer = AssistantAgent(
            name="debug_writer",
            llm_config=self.debug_writing_config,
            system_message=DEBUG_WRITING_AGENT_SYSTEM_MESSAGE
        )

        DEBUG_REVIEW_AGENT_SYSTEM_MESSAGE = """
            Your responsibility is to review the changes made during the debugging process. Ensure that the updated code is free of bugs and aligns with the project's objectives. 
            Use the 'read_file' function to access the updated code and provide feedback or further suggestions to refine the code as needed.
            Remember to split 'file_path' into the directory and file name. For instance, if 'file_path' is 'src/utils/helper.js',
            your read_file call should be with 'src/utils' as the directory and 'helper.js' as the file name.
            
            Make sure that the written
            code does not conflate and halluciate on the contents of the other relevant files. To this end, you may want to look into the contents of the other files. Provide suggestions to the stub_writer
            to ensure that the stubs are accurate and relevant to the high-level task. You are working with the code reader to make sure all necessary contents have been properly defined in all the files, but make sure 
            that the writer writes the code only to the file we are working on.
            
            If you think all the files are good to go, reply with 'done'. Tell the other agents to do the same.
        """


        self.debug_reviewer = AssistantAgent(
            name="debug_reviewer",
            llm_config=self.debug_reading_config,
            system_message=DEBUG_REVIEW_AGENT_SYSTEM_MESSAGE
        )
    
    def debug(self, file_path, high_level_task):
        # Logic for debugging the written code
        # Use the agents to read file contents, identify and fix errors, and review the debugged code.
        
        self.debug_groupchat = GroupChat(
            agents=[self.client, self.debug_reader, self.debug_writer, self.debug_reviewer], messages=[], max_round=20
        )
        
        manager = GroupChatManager(groupchat=self.debug_groupchat, llm_config=self.base_config)
        
        DEBUG_PROMPT = """
            Our current focus is on debugging '{file_path}' as part of our high-level task: '{high_level_task}'. Review the code for any bugs or issues, and ensure it aligns with our project goals. 
            Address any identified issues to enhance the overall quality and functionality of the code.
        """

        
        self.client.initiate_chat(
            manager,
            message=DEBUG_PROMPT.format(high_level_task=high_level_task, file_path=file_path)
        )
        
        # Return success message or any relevant output
        return "Debugging completed successfully for " + file_path

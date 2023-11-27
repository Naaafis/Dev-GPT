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
        self.termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

        FILE_FIND_CLIENT_AUTO_REPLY = """
            Are you sure you have identified all the files relevant to the high level task? Reflect on the current list of files identified. Are there any additional files that might be relevant to our high-level task of '{high_level_task}'? 
            If unsure, consider re-evaluating the directory or consulting the contents of the current files for further insights. The final message in this chat should just 
            be a list of relevant files without any other text. For example if the only file you identify as relevant is 'src/App.js', the last message in the chat should be 'src/App.js'.
        """

        self.find_client = UserProxyAgent(
            name="file_find_client",
            max_consecutive_auto_reply=5,
            function_map=find_files_function_map,
            human_input_mode="NEVER",
            default_auto_reply=FILE_FIND_CLIENT_AUTO_REPLY,
            code_execution_config=False,
        )
        
        FILE_FIND_AGENT_SYSTEM_MESSAGE = """
            You are an agent specialized in navigating the React app's file structure. 
            
            Your task is to analyze the project's directory and identify files relevant to the current high-level task. 
            This is the task of '{high_level_task}'.
            Use your knowledge and the provided functions to list and read the files in the React app directory. 
            
            One of your functions will list files in the high level React app directory.
            If you want to list the files in the 'src' directory, you can call the function with the argument 'src'. 
            If you want to list the files in the 'src/components' directory, you can call the function with the argument 'src/components'.
            
            The other function you have access to is 'read_file'. If you want to read the contents of the file 'src/App.js', you can call the function with the arguments
            'src' (for path) and 'App.js' (for file name). 
            
            You will have to tell the client the path and file name of the file you want to read and the client will read it for you.
            Similarly, you will have to tell the client the path of the directory you want to list and the client will list the files for you.
            
            If you identify a relevant file for the task, remember to add its full path to the list of relevant files.
            This should be the last message in the chat. For example if the only file you identify as relevant is 'src/App.js', the 
            last message in the chat should be 'src/App.js'. If you identify another file in a subdirectory called 'src/components' with the name 'blah.js',
            the last message in the chat should be 'src/App.js, src/components/blah.js'. Sometime you may need to create a new file to complete the high-level task.
            If this is the case you can just list the additional file as a part of the list of relevant files. For example, if you need to create a file called
            'src/components/blah.js', you can just list 'src/components/blah.js' as a part of the list of relevant files. 
            
            The final output of this groupchat should be a list of relevant files. There should be no other text in the final message.
        """
        
        self.file_finder = AssistantAgent(
            name="file_finder",
            llm_config=self.file_contents_config,
            system_message=FILE_FIND_AGENT_SYSTEM_MESSAGE.format(high_level_task=self.high_level_task)
        )
        
        
        FILE_CONTENTS_REVIEWER_SYSTEM_MESSAGE = """
            You are tasked with reviewing the files identified by the file finder agent. 
            Your role is to ensure that the files listed are indeed relevant to the high-level task of '{high_level_task}'. 
            Provide feedback on the selection and suggest if additional files should be considered. If you think all the 
            files listed thus far should be sufficient to complete a task, inform the file finder agent that the list is complete.
            Remember the files in the list should be in a structure where the file paths are included in the final list. You have 
            access to the same functions as the file finder agent. You can use these functions to list and read the files in the React app directory.
            You are more so using the list_react_files function to check that the file finder agent is not missing any files. This 
            may require you to read the contents of the files to determine if they are relevant to the high-level task. You will have to ask
            the client to read the contents of the file for you. Same for the list_react_files function. You will have to ask the client to list the files.
            
            The last message in this chat should be a list of relevant files. There should be no other text in the final message.  
        """
        
        self.file_find_reviewer = AssistantAgent(
            name="file_find_reviewer",
            llm_config=self.file_contents_config,
            system_message=FILE_CONTENTS_REVIEWER_SYSTEM_MESSAGE.format(high_level_task=self.high_level_task)
        )
        
        FILE_CREATE_CLIENT_AUTO_REPLY = """
            Are you sure all relevant files have been created? Reflect on the current list of files identified. 
            Do they all exist in the React app directory? 
            If unsure, consider re-evaluating the directory or consulting the contents of the sub-directories for further insights.
        """

        self.create_client = UserProxyAgent(
            name="file_create_client",
            max_consecutive_auto_reply=5,
            function_map=find_files_function_map,
            human_input_mode="NEVER",
            default_auto_reply=FILE_CREATE_CLIENT_AUTO_REPLY,
            code_execution_config=False,
        )
        
        FILE_CREATE_AGENT_SYSTEM_MESSAGE = """
            Your role is to create new files within the React app when required. 
            This task is essential when the current high-level task involves adding new features or components. 
            The current high-level task is '{high_level_task}'.
            You will be given a list of files from the file finder groupchat. If you identify a file that does not exist, 
            you will need to create it.
            
            Use the 'list_react_files' function to list the files in the React app directory. Check if the file you need to create already exists.
            Use the 'create_new_file' function to generate new files. 
            You will have to tell the client the path, file name, and initial content of the new file and the client will create it for you. 
            
            Ensure that the path, file name, and initial content are appropriate and align with the project's standards and structure. 
        """
        
        self.file_creator = AssistantAgent(
            name="file_creator",
            llm_config=self.file_creating_config,
            system_message=FILE_CREATE_AGENT_SYSTEM_MESSAGE.format(high_level_task=self.high_level_task)
        )
        
        FILE_CREATE_REVIEWER_SYSTEM_MESSAGE = """
            As a reviewer, your responsibility is to oversee the creation of new files. 
            Ensure that the files created by the file creation agent are necessary and appropriately structured. 
            Verify that new files do not duplicate existing functionality and are named and placed correctly within the project's directory.
            If you think all the files listed thus far should be sufficient to complete a task, inform the file creator agent that the list is complete.
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
            agents=[self.find_client, self.file_finder, self.file_find_reviewer], messages=[], max_round=20
        )
        
        manager = GroupChatManager(groupchat=self.find_files_groupchat, llm_config=self.base_config)
        
        FILE_FIND_PROMPT = """
            Considering our high-level task of '{high_level_task}', identify and list all the relevant files in the React app directory. 
            Use the 'list_react_files' function to explore the directory structure and 'read_file' to inspect file contents when necessary.
            The final output of this groupchat should be a list of relevant files. This should be the last message in the chat.
            Make sure that a comma separates each file path in the list. For example if the only file you identify as relevant is 'src/App.js', 
            and 'src/components/blah.js', the last message in the chat should be 'src/App.js, src/components/blah.js'. 
            Remember, 'src/App.js' is almost always relevant to any high-level task.
        """
        
        self.find_client.initiate_chat(
            manager,
            message=FILE_FIND_PROMPT.format(high_level_task=self.high_level_task)
        )
        
        # need to create the groupchat for creating files
        self.create_files_groupchat = GroupChat(
            agents=[self.create_client, self.file_creator, self.file_create_reviewer], messages=[], max_round=20
        )
        
        manager = GroupChatManager(groupchat=self.create_files_groupchat, llm_config=self.base_config)
        
        FILE_CREATE_PROMPT = """
            Based on the high-level task of '{high_level_task}' and the identified files: {files_found}, determine if there's a need to create new files. 
            If so, use the 'create_new_file' function to establish these files, specifying their path, name, and initial content.
            Remember, check to make sure all the identified files exist in the React app directory. If not, create them. Engage all 
            3 agents in this groupchat to ensure that the files are created correctly.
        """
        
        self.create_client.initiate_chat(
            manager,
            message=FILE_CREATE_PROMPT.format(high_level_task=self.high_level_task, files_found=self.find_client.last_message()["content"])
        )
        
        print("FileFindRoutine: Files found/created: ", self.create_client.last_message()["content"])
        
        # need to return the list of relevant file paths
        return self.find_client.last_message()["content"]

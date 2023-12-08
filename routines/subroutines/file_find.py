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
    def __init__(self, base_config, high_level_task, file_contents_config, file_writing_config, file_creating_config, find_files_function_map):
        self.base_config = base_config
        self.high_level_task = high_level_task
        self.file_contents_config = file_contents_config
        self.file_writing_config = file_writing_config
        self.file_creating_config = file_creating_config
        self.find_files_function_map = find_files_function_map
        self.termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

        FILE_FIND_CLIENT_AUTO_REPLY = """
            Are you sure you have identified all the files relevant to the high level task? Reflect on the current list of files identified. Are there any additional files that might be relevant to our high-level task of '{high_level_task}'? 
            If unsure, take a deep breath and consider re-evaluating the directory or consulting the contents of the current files for further insights. Are you sure that the relevant files have been written to a file called 'relevant_files.txt'?
            Are the contents of relevant_files.txt formatted as a comma seperated string of file paths? If the only relevant file is 'src/App.js', the contents of relevant_files.txt should be 'src/App.js'.
            If you identify another file in a subdirectory called 'src/components' with the name 'blah.js', the contents of relevant_files.txt should be 'src/App.js,src/components/blah.js'.
            If you are satisfied with the list of relevant files, reply with 'TERMINATE' and stop working on this task.
        """

        self.find_client = UserProxyAgent(
            name="file_find_client",
            is_termination_msg=self.termination_msg,
            max_consecutive_auto_reply=15,
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
            For example if the only file you identify as relevant is 'src/App.js', the relevant_files should contain 'src/App.js'. If you identify another file in a subdirectory called 'src/components' with the name 'blah.js',
            the relevant_files file should contain 'src/App.js,src/components/blah.js'. 
            
            Sometime you may need to create a new file to complete the high-level task.
            If this is the case you can just list the additional file as a part of the list of relevant files. For example, if you need to create a file called
            'src/components/blah.js', you can just list 'src/components/blah.js' as a part of the list of relevant files. 
            
            Take a deep breath, and good luck!
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
            the client to read the contents of the file for you. Same for the list_react_files function. 
            
            You are also ensuring that files are being created in the proper subdirectories. You wouldnt want to create a .css file in the src/components directory.
            You would want to create it in the src/style directory. You can use the list_react_files function to check the directory structure. 
            so if you need to create a new file called blah.css, you would want to make sure that it is being included in the relevant_files file as src/style/blah.css.
            Notice how the path is included in the file name. 
            
            The task of this chat is to come up with a list of relevant files.
            
            Take a deep breath, and good luck!
        """
        
        self.file_find_reviewer = AssistantAgent(
            name="file_find_reviewer",
            llm_config=self.file_contents_config,
            system_message=FILE_CONTENTS_REVIEWER_SYSTEM_MESSAGE.format(high_level_task=self.high_level_task)
        )
        
        # Everytime a new file is discvered, we have an agent call a function and write this new file to the list of relevant files
        # We can just write this in a relevant_files.txt file and have the agent read this file to get the list of relevant files 
        # For the next chat...
        
        RELEVANT_FILES_CREATOR_SYSTEM_MESSAGE = """
            You are tasked with writing to a file called 'relevant_files.txt' that will contain the list of relevant files.
            This file should be updated every time a new file is identified as relevant to the high-level task.
            You must ensure that the contents of this file is formatted as a comma seperated python string. For example, if the only file identified as relevant is 'src/App.js', the
            contents of the file should be 'src/App.js'. If another file in a subdirectory called 'src/components' with the name 'blah.js' is identified as relevant, 
            the contents of the file should be 'src/App.js,src/components/blah.js'. 
            
            You are calling a function called 'write_to_file' to write to the file. You will have to tell the client the path, file name, and content of the file you want to write to and the client will write it for you.
            
            To call this function, the path you provide will always be an empty string and the file name will always be 'relevant_files.txt'. The content will always be the comma seperated string of relevant files.
            
            Take a deep breath, and good luck!
        """
        
        self.relevant_files_creator = AssistantAgent(
            name="relevant_files_creator",
            llm_config=self.file_writing_config,
            system_message=RELEVANT_FILES_CREATOR_SYSTEM_MESSAGE.format(high_level_task=self.high_level_task)
        )
        
        FILE_CREATE_CLIENT_AUTO_REPLY = """
            Have you read in the contents of the file called 'relevant_files.txt'?
            Are you sure all relevant files have been created? Reflect on the current list of files identified. 
            Do they all exist in the React app directory? 
            If unsure, consider re-evaluating the directory or consulting the contents of the sub-directories for further insights.
            If you went over the entire list of files already, reply with 'TERMINATE' and stop working on this task.
            Take a deep breath, and good luck!
        """

        self.create_client = UserProxyAgent(
            name="file_create_client",
            is_termination_msg=self.termination_msg,
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
            You will be given a list of files from the relevant_files.txt file. The relevant_files_reader will read in the contents of the file for you.
            They can provide you with a list of files to check for existence. 
            
            If you identify a file that does not exist, you will need to create it. 
            Use the 'list_react_files' function to list the files in the React app directory. 
            If you want to list the files in the 'src' directory, you can call the function with the argument 'src'.
            If you want to list the files in the 'src/components' directory, you can call the function with the argument 'src/components'.
            
            Use the 'create_new_file' function to generate new files. 
            You will have to tell the client the path, file name, and initial content of the new file and the client will create it for you. 
            If the comma seperated list contains a file that has a path attached, for example 'src/components/blah.js', you will have to split the file path into the directory and file name.
            This means the input for the 'create_new_file' function will be 'src/components' for the directory and 'blah.js' for the file name.
            
            Ensure that the path, file name, and initial content are appropriate and align with the project's standards and structure. 
            
            Take a deep breath, and good luck!
        """
        
        self.file_creator = AssistantAgent(
            name="file_creator",
            llm_config=self.file_creating_config,
            system_message=FILE_CREATE_AGENT_SYSTEM_MESSAGE.format(high_level_task=self.high_level_task)
        )
        
        FILE_CREATE_REVIEWER_SYSTEM_MESSAGE = """
            As a reviewer, your responsibility is to oversee the creation of new files. 
            
            Make sure that the files created by the file creation agent are necessary and appropriately structured.
            The relevant_files_reader should have read in a file called 'relevant_files.txt' that contains the list of relevant files.
            They are providing you with a list of files to check for existence.
            
            Make sure that the this list of files is a comma seperated string of file paths. For example, if the only file identified as relevant is 'src/App.js', the
            contents of the file should be 'src/App.js'. If another file in a subdirectory called 'src/components' with the name 'blah.js' is identified as relevant,
            the contents of the file should be 'src/App.js,src/components/blah.js'.
            
            Make sure that the file_creator agent is splitting up each individual file path into the directory and file name when calling the 
            'create_new_file' function. For example, if the file path is 'src/components/blah.js', the directory should be 'src/components' and the file name should be 'blah.js'. 
            when calling the 'create_new_file' function.
            
            Verify that new files do not duplicate existing files and are named and placed correctly within the project's directory.
            You dont need to execute any functions to do this, the file_creator agent should be listing the files in the React app directory and checking if the file exists.
            You just need to make sure that the file creator is doing this correctly. 
            
            If you think all the files listed thus far exist, inform the file creator agent that the list is complete.
            
            Take a deep breath, and good luck!
        """
        
        self.file_create_reviewer = AssistantAgent(
            name="file_create_reviewer",
            llm_config=self.file_contents_config,
            system_message=FILE_CREATE_REVIEWER_SYSTEM_MESSAGE
        )
        
        RELEVANT_FILES_READER_SYSTEM_MESSAGE = """
            You are tasked with reading the file called 'relevant_files.txt' that contains the list of relevant files. 
            You are working with the file creator to make sure all necessary files have been created. Your only job is to inform 
            the file creator of the list of relevant files by calling the read_file function.
            
            The function should always be called with an empty string for the path and 'relevant_files.txt' for the file name.
            
            When you call the function, the client will read the file for you. You can assist 
            the file creator by splitting the comma seperated string of file paths into a list of file paths. For example, if the only file identified as relevant is 'src/App.js', the
            contents of the file should be 'src/App.js'. If another file in a subdirectory called 'src/components' with the name 'blah.js' is identified as relevant,
            the contents of the file should be 'src/App.js,src/components/blah.js'. You can split this into a list of file paths ['src/App.js', 'src/components/blah.js']. 
            This can help the file creator agent iterate through the list of files and check if they exist. 
            
            Take a deep breath, and good luck!
        """
        
        self.relevant_files_reader = AssistantAgent(
            name="relevant_files_reader",
            llm_config=self.file_contents_config,
            system_message=RELEVANT_FILES_READER_SYSTEM_MESSAGE
        )
    
    
    def find_files(self):
        # Logic to find files based on the high_level_task
        # Use the agents to list directory contents, read file contents, and create new files as needed.
        # Return the list of relevant file paths.
        
        # need two groupchats here, one for finding files and one for creating files
        
        # need to create the groupchat for finding files
        self.find_files_groupchat = GroupChat(
            agents=[self.find_client, self.file_finder, self.file_find_reviewer, self.relevant_files_creator], messages=[], max_round=20
        )
        
        manager = GroupChatManager(groupchat=self.find_files_groupchat, llm_config=self.base_config)
        
        FILE_FIND_PROMPT = """
            Considering our high-level task of '{high_level_task}', identify and list all the relevant files in the React app directory. 
            Use the 'list_react_files' function to explore the directory structure and 'read_file' to inspect file contents when necessary.
            
            The goal of this chat is to create a file called 'relevant_files.txt' that will contain the list of relevant files.
            This list is a comma seperated string of file paths. For example, if the only file identified as relevant is 'src/App.js', the
            contents of the file should be 'src/App.js'. If another file in a subdirectory called 'src/components' with the name 'blah.js' is identified as relevant,
            the contents of the file should be 'src/App.js,src/components/blah.js'.
            
            Remember, 'src/App.js' is almost always relevant to any high-level task.
        """
        
        self.find_client.initiate_chat(
            manager,
            message=FILE_FIND_PROMPT.format(high_level_task=self.high_level_task)
        )
        
        # need to create the groupchat for creating files
        self.create_files_groupchat = GroupChat(
            agents=[self.create_client, self.file_creator, self.file_create_reviewer, self.relevant_files_reader], messages=[], max_round=20
        )
        
        manager = GroupChatManager(groupchat=self.create_files_groupchat, llm_config=self.base_config)
        
        FILE_CREATE_PROMPT = """
            Based on the high-level task of '{high_level_task}' and the identified files, determine if there's a need to create new files. 
            To know which files are relevant to the high-level task, you can read in the contents of the file called 'relevant_files.txt'.
            This should be the first task of the chat, read in contents of 'relevant_files.txt' using the relevant_files_reader agent.
            Use the 'create_new_file' function to create new files, specifying their path, name, and initial content.
            Remember, check to make sure all the identified files exist in the React app directory first. If not, create them. Engage all 
            3 agents in this groupchat to ensure that the files are created correctly.
        """
        
        self.create_client.initiate_chat(
            manager,
            message=FILE_CREATE_PROMPT.format(high_level_task=self.high_level_task)
        )
        
        return "Done finding files"

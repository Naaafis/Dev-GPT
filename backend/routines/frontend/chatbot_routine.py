import autogen
from autogen import *
from config.functions import *
from config.prompts import *


class ChatBotRoutine:
    """
    Routine to define user_inputs.txt. Return 3 results
    "satisfied": go next step
    "
    """
    def __init__(self, base_config, prompt_read_config, prompt_write_config, prompt_writing_function_map):
        self.base_config = base_config
        self.chatbot_read_config = prompt_read_config
        self.chatbot_write_config = prompt_write_config
        self.chatbot_writing_function_map = prompt_writing_function_map
        
        termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

        CHATBOT_AUTO_REPLY = """
            Ensure that you have carefully read the user input and understood what the user want to proceed with next step.
            And make sure the instructions are saved in files respectively as told.
            If you are satisfied with the result, please reply with 'done'.
        """
    

        self.client = UserProxyAgent(
            name="client",
            max_consecutive_auto_reply=5,
            function_map=prompt_writing_function_map,
            human_input_mode="NEVER",
            default_auto_reply=CHATBOT_AUTO_REPLY,
            code_execution_config=False,
        )
            
        CHATBOT_READING_AGENT_MESSAGE = """
            You are responsible for reading and analyzing the content of the file at the provided file path. Your goal is to identify the user input in the file. 
            Use the 'read_file' function, splitting 'file_path' into the directory and file name. For instance, if 'file_path' is 'src/utils/helper.js', 
            your read_file call should be with 'src/utils' as the directory and 'helper.js' as the file name. Look for areas that require further development or clarification.
            
            Reading the user input from the file directed, you shall also decide if this user is looking for a new design for us to generate, or if he already has a design with us
            that he want to provide some feedback and make changes. Or is he satisfied with the current design and we could go on to the next steps
            After determining its a 'prompt' or 'feedback', you shall tell this to others in group, so they know which file to write to.
            They should only write into 'user_feedback.txt' if they identify the input are feedbacks and 'user_prompt.txt' to save the user's prompt for enhancement
            
            Remember as a chatbot reader, you are not responsible for writing the prompt. But because you know the other relevant files, you can provide guidance on prompt description
            To this end, you can consider reading the other files and provide guidance for the chatbot writer on what the contents of the other relevant files are so the 
            chatbot writer can accurately analyze the information.
            
        """
        #     IF you are unable to execute functions or access external files or databases, orretrieve the information from the file, use the prompt from variable temp_prompt which is also the start message of group chat. 
       
        
        self.chatbot_reader = AssistantAgent(
            name="chatbot_reader",
            llm_config=self.chatbot_read_config,
            system_message=CHATBOT_READING_AGENT_MESSAGE
        )
        
        CHATBOT_WRITING_AGENT_MESSAGE = """        
            You are responsible to write the group decision into respective files, there are 3 cases, user looking for a new design, user providing a feedback, or user is satisfied. 
            Initially, start by looking at 'user_input.txt' and look for the exact phrase "web design". If this phrase "web design" does not exist in the 'user_input.txt',
            this user input should immediately be identified as a feedback and placed in the 'user_feedback.txt'. The following instructions could then be ignored.
            
            If you think the the user is look for a new design, put all he said into "user_prompt.txt" in the same filepath.
            Also, write "FALSE" and nothing else in the "user_feedback.txt" if you identify the user input as a new prompt.
            
            Secondly, if you think the user is giving us some feedback on parts he want to make changes in styles, content or anything
            that in his input show its some intructions to make modifications, a major check is to see if the content "user_input.txt" 
            include the keywords "web design", if they do not exist, you should identify the user_input as feedback and put what he said 
            into "user_feedback.txt" instead in the same filepath. If you identify it as a feedback, you MUST NOT 
            modify the "user_prompt.txt" and leave it for other agents to combine it with "user_feedback.txt" to come up with better prompt.
            
            Lastly, if you think the user is satisfied with the current status, write "SATISFIED" and enter nothing else in the "user_feedback.txt".
            
            You will be using the 'write_to_file' function, remember to split 'file_path' into the directory and file name. 
         """

        self.chatbot_writer = AssistantAgent(
            name="chatbot_writer",
            llm_config=self.chatbot_write_config,
            system_message=CHATBOT_WRITING_AGENT_MESSAGE
        )

        CHATBOT_REVIEW_AGENT_SYSTEM_MESSAGE = """
            As a reviewer, critically evaluate the 'user_feedback.txt' and 'user_prompt.txt' to see if the users request has been place into
            correct document for future steps. The context within these files should be coherent, relevant, and could even be identical to the original user input.
            Look at 'user_input.txt' and look for the exact phrase "web design". If this phrase "web design" does not exist in the 'user_input.txt',
            this user input should immediately be identified as a feedback and placed in the 'user_feedback.txt' and the following instructions could then be ignored.
            
            The following is instructions given to the chatbot writer, if you do not agree with his decisions, tell other agents and talk each other out about
            whose decision is better.
            
            "You are responsible to write the group decision into respective files, there are 3 cases, user looking for a new design, user providing a 
            feedback, or user is satisfied. 
            
            If you think the the user is look for a new design, put all he said into "user_prompt.txt" in the same filepath.
            Also, write "FALSE" and nothing else in the "user_feedback.txt" if you identify the user input as a new prompt.
            
            Secondly, if you think the user is giving us some feedback on parts he want to make changes in styles, content or anything
            that in his input show its some intructions to make modifications, a major check is to see if the content "user_input.txt" 
            include the keywords "web design", if they do not exist, you should identify the user_input as feedback and put what he said 
            into "user_feedback.txt" instead in the same filepath. If you identify it as a feedback, you MUST NOT 
            modify the "user_prompt.txt" and leave it for other agents to combine it with "user_feedback.txt" to come up with better prompt.
            
            Lastly, if you think the user is satisfied with the current status, write "SATISFIED" and enter nothing else in the "user_feedback.txt"."
            Ensure that in the file "user_feedback.txt" has only one line and no '\n' at the end.
                    
            Use the 'read_file' function to access the updated content, splitting 'file_path' as needed. Provide feedback or suggest improvements to 
            ensure high-quality stubs. Make sure that the written stubs do not conflate and halluciate on the contents of the other relevant files. 
            To this end, you may want to look into the contents of the other files. Provide suggestions to the chatbot_writerto ensure that the stubs 
            are accurate and relevant to the high-level task.
            
            If you think all the files are good to go, reply with 'done'. Tell the other agents to do the same. If all other agents have replied 'done'.
        """
        
        #IF you are unable to retrieve the information from the file, use the prompt from variable temp_prompt which is also the start message of group chat. 
            
          

        self.chatbot_reviewer = AssistantAgent(
            name="chatbot_reviewer",
            llm_config=self.chatbot_read_config,
            system_message=CHATBOT_REVIEW_AGENT_SYSTEM_MESSAGE
        )
    
    def user_decision(self, file_path, high_level_task):
        # Logic to write stubs based on the high_level_task
        # Use the agents to read file contents and write stubs as needed.
        
        self.chatbot_groupchat = GroupChat(
            agents=[self.client, self.chatbot_reader, self.chatbot_writer, self.chatbot_reviewer], messages=[], max_round=20
        )
        
        manager = GroupChatManager(groupchat=self.chatbot_groupchat, llm_config=self.base_config)
        
        PROMTENHANCE_PROMPT = """
            Our high-level task, '{high_level_task}', involves working across multiple files included in the high level task description. 
            Currently, focus on identifying what our user is looking for in '{file_path}'. Update related files in the filepath with the 
            user input accurately.
        """
        
        self.client.initiate_chat(
            manager,
            #message = self.temp_prompt
            message=PROMTENHANCE_PROMPT.format(high_level_task=high_level_task, file_path=file_path)
        )
        
        # Return success message or any relevant output
        return manager.last_message(agent=self.chatbot_reviewer)["content"]
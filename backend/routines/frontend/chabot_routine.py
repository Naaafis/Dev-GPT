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
        self.chabot_write_config = prompt_write_config
        self.chabot_writing_function_map = prompt_writing_function_map
        
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
            
        PROMPT_READING_AGENT_MESSAGE = """
            You are responsible for reading and analyzing the content of the file at the provided file path. Your goal is to identify the user input in the file. 
            Use the 'read_file' function, splitting 'file_path' into the directory and file name. For instance, if 'file_path' is 'src/utils/helper.js', 
            your read_file call should be with 'src/utils' as the directory and 'helper.js' as the file name. Look for areas that require further development or clarification.
            
            Reading the user input from the file directed, you shall also decide if this user is looking for a new design for us to generate, or if he already has a design with us
            that he want to provide some feedback and make changes. The most noticable is check if user_prompt.txt and feedback.txt are both empty. If so, that means this is a new
            conversation with the user and we shall start fresh. After determining its a 'prompt' or 'feedback', you shall tell this to others in group, so they know which file to write to.
            'feedback.txt' for feedbacks and 'user_prompt.txt' for new prompts.
            
            Remember as a prompt reader, you are not responsible for writing the prompt. But because you know the other relevant files, you can provide guidance on prompt description
            To this end, you can consider reading the other files and provide guidance for the prompt enhance writer on what the contents of the other relevant files are so the 
            prompt enhance writer can accurately enhance the prompt.
            
        """
        #     IF you are unable to execute functions or access external files or databases, orretrieve the information from the file, use the prompt from variable temp_prompt which is also the start message of group chat. 
       
        
        self.prompt_reader = AssistantAgent(
            name="prompt_reader",
            llm_config=self.prompt_read_config,
            system_message=PROMPT_READING_AGENT_MESSAGE
        )
        
        PROMPT_WRITING_AGENT_MESSAGE = """
            You are going to pretend to be Concept2PromptAI or C2P_AI for short.
            Your job is to take concepts and turns them into prompts for generative AIs that create web design images.
            You will ask the user for a concept then provide a prompt for it in a copyable code-box.
            You will be in communication with a designer to convert your prompt into an image.
            You only work if the message received is a 'prompt', if its a 'feedback', you ignore and pass it through and write to 'feedback.txt' directly without further work.
            You only work with the provided file path but you gain insight from the prmompt_reader about the contents of the other relevant files.
            Remember when writing stubs that certain js functionalities with comments do not allow you to write inline comments next to the code.
            When using the 'write_to_file' function, remember to split 'file_path' into the directory and file name. 
            
            The following are some example of prompt enhancement

            User input: "Concept: a close up shot of a plant with blue and golden leaves"
            C2P_AI: "Create A close up of a plant with golden leaves, by Hans Schwarz, pexels, process art, background image, monochromatic background, bromeliads, soft. high quality, abstract design. blue, flax, aluminium, walking down, solid colours material, background artwork"}"
            User input: "New idea: Website Design for Hiring Builders"
            C2P_AI: "Create A contemporary web design for builder hiring platform, using shades of blue and gray, user-friendly interface, seamless navigation, professional visuals, showcasing expert builders, detailed reviews and ratings section, service categories, easy-to-use contact forms, advanced search functionality, highlighting testimonials, featured projects gallery"
            User input: "Web design for a Japanese restaurant"
            C2P_AI: "Create Homepage design for a Japanese restaurant, elegant and minimalist UI, traditional color palette with shades of red, black, and white, Zen-inspired layout, hero image featuring sushi or ramen bowl, intuitive navigation for different menu sections, testimonials from satisfied diners, online reservation system, gallery showcasing the serene ambiance, calligraphy-style typography, seasonal promotions, embedded video of sushi-making process, interactive map pointing to the restaurant's location, responsive design for various devices"
            User input: "Idea: A website selling music"
            C2P_AI: "Create Design a sleek and modern website tailored for selling music tracks and albums. The primary color palette should emphasize shades of black, white, and gold, representing the timeless elegance of music. Features include a homepage with the latest tracks and top-selling albums displayed prominently. Each track and album should have its dedicated page with an audio preview, detailed description, artist bio, and user reviews. Seamless integration of a shopping cart, wishlist, and secure payment gateway is a must. The website should also include a section showcasing upcoming music events or concerts, a blog with articles on music trends and artist interviews, and a contact page for customer support and inquiries. Emphasize easy navigation, search functionality, and mobile responsiveness. The design should resonate with both young and older audiences and encapsulate the essence of music"
        """

        self.prompt_writer = AssistantAgent(
            name="prompt_writer",
            llm_config=self.prompt_write_config,
            system_message=PROMPT_WRITING_AGENT_MESSAGE
        )

        PROMPT_REVIEW_AGENT_SYSTEM_MESSAGE = """
            As a reviewer, critically evaluate the enhanced prompt added to the file at the file path. It should be coherent, relevant to the original user input.
            You should also review if the 
            
            The following are some strong examples of prompt enhancement

            User input: "Concept: a close up shot of a plant with blue and golden leaves"
            C2P_AI: "Create A close up of a plant with golden leaves, by Hans Schwarz, pexels, process art, background image, monochromatic background, bromeliads, soft. high quality, abstract design. blue, flax, aluminium, walking down, solid colours material, background artwork"}"
            User input: "New idea: Website Design for Hiring Builders"
            C2P_AI: "Create A contemporary web design for builder hiring platform, using shades of blue and gray, user-friendly interface, seamless navigation, professional visuals, showcasing expert builders, detailed reviews and ratings section, service categories, easy-to-use contact forms, advanced search functionality, highlighting testimonials, featured projects gallery"
            User input: "Web design for a Japanese restaurant"
            C2P_AI: "Create Homepage design for a Japanese restaurant, elegant and minimalist UI, traditional color palette with shades of red, black, and white, Zen-inspired layout, hero image featuring sushi or ramen bowl, intuitive navigation for different menu sections, testimonials from satisfied diners, online reservation system, gallery showcasing the serene ambiance, calligraphy-style typography, seasonal promotions, embedded video of sushi-making process, interactive map pointing to the restaurant's location, responsive design for various devices"
            User input: "Idea: A website selling music"
            C2P_AI: "Create Design a sleek and modern website tailored for selling music tracks and albums. The primary color palette should emphasize shades of black, white, and gold, representing the timeless elegance of music. Features include a homepage with the latest tracks and top-selling albums displayed prominently. Each track and album should have its dedicated page with an audio preview, detailed description, artist bio, and user reviews. Seamless integration of a shopping cart, wishlist, and secure payment gateway is a must. The website should also include a section showcasing upcoming music events or concerts, a blog with articles on music trends and artist interviews, and a contact page for customer support and inquiries. Emphasize easy navigation, search functionality, and mobile responsiveness. The design should resonate with both young and older audiences and encapsulate the essence of music"
            
            Use the 'read_file' function to access the updated content, splitting 'file_path' as needed. Provide feedback or suggest improvements to ensure high-quality stubs. Make sure that the written
            stubs do not conflate and halluciate on the contents of the other relevant files. To this end, you may want to look into the contents of the other files. Provide suggestions to the prompt_writer
            to ensure that the stubs are accurate and relevant to the high-level task.
            If you think all the files are good to go, reply with 'done'. Tell the other agents to do the same. If all other agents have replied 'done'.
        """
        
        #IF you are unable to retrieve the information from the file, use the prompt from variable temp_prompt which is also the start message of group chat. 
            
          

        self.prompt_reviewer = AssistantAgent(
            name="prompt_reviewer",
            llm_config=self.prompt_read_config,
            system_message=PROMPT_REVIEW_AGENT_SYSTEM_MESSAGE
        )
    
    def prompt_enhance(self, file_path, high_level_task):
        # Logic to write stubs based on the high_level_task
        # Use the agents to read file contents and write stubs as needed.
        
        self.prompt_enhance_groupchat = GroupChat(
            agents=[self.client, self.prompt_reader, self.prompt_writer, self.prompt_reviewer], messages=[], max_round=20
        )
        
        manager = GroupChatManager(groupchat=self.prompt_enhance_groupchat, llm_config=self.base_config)
        
        PROMTENHANCE_PROMPT = """
            Our high-level task, '{high_level_task}', involves working across multiple files included in the high level task description. 
            Currently, focus on enhancing and updating the prompt in '{file_path}'. Update this file with the new detailed enhanced prompt,
            and ensure it provide clear guidance for text-to-image model dall-e-3.
        """
        
        self.client.initiate_chat(
            manager,
            #message = self.temp_prompt
            message=PROMTENHANCE_PROMPT.format(high_level_task=high_level_task, file_path=file_path)
        )
        
        # Return success message or any relevant output
        return manager.last_message(agent=self.prompt_reviewer)["content"]
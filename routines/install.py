import os
from autogen import *
from config.prompts import *

class InstallRoutine():
    """Install all necessary node packages based on plan."""
    def __init__(self, base_config, install_config, install_function_map):
        self.base_config = base_config
        termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

        self.client = UserProxyAgent(
            name="client",
            is_termination_msg=termination_msg,
            function_map=install_function_map,
            human_input_mode="NEVER",
            code_execution_config={"work_dir": "API-Galore"},
        )

        self.installer = AssistantAgent(
            name="installer",
            is_termination_msg=termination_msg,
            llm_config=base_config,
            system_message=INSTALL_AGENT_SYSTEM_MESSAGE
        )

        self.reviewer = AssistantAgent(
            name="reviewer",
            is_termination_msg=termination_msg,
            llm_config=base_config,
            system_message=INSTALL_REVIEWER_SYSTEM_MESSAGE
        )

        self.executor = AssistantAgent(
            name="executor",
            llm_config=install_config,
            system_message=INSTALL_EXECUTOR_SYSTEM_MESSAGE
        )

    def find_dependencies(self, plan):
        groupchat = GroupChat( 
            agents=[self.client, self.installer, self.reviewer, self.executor], messages=[], max_round=15
        )

        manager = GroupChatManager(groupchat=groupchat, llm_config=self.base_config)
        self.client.initiate_chat(
            manager,
            message=INSTALL_PROMPT.format(plan=plan)
        )

    def install_dependenies(self, react_manager):
        file="install.txt"
        file_path = os.path.join(react_manager.get_react_app_directory(), file)
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            react_manager.controller.execute_command(line)
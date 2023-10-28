from reactManager import ReactAppManager
import openai
from autogen import *
from functions import *
from prompts import *
from util import ExecutorGroupchat

class PlanningRoutine:
    def __init__(self, base_config, plan_config, plan_function_map):
        self.base_config = base_config
        self.plan_config = plan_config
        self.termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

        self.client = UserProxyAgent(
            name="client",
            max_consecutive_auto_reply=2,
            is_termination_msg=self.termination_msg,
            function_map=plan_function_map,
            human_input_mode="NEVER",
            default_auto_reply=PLAN_CLIENT_AUTO_REPLY,
            code_execution_config={"work_dir": "API-Galore"},
        )

        self.executor = AssistantAgent(
            name="executor",
            llm_config=self.plan_config,
            system_message=PLAN_EXECUTOR_SYSTEM_MESSAGE
        )

        self.planner = AssistantAgent(
            name="planner",
            is_termination_msg=self.termination_msg,
            llm_config=self.base_config,
            system_message=PLAN_AGENT_SYSTEM_MESSAGE
        )

        self.reviewer = AssistantAgent(
            name="reviewer",
            is_termination_msg=self.termination_msg,
            llm_config=self.base_config,
            system_message=PLAN_REVIEWER_SYSTEM_MESSAGE
        )

    def init_plan(self, user_prompt):
        groupchat = ExecutorGroupchat( 
            agents=[self.client, self.planner, self.reviewer, self.executor], messages=[], max_round=15, 
            dedicated_executor = self.client
        )

        manager = GroupChatManager(groupchat=groupchat, llm_config=self.base_config)
        self.client.initiate_chat(
            manager,
            message=user_prompt
        )

    def modularize_step(self, task_num):
        groupchat = ExecutorGroupchat( 
            agents=[self.client, self.planner, self.reviewer, self.executor], messages=[], max_round=5, 
            dedicated_executor = self.client
        )

        manager = GroupChatManager(groupchat=groupchat, llm_config=self.base_config)
        self.client.initiate_chat(
            manager,
            message=PLAN_ITR_STEP_PROMPT.format(step=task_num)
        )

class CodingRoutine:
    def __init__(self, base_config, code_config, code_function_map):
        self.base_config = base_config
        self.code_config = code_config
        self.termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

        self.client = UserProxyAgent(
            name="client",
            max_consecutive_auto_reply=5,
            is_termination_msg=self.termination_msg,
            function_map=code_function_map,
            human_input_mode="NEVER",
            code_execution_config={"work_dir": "API-Galore"},
        )

        self.executor = AssistantAgent(
            name="executor",
            llm_config=self.code_config,
            system_message="As the team creates and revises code for a file, ask the client to record the code VERBATIM" +
                "in an appropriately named file in the react directory. You have access to functions for creating, " +
                "reading and writing to files. You also have functions to understand the file structure of the " +
                "entire react directory. Use these functions to provide relevant information about the current state " +
                "of the project and files within it as the engineers need it. "
        )

        self.coder1 = AssistantAgent(
            name="coder1",
            is_termination_msg=self.termination_msg,
            llm_config=self.base_config,
            # the default system message of the AssistantAgent is overwritten here
            system_message="You are a senior software engineer on the team building a react project. Your job is understand the task and " +
                "any subtasks given to you and generate code addressing each step. Consider the most effective design choices and "
                "use react best practices when writing the code. However, prioritize delivering functional code. You will be working " +
                "in a team with other engineers, code reviewers, and subject matter experts to bring the client's idea to life " +
                "In summary, your only job is to work collaboratively to translate the natural language write psuedo code into working code. "
        )

        self.coder2 = AssistantAgent(
            name="coder2",
            is_termination_msg=self.termination_msg,
            llm_config=self.base_config,
            # the default system message of the AssistantAgent is overwritten here
            system_message="You are a junior software engineer on the team building a react project. Your job is understand the task and " +
                "any subtasks given to you and generate code addressing each step. Consider the most effective design choices and "
                "use react best practices when writing the code. However, prioritize delivering functional code. You will be working " +
                "in a team with other engineers, code reviewers, and subject matter experts to bring the client's idea to life " +
                "In summary, your only job is to work collaboratively to translate the natural language write psuedo code into working code. "
        )

        self.react_sme = AssistantAgent(
            name="reviewer",
            is_termination_msg=self.termination_msg,
            llm_config=self.base_config,
            # the default system message of the AssistantAgent is overwritten here
            system_message="You are a reviewer on the planning team. You are tasked with providing feedback to the planner to improve the plan. " +
                "Ensure that the plan meets the user's requirements and the plan does not contain any code snippets. "
        )

        self.reviewer = AssistantAgent(
            name="reviewer",
            is_termination_msg=self.termination_msg,
            llm_config=self.base_config,
            # the default system message of the AssistantAgent is overwritten here
            system_message="You are a reviewer on the planning team. You are tasked with providing feedback to the planner to improve the plan. " +
                "Ensure that the plan meets the user's requirements and the plan does not contain any code snippets. "
        )

    def iter(self, user_prompt):
        groupchat = ExecutorGroupchat( 
            agents=[self.client, self.planner, self.reviewer, self.executor], messages=[], max_round=30, 
            dedicated_executor = self.client
        )

        manager = GroupChatManager(groupchat=groupchat, llm_config=self.base_config)
        self.client.initiate_chat(
            manager,
            message=user_prompt
        )



class SMEAgent:
    def __init__(self, llm_config, termination_msg):
        self.assistant = AssistantAgent(
            name="sme",
            is_termination_msg=termination_msg,
            llm_config=llm_config,
            # the default system message of the AssistantAgent is overwritten here
            system_message="You are a subject matter expert on the team. You have been given a url to some documentation " +
                "and are tasked with providing further context about that documentation to anybody on your team who may ask."
        )
        # self.retrieval = RetrieveUserProxyAgent(
        #     name="sme_user",
        #     max_consecutive_auto_reply=0,  # terminate without auto-reply
        #     human_input_mode="NEVER",
        #     retrieve_config={
        #         task: "qa",
        #         docs_path: docs_url
        #     }
        # )

    def ask_expert(self, requirements):
        pass

class Builder:
    def __init__(self, api_key, app_name, user_prompt):
        self.app_name = app_name
        self.user_prompt = user_prompt
        self.config_list = [ { 'model': 'gpt-4', 'api_key': api_key } ]
        self.base_config = {
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }

        self.init_react_manager()
        self.planner = PlanningRoutine(self.base_config, self.plan_config, self.plan_function_map)

    def build(self):
        self.planner.init_plan(self.user_prompt)

    def init_react_manager(self):
        self.react_manager = ReactAppManager(self.app_name)

        self.plan_function_map={
            "read_plan": self.react_manager.read_file,
            "create_plan": self.react_manager.create_new_file,
            "write_to_plan": self.react_manager.write_to_file,
            "insert_into_plan": self.react_manager.insert_into_file,
            "delete_lines": self.react_manager.delete_lines,
        }

        self.plan_config = {
            "functions": plan_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }

        self.write_function_map={
            "create_directory": self.react_manager.create_directory,
            "read_file": self.react_manager.read_file,
            "create_file": self.react_manager.create_new_file,
            "write_to_file": self.react_manager.write_to_file,
            "insert_into_file": self.react_manager.insert_into_file,
            "delete_lines": self.react_manager.delete_lines,
        }

        self.write_config = {
            "functions": write_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }


def main():
    builder = Builder("YOUR_API_KEY", "my_app", "Recreate google maps with just the api.")
    builder.build()

if __name__ == "__main__":
    main()


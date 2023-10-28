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

    def expand_step(self, step_num):
        groupchat = ExecutorGroupchat( 
            agents=[self.client, self.planner, self.reviewer, self.executor], messages=[], max_round=5, 
            dedicated_executor = self.client
        )

        manager = GroupChatManager(groupchat=groupchat, llm_config=self.base_config)
        self.client.initiate_chat(
            manager,
            message=PLAN_ITER_STEP_PROMPT.format(step=step_num)
        )

class CodingRoutine:
    def __init__(self, base_config, code_config, code_function_map):
        self.base_config = base_config
        self.code_config = code_config
        self.termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

        self.client = UserProxyAgent(
            name="client",
            max_consecutive_auto_reply=3,
            is_termination_msg=self.termination_msg,
            function_map=code_function_map,
            human_input_mode="NEVER",
            default_auto_reply=CODE_CLIENT_AUTO_REPLY,
            code_execution_config=False,
        )

        self.executor = AssistantAgent(
            name="executor",
            llm_config=self.code_config,
            system_message=CODE_EXECUTOR_SYSTEM_MESSAGE
        )

        self.coder = AssistantAgent(
            name="coder",
            is_termination_msg=self.termination_msg,
            llm_config=self.base_config,
            # the default system message of the AssistantAgent is overwritten here
            system_message=CODE_AGENT_SYSTEM_MESSAGE
        )

        self.reviewer = AssistantAgent(
            name="reviewer",
            is_termination_msg=self.termination_msg,
            llm_config=self.base_config,
            # the default system message of the AssistantAgent is overwritten here
            system_message=CODE_REVIEWER_SYSTEM_MESSAGE
        )

    def init_code(self, step, step_str):
        groupchat = ExecutorGroupchat( 
            agents=[self.client, self.coder, self.reviewer, self.executor], messages=[], max_round=20, 
            dedicated_executor = self.client
        )

        manager = GroupChatManager(groupchat=groupchat, llm_config=self.base_config)
        self.client.initiate_chat(
            manager,
            message=CODE_ITER_STEP_PROMPT.format(step=step, step_str=step_str)
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
        self.coder = CodingRoutine(self.base_config, self.code_config, self.code_function_map)

    def build(self):
        #self.planner.init_plan(self.user_prompt)
        plan_items = self.react_manager.get_plan_items()
        if not plan_items:
            print("PLAN ROUTINE")
            self.planner.init_plan(self.user_prompt)

        print("CODE ROUTINE")
        #for t in range(len(plan_items)):
        step = plan_items[1]
        step_str = "\n".join(step)
        for sub in range(1, len(step)):
            self.coder.init_code(step[sub], step_str)
        print("DONE")


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

        self.code_function_map={
            "create_directory": self.react_manager.create_directory,
            "read_file": self.react_manager.read_file,
            "create_file": self.react_manager.create_new_file,
            "write_to_file": self.react_manager.write_to_file,
            "insert_into_file": self.react_manager.insert_into_file,
            "delete_lines": self.react_manager.delete_lines,
        }

        self.code_config = {
            "functions": code_functions,
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


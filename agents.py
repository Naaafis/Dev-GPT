from reactManager import ReactAppManager
import openai
from autogen import *
from functions import *
from util import ExecutorGroupchat

class PlanningRoutine:
    def __init__(self, base_config, plan_config, plan_function_map):
        self.base_config = base_config
        self.plan_config = plan_config
        self.termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

        self.client = UserProxyAgent(
            name="client",
            max_consecutive_auto_reply=5,
            is_termination_msg=self.termination_msg,
            function_map=plan_function_map,
            human_input_mode="NEVER",
            code_execution_config={"work_dir": "API-Galore"},
        )

        self.executor = AssistantAgent(
            name="executor",
            llm_config=self.plan_config,
            system_message="As the planner creates and revises the plan, ask the client to record the plan VERBATIM" +
                "in a file called plan.txt at the highest level directory project. Include every minor and major step of the plan in  " +
                " a seperate line, indenting nested steps accordingly."
        )

        self.planner = AssistantAgent(
            name="planner",
            is_termination_msg=self.termination_msg,
            llm_config=self.base_config,
            # the default system message of the AssistantAgent is overwritten here
            system_message="You are the product manager on a team building a react project. Your job is break down the client's idea into " +
                "a step by step set of instructions that a software engineer can code. Each instruction should correspond " +
                "to a single component or function that can be unit tested. If an instruction can be broken down further " +
                "into clearer instructions, do so until breaking down the instruction further would be trivial. You will " +
                "be in communication with a reviewer who will provide feedback to improve the plan " +
                "In summary, your only job is to write psuedo code in natural language to build the client's product. "
        )

        self.reviewer = AssistantAgent(
            name="reviewer",
            is_termination_msg=self.termination_msg,
            llm_config=self.base_config,
            # the default system message of the AssistantAgent is overwritten here
            system_message="You are a reviewer on the planning team. You are tasked with providing feedback to the planner to improve the plan. " +
                "Ensure that the plan meets the user's requirements and the plan does not contain any code snippets. "
        )

    def plan(self, user_prompt):
        groupchat = ExecutorGroupchat( 
            agents=[self.client, self.planner, self.reviewer, self.executor], messages=[], max_round=15, 
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
        self.planner.plan(self.user_prompt)

    def init_react_manager(self):
        self.react_manager = ReactAppManager(self.app_name)

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

def main():
    builder = Builder("YOUR_API_KEY", "my_app", "Recreate google maps with just the api.")
    builder.build()

if __name__ == "__main__":
    main()


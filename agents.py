from reactManager import ReactAppManager
import openai
import os

from autogen import *
from functions import *
from prompts import *
from util import ExecutorGroupChat

from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import chromadb

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
        groupchat = GroupChat( 
            agents=[self.client, self.planner, self.reviewer, self.executor], messages=[], max_round=15
        )

        manager = GroupChatManager(groupchat=groupchat, llm_config=self.base_config)
        self.client.initiate_chat(
            manager,
            message=user_prompt
        )

    def expand_step(self, step_num):
        groupchat = GroupChat( 
            agents=[self.client, self.planner, self.reviewer, self.executor], messages=[], max_round=5, 
            dedicated_executor = self.client
        )

        manager = GroupChatManager(groupchat=groupchat, llm_config=self.base_config)
        self.client.initiate_chat(
            manager,
            message=PLAN_ITER_STEP_PROMPT.format(step=step_num)
        )

class CodingRoutine:
    def __init__(self, base_config, code_config, code_function_map, sme_config):
        self.base_config = base_config
        self.code_config = code_config
        self.sme_config = sme_config
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

        self.sme = AssistantAgent(
            name="sme",
            is_termination_msg=self.termination_msg,
            llm_config=self.sme_config,
            # the default system message of the AssistantAgent is overwritten here
            system_message=CODE_SME_SYSTEM_MESSAGE
        )

        self.reviewer = AssistantAgent(
            name="reviewer",
            is_termination_msg=self.termination_msg,
            llm_config=self.base_config,
            # the default system message of the AssistantAgent is overwritten here
            system_message=CODE_REVIEWER_SYSTEM_MESSAGE
        )

    def init_code(self, step, step_str):
        groupchat = ExecutorGroupChat( 
            agents=[self.client, self.coder, self.executor, self.reviewer], messages=[], max_round=20,
            dedicated_executor = self.client)

        manager = GroupChatManager(groupchat=groupchat, llm_config=self.base_config)
        self.client.initiate_chat(
            manager,
            message=CODE_ITER_STEP_PROMPT.format(step=step, step_str=step_str)
        )

class SMERoutine():
    def __init__(self, base_config, docs_path="./ReactAPIDocs"):
        self.termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()
        self.ragproxyagent = RetrieveUserProxyAgent(
            name="ragproxyagent",
            is_termination_msg=self.termination_msg,
            system_message="Assistant who has extra content retrieval power for solving difficult problems.",
            human_input_mode="TERMINATE",
            max_consecutive_auto_reply=3,
            retrieve_config={
                "task": "code",
                "docs_path": docs_path, 
                "chunk_token_size": 2000,
                "model": base_config["config_list"][0]["model"],
                "client": chromadb.PersistentClient(path="/tmp/chromadb"),
                "collection_name": "groupchat",
                "get_or_create": True,
            },
            code_execution_config=False,  # we don't want to execute code in this case.
        )

    def ask_expert(self, code_block, n_results=1):
        message = SME_INPUT_QUESTION.format(code_block=code_block)
        self.ragproxyagent.n_results = n_results  # Set the number of results to be retrieved.
        # Check if we need to update the context.
        update_context_case1, update_context_case2 = self.ragproxyagent._check_update_context(message)
        if (update_context_case1 or update_context_case2) and self.ragproxyagent.update_context:
            self.ragproxyagent.problem = message if not hasattr(self.ragproxyagent, "problem") else self.ragproxyagent.problem
            _, ret_msg = self.ragproxyagent._generate_retrieve_user_reply(message)
        else:
            ret_msg = self.ragproxyagent.generate_init_message(message, n_results=n_results)
        return ret_msg if ret_msg else message


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
        self.react_sme = SMERoutine(self.base_config, docs_path="./ReactAPIDocs")

        self.init_react_manager()
        self.planner = PlanningRoutine(self.base_config, self.plan_config, self.plan_function_map)
        self.coder = CodingRoutine(self.base_config, self.code_config, self.code_function_map, self.sme_config)

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
            "read_file": self.react_manager.read_file,
            "create_file": self.react_manager.create_new_file,
            "write_to_file": self.react_manager.write_to_file,
            "insert_into_file": self.react_manager.insert_into_file,
            "delete_lines": self.react_manager.delete_lines,
            "ask_react_expert": self.react_sme.ask_expert
        }

        self.code_config = {
            "functions": code_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }

        self.sme_config = {
            "functions": sme_functions,
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


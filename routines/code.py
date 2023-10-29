from autogen import *
from config.functions import *
from config.prompts import *

from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import chromadb

"""
todo:
- fix bug in SME
- rethink design - single groupchat won't scale - may need multiple groupchats running concurrently making requests to each other
- add linter
- custom groupchat for control of work flow
- handle_test_report function
"""
class CodeRoutine:
    """Generate code and tests for every step in the plan."""
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
        groupchat = GroupChat( 
            agents=[self.client, self.coder, self.executor, self.reviewer], messages=[], max_round=20
        )

        manager = GroupChatManager(groupchat=groupchat, llm_config=self.base_config)
        self.client.initiate_chat(
            manager,
            message=CODE_ITER_STEP_PROMPT.format(step=step, step_str=step_str)
        )

class SMEAgent():
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

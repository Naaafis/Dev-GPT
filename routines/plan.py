from autogen import *
from config.prompts import *

"""
todo:
- expand_step - in 
"""

class PlanRoutine:
    def __init__(self, base_config, plan_config, plan_function_map):
        self.base_config = base_config
        termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

        self.client = UserProxyAgent(
            name="client",
            max_consecutive_auto_reply=5,
            is_termination_msg=termination_msg,
            function_map=plan_function_map,
            human_input_mode="NEVER",
            default_auto_reply=PLAN_CLIENT_AUTO_REPLY,
            system_message=PLAN_CLIENT_SYSTEM_MESSAGE
        )

        self.executor = AssistantAgent(
            name="executor",
            llm_config=plan_config,
            system_message=PLAN_EXECUTOR_SYSTEM_MESSAGE
        )

        self.planner = AssistantAgent(
            name="planner",
            is_termination_msg=termination_msg,
            llm_config=base_config,
            system_message=PLAN_AGENT_SYSTEM_MESSAGE
        )

        self.reviewer = AssistantAgent(
            name="reviewer",
            is_termination_msg=termination_msg,
            llm_config=base_config,
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
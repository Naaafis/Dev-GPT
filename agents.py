from reactManager import ReactAppManager
import openai
from autogen import *

class PlanningAgent:
    def __init__(self, client, llm_config, termination_msg):
        self.client = client
        self.llm_config = llm_config
        self.termination_msg = termination_msg

        self.planner = AssistantAgent(
            name="planner",
            is_termination_msg=termination_msg,
            llm_config=llm_config,
            # the default system message of the AssistantAgent is overwritten here
            system_message="You are the product manager on the team. Your job is break down the client's idea into " +
                "a step by step set of instructions that a software engineer can code. Each instruction should correspond " +
                "to a single component or function that can be unit tested. If an instruction can be broken down further " +
                "into clearer instructions, do so until breaking down the instruction further would be trivial. You will " +
                "be in communication with a reviewer who will provide feedback to improve the plan " +
                "In summary, your only job is to write psuedo code in natural language to build the client's product"
        )
        self.plan_sme = AssistantAgent(
            name="plan_sme",
            is_termination_msg=termination_msg,
            llm_config=llm_config,
            # the default system message of the AssistantAgent is overwritten here
            system_message="You are a subject matter expert on the team. You have been given a url to react documentation " +
                "and are tasked with providing react specific context to the planner to improve the plan."
        )

        self.reviewer = AssistantAgent(
            name="reviewer",
            is_termination_msg=termination_msg,
            llm_config=llm_config,
            # the default system message of the AssistantAgent is overwritten here
            system_message="You are a reviewer on the planning team. You are tasked with providing feedback to the planner to improve the plan."
        )

    def plan(self, user_prompt):
        groupchat = GroupChat(
            agents=[self.client, self.planner, self.reviewer], messages=[], max_round=10
        )
        manager = GroupChatManager(groupchat=groupchat, llm_config=self.llm_config)

        self.client.initiate_chat(
            manager,
            message=user_prompt,
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
        self.user_prompt = user_prompt
        self.config_list = [ { 'model': 'gpt-4', 'api_key': api_key } ]
        self.llm_config = {
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
        self.termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

        self.client = UserProxyAgent(
            name="client",
            max_consecutive_auto_reply=3,
            is_termination_msg=self.termination_msg,
            human_input_mode="TERMINATE",
            system_message="The client who wants a specific product built.",
            code_execution_config=False,  # we don't want to execute code in this case.
        )

        self.react_manager = ReactAppManager(app_name)
        self.planner = PlanningAgent(self.client, self.llm_config, self.termination_msg)

    def process(self):
        self.planner.plan(self.user_prompt)

def main():
    builder = Builder('YOUR_API_KEY', "my_app", "Create a user profile component.")
    builder.process()

if __name__ == "__main__":
    main()




# from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# class PlanAgent:
#     def __init__(self):
#         self.planner = autogen.AssistantAgent(
#             name="planner",
#             llm_config={
#                 "temperature": 0,
#                 "config_list": config_list,
#             },
#             system_message="Your job on the team is the Product Manager. You suggest a step by step plan for the task you are given. A software engineer will then take your plan and build out the product."
#         )
#         self.planner_user = autogen.UserProxyAgent(
#             name="planner_user",
#             max_consecutive_auto_reply=0,  # terminate without auto-reply
#             human_input_mode="NEVER",
#         )
#         self.plan = ""

#     def create_plan(self, message):
#         planner_user.initiate_chat(planner, message=message)
#         self.plan = planner_user.last_message()["content"]
#         return self.plan

#     def improve_plan(self, suggestions):
#         planner_user.initiate_chat(planner, suggestions=suggestions)
#         self.plan = planner_user.last_message()["content"]
#         return self.plan

# class CodeAgent:
#     def __init__(self):
#         pass

#     def write_code(self, plan):
#         # Write the component codes (JS, HTML, CSS)
#         pass

# class DebugAgent:
#     def __init__(self):
#         pass

#     def debug_code(self, plan, ):
#         # Check for errors and instruct the Executor
#         pass

# class SMEAgent:
#     def __init__(self):
#         pass

#     def get_context(self, query):
#         # Write the component codes (JS, HTML, CSS)
#         pass

# class ExecAgent:
#     def __init__(self):
#         pass

#     def give_context(self, query):
#         # Write the component codes (JS, HTML, CSS)
#         pass

# class UserAgent:
#     def __init__(self):
#         pass

#     def give_context(self, query):
#         # Write the component codes (JS, HTML, CSS)
#         pass
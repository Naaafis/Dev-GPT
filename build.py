from reactManager import ReactAppManager

from routines.plan import PlanRoutine
from routines.install import InstallRoutine
from routines.code import CodeRoutine, SMEAgent
from routines.test import TestRoutine

from config.functions import *

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
        self.react_sme = SMEAgent(self.base_config, docs_path="./ReactAPIDocs")

        self.init_react_manager()
        self.planner = PlanRoutine(self.base_config, self.plan_config, self.plan_function_map)
        self.installer = InstallRoutine(self.base_config, self.install_config, self.install_function_map)
        self.coder = CodeRoutine(self.base_config, self.code_config, self.code_function_map, self.sme_config)

    def build(self):
        # self.planner.init_plan(self.user_prompt)
        # self.installer.find_dependencies(self.react_manager.read_file("", "plan.txt"))
        plan_items = self.react_manager.get_plan_items()
        if not plan_items:
            print("PLAN ROUTINE")
            self.planner.init_plan(self.user_prompt)

        print("CODE ROUTINE")
        #for t in range(len(plan_items)):
        step = plan_items[2]
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

        self.install_function_map={
            "create_dependency_list": self.react_manager.create_new_file
        }

        self.install_config = {
            "functions": install_functions,
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }


def main():
    builder = Builder("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", "my_app", "Recreate google maps with just the api.")
    builder.build()

if __name__ == "__main__":
    main()


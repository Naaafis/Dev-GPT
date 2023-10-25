from reactManager import ReactAppManager
import openai
import os

class GPTAgent:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate_code(self, prompt, max_tokens=150):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=max_tokens
        )
        return response.choices[0].text.strip()

class PlanningAgent:
    def __init__(self, gpt_agent, react_manager):
        self.gpt_agent = gpt_agent
        self.react_manager = react_manager

    def process_requirements(self, requirements):
        # Check if the React app already exists
        app_directory = os.path.join(self.react_manager.controller.print_working_directory(), self.react_manager.get_react_app_name())
        if not os.path.exists(app_directory):
            self.react_manager.create_react_app(self.react_manager.get_react_app_name())

        # Generate tasks using GPTAgent
        prompt = f"Given the following requirements for a React app, provide a plan of tasks to execute: {requirements}"
        plan = self.gpt_agent.generate_code(prompt)
        tasks = plan.split("\n")
        print("Planning Agent - Tasks:", tasks)
        return tasks

class CodeWritingAgent:
    def __init__(self, gpt_agent):
        self.gpt_agent = gpt_agent

    def write_code(self, initial_input):
        prompt = f"Generate React code for: {initial_input}\n```"
        code = self.gpt_agent.generate_code(prompt)
        code_snippets = [{'type': 'js', 'code': code}]  # Example format, adjust as needed
        print("Code Writing Agent - Code Snippets:", code_snippets)
        return code_snippets

class ExecutorAgent:
    def __init__(self, react_manager):
        self.react_manager = react_manager

    def execute_task(self, task, codes, action_type="coding"):
        print("Executor Agent - Task:", task)
        if action_type == "coding":
            if task == 'CreateComponent':
                results = {}
                for code_snippet in codes:
                    if code_snippet['type'] == 'js':
                        results['js'] = self.react_manager.edit_file(f'src/{code_snippet["name"]}.js', code_snippet['code'])
                    elif code_snippet['type'] == 'html':
                        results['html'] = self.react_manager.edit_file(f'public/{code_snippet["name"]}.html', code_snippet['code'])
                    elif code_snippet['type'] == 'css':
                        results['css'] = self.react_manager.edit_file(f'src/{code_snippet["name"]}.css', code_snippet['code'])
                print("Executor Agent - Coding Results:", results)
                return results
        elif action_type == "debugging":
            if task == 'edit_file':
                result = self.react_manager.edit_file(codes["filename"], codes["content"], codes.get("mode", "replace"), codes.get("line_num", None))
                print("Executor Agent - Debugging Result:", result)
                return result
            elif task == 'install_package':
                result = self.react_manager.install_npm_packages([codes["package_name"]])
                print("Executor Agent - Package Installation Result:", result)
                return result
        return "Unknown task"

class DebuggerAgent:
    def __init__(self, react_manager, gpt_agent):
        self.react_manager = react_manager
        self.gpt_agent = gpt_agent

    def debug(self, errors):
        advice = {}
        for key, error_message in errors.items():
            prompt = f"Given the error message: {error_message}, provide debugging advice."
            debug_advice = self.gpt_agent.generate_code(prompt)
            advice[key] = debug_advice
        print("Debugger Agent - Debugging Advice:", advice)
        return advice

class AutoGenAgent:
    def __init__(self, api_key):
        self.react_manager = ReactAppManager()
        self.gpt_agent = GPTAgent(api_key)
        self.planner = PlanningAgent(self.gpt_agent)
        self.writer = CodeWritingAgent(self.gpt_agent)
        self.executor = ExecutorAgent(self.react_manager)
        self.debugger = DebuggerAgent(self.react_manager, self.gpt_agent)

    def process_input(self, user_input):
        tasks = self.planner.process_requirements(user_input)
        initial_input = "Create base React app"  # Sample initial input
        codes = self.writer.write_code(initial_input)
        outputs = {}
        for task in tasks:
            execution_result = self.executor.execute_task(task, codes)
            if any("error" in res.lower() for res in execution_result.values()):
                debug_advice = self.debugger.debug(execution_result)
                debug_result = self.executor.execute_task(task, debug_advice, action_type="debugging")
                outputs[task] = debug_result
            else:
                outputs[task] = "Success"
        print("AutoGen Agent - Final Outputs:", outputs)
        return outputs

def main():
    agent = AutoGenAgent("YOUR_OPENAI_API_KEY")
    
    user_input = "Write a React component to display a user profile with deliberate mistakes."
    results = agent.process_input(user_input)
    print("Main - Results:", results)

if __name__ == "__main__":
    main()

'''
# To run the main function with a sample user input
python reactAgents.py

# As we develop more specific functions, you might have commands like:
python reactAgents.py process_input "Write a React component to display a user profile."

# Or, if you implement more specific functions within the AutoGenAgent:
python reactAgents.py create_component UserProfile
'''

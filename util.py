from autogen import GroupChat, ConversableAgent, UserProxyAgent
from dataclasses import dataclass
from bs4 import BeautifulSoup


@dataclass
class ExecutorGroupChat(GroupChat):
    dedicated_executor: UserProxyAgent = None

    def select_speaker(
        self, last_speaker: ConversableAgent, selector: ConversableAgent
    ):
        """Select the next speaker."""

        try:
            message = self.messages[-1]
            if "function_call" in message:
                return self.dedicated_executor
        except Exception as e:
            print(e)
            pass

        selector.update_system_message(self.select_speaker_msg(self.agents))
        final, name = selector.generate_oai_reply(
            self.messages
            + [
                {
                    "role": "system",
                    "content": f"Read the above conversation. Then select the next role from {self.agent_names} to play. Only return the role.",
                }
            ]
        )
        if not final:
            # i = self._random.randint(0, len(self._agent_names) - 1)  # randomly pick an id
            return self.next_agent(last_speaker)
        try:
            return self.agent_by_name(name)
        except ValueError:
            return self.next_agent(last_speaker)


def extract_main_container_html(html_file_path):
    # Read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the <main> container element
    main_container = soup.find('main')

    if main_container:
        # Create a new HTML file for the extracted content
        with open(html_file_path, 'w', encoding='utf-8') as output_file:
            # Write the main container and its contents to the new file
            output_file.write(str(main_container))

def html_to_text(input_html_path, output_text_path):
    # Load the HTML file
    with open(input_html_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all text within the HTML
    all_text = soup.get_text()

    # Store the text in the output text file with similar formatting
    with open(output_text_path, 'w', encoding='utf-8') as output_file:
        output_file.write(all_text)


def main():
    html_to_text("/Users/asilverde/Desktop/API-Galore/ReactAPIDocs/use – React.html", "/Users/asilverde/Desktop/API-Galore/ReactAPIDocs/use – React.txt")

if __name__ == "__main__":
    main()
from autogen import GroupChat, ConversableAgent, UserProxyAgent
from dataclasses import dataclass


@dataclass
class ExecutorGroupchat(GroupChat):
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
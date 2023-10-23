from midjourney import MidjourneyClient
#from image_downloader import runthis
from prompt_manager import image_prompt
import pprint

import time


def process_message(message):
    pprint.pprint(message)


def imagine(prompt):
    client = MidjourneyClient(
        name="test",
        token="DISCORD USER TOKEN",  # your discord token
        application_id="936929561302675456",  # bot application_id
        guild_id="1165849164832309420",  # your discord server id or None
        channel_id="1165849164832309423",  # your channel_id
        message_handler=process_message,
    )
    client.run()
    time.sleep(3)
    client.imagine(prompt)
    print("Prompt received, Generating...")
    time.sleep(90)
    print("A web design image is generated")
    client.interact(message_id="", label="U1")
    time.sleep(2)
    client.interact(message_id="", label="U2")
    time.sleep(2)
    client.interact(message_id="", label="U3")
    time.sleep(2)
    client.interact(message_id="", label="U4")
    time.sleep(2)
    client.close()
    
def main():
    prompt = image_prompt()
    time.sleep(5)
    imagine(prompt)
    time.sleep(3)
    #runthis()
    
if __name__ == "__main__":
    main()
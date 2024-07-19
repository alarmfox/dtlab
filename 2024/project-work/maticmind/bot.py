import os

from openai import OpenAI
from dotenv import load_dotenv

from webex_bot.models.response import Response
from webex_bot.webex_bot import WebexBot
from webex_bot.models.command import Command

load_dotenv()

bot = WebexBot( 
    teams_bot_token = os.environ.get("WEBEX_TOKEN"),
    approved_rooms = [],
)

client = OpenAI(
    api_key=os.environ.get("OPENAI_TOKEN"),
)

class Chat(Command):
    def __init__(self):
        super().__init__(
            command_keyword="chat",
            help_message="Ask something to chatGPT",
            card=None,
        )
        
    def execute(self, message, attachment_actions, activity):
        try:
            chat_completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user", 
                        "content": message.strip()
                    }
                ]
            ) 
        except:
           return "error in OpenAI token" 
        return chat_completion.choices[0].text

class Done(Command):
    def __init__(self):
        super().__init__(
            command_keyword = "done",
            help_message = "Get the report and exit the room.",
            card = None,
        )  
    def execute(self, message, attachment_actions, activity):
        # Todo: report 
        return "Incident marked as solved; everyone will get a MoM through email. The room will be destroyed in the next 24 hour. Send a message here to cancel"
    

bot.add_command(Chat())
bot.add_command(Done())
bot.run()

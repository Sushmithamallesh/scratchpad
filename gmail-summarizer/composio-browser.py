from composio import ComposioToolSet, App
import anthropic


import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
anthropic.api_key = api_key

tool = ComposioToolSet(app=App.BROWSER_TOOL)

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000,
    temperature=0,
    system="You have access to a browser tool. Use it to answer the user's question.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Use the browser to open youtube and fetch the latest Joe Rogan video. Whats the title?"
                }
            ]
        }
    ], 
    tools=tool.get_action_schemas()
)
print(message.content)



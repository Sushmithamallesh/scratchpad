from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
# Call the GPT model to generate text
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a javascript developer, skilled in explaining complex programming concepts with creative flair.",
        },
        {
            "role": "user",
            "content": "Give me react component code for a button that says hello world. Give me the code in a file called helloworld.jsx",
        },
    ],
)

print(completion.choices[0].message)
print(completion.choices[0].message.content)

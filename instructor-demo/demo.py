import instructor
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv


# Define your desired output structure
class UserInfo(BaseModel):
    name: str
    age: int


# init enviroment variable call for all api keys
load_dotenv()

# env variable for OpenAI API key
key = os.getenv("OPENAI_API_KEY")

# Patch the OpenAI client
client = instructor.from_openai(OpenAI())

# Extract structured data from natural language
user_info = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=UserInfo,
    messages=[{"role": "user", "content": "John Doe is 30 years old."}],
)

print(user_info.name)
# > John Doe
print(user_info.age)

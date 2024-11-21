import os
from pydantic import BaseModel, Field
from pydantic import BaseModel, field_validator
from typing import List
import instructor
from anthropic import Anthropic
from dotenv import load_dotenv
import requests
import base64

load_dotenv()


# class UserDetails(BaseModel):
#     name: str
#     age: int

#     @field_validator("name")
#     @classmethod
#     def validate_name(cls, v):
#         if v.upper() != v:
#             raise ValueError("Name must be in uppercase.")
#         return v


# client = instructor.from_anthropic(Anthropic())
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

url = "https://utfs.io/f/fe55d6bd-e920-4a6f-8e93-a4c9dd851b90-eivhb2.png"
image_data = requests.get(url).content

# Convert the image data to base64
image_base64 = base64.b64encode(image_data).decode("utf-8")
model = client.messages.create(
    model="claude-3-haiku-20240307",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract the clours in this image"},
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_base64,
                    },
                },
            ],
        },
    ],
    max_tokens=1024,
)


# {
#     "role": "user",
#     "content": [
#         {
#             "type": "image",
#             "source": {
#                 "type": "base64",
#                 "media_type": "image/jpeg",
#                 "data": "/9j/4AAQSkZJRg...",
#             },
#         },
#         {"type": "text", "text": "What is in this image?"},
#     ],
# }
print(model)

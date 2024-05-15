import instructor
import os
from instructor import Partial
from openai import OpenAI
from pydantic import BaseModel, field_validator
from typing import Iterable, List
from rich.console import Console
from dotenv import load_dotenv

load_dotenv()

client = instructor.from_openai(OpenAI())


class UserDetails(BaseModel):
    name: str
    age: int

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if v.upper() != v:
            raise ValueError("Name must be in uppercase.")
        return v


model = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=UserDetails,
    max_retries=2,
    messages=[
        {"role": "user", "content": "Extract jason is 25 years old"},
    ],
)

assert model.name == "JASON"

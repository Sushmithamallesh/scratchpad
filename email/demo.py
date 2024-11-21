import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


def generate_crew_ai_response(prompt, api_key, model="gpt-3.5-turbo"):
    """
    Generate a response based on a text prompt using OpenAI's GPT model.

    Parameters:
    - prompt (str): The text prompt to generate the response from.
    - api_key (str): Your OpenAI API key.
    - model (str): The model to use for text generation. Default is "gpt-3.5-turbo".

    Returns:
    - response_text (str): The generated response text.
    """
    client = OpenAI(api_key=api_key)
    response = client.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    response_text = response.choices[0].text.strip()
    return response_text


prompt = "crew ai"
response_text = generate_crew_ai_response(prompt, api_key)
print(response_text)

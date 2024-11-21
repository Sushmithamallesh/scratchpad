from openai import OpenAI
import os
from dotenv import load_dotenv


def generate_image(prompt, api_key, model="image-alpha-001"):
    """
    Generate an image based on a text prompt using OpenAI's image generation model.

    Parameters:
    - prompt (str): The text prompt to generate the image from.
    - api_key (str): Your OpenAI API key.
    - model (str): The model to use for image generation. Default is "image-alpha-001".

    Returns:
    - image_url (str): The URL of the generated image.
    """
    client = OpenAI(api_key=api_key)
    response = client.images.generate(
        model="dall-e-3",
        prompt="A cartoon depiction in black and white of a young princess born in the erstwhile vijayanagara empire",
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url

    return image_url


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
prompt = "A futuristic cityscape at sunset"
image_url = generate_image(prompt, api_key)
print(image_url)

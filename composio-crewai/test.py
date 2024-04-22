import os
import anthropic
from dotenv import load_dotenv

# Example usage


anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
reoly = anthropic_client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, world"}],
)

print(reoly)

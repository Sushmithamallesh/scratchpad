from pydantic_ai import Agent
from dotenv import load_dotenv
load_dotenv()


# Define a very simple agent including the model to use, you can also set the model when running the agent.
agent = Agent(
    'openai:gpt-4',
    # Register a static system prompt using a keyword argument to the agent.
    # For more complex dynamically-generated system prompts, see the example below.
    system_prompt='Be concise, reply with one sentence.',
    Tool=[
        Tool(
            name="get_altitude",
            description="Get the altitude of the highest peak in the world",
            func=get_altitude,
        )
    ]
)

# Run the agent synchronously, conducting a conversation with the LLM.
# Here the exchange should be very short: PydanticAI will send the system prompt and the user query to the LLM,
# the model will return a text response. See below for a more complex run.
result = agent.run_sync('Whats the altitude of the highest peak in the world?')
print(result.data)
"""
"""
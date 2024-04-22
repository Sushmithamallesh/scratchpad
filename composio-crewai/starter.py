import time
import uuid
import anthropic
import chromadb
from crewai import Agent, Task
from langchain_openai import ChatOpenAI
import cohere

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up API keys
cohere_api_key = os.getenv("COHERE_API_KEY")  # Cohere API key
openai_key = os.getenv("OPEN_AI_API_KEY")  # OpenAI API key
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")  # Anthropic API key
llm = ChatOpenAI(openai_api_key=openai_key)
co = cohere.Client(cohere_api_key)

# Get All the tools

# check if the tools file is empty or not if not then write the tools to the file
# todo: there are mnay tools so this just a demo

dir_name = "toolsetdata"
if not os.path.exists(dir_name):
    os.makedirs(dir_name)


# tool_name = App.GITHUBLARGEBETA.name.lower()
tool_name = "githublargebeta"
file_name = "{}/{}.txt".format(dir_name, tool_name)
# if not os.path.exists(file_name):
#     tools = ComposioToolset(apps=[App.GITHUBLARGEBETA])
#     with open(file_name, "w") as f:
#         for tool in tools:
#             f.write(str(tool) + "\n")

# get the contents of the file
with open(file_name, "r") as f:
    tools = f.readlines()

chroma_client = chromadb.PersistentClient(path="vector.chroma")
try:
    collection = chroma_client.get_collection(tool_name)
except Exception as e:
    print(f"Error while getting collection: {e}")
    collection = chroma_client.create_collection(name=tool_name)
    print(f"Collection created: {collection.name}")
    # do sentence level chunking
    for tool in tools:
        tool = tool.strip()
        if tool:
            try:
                # call cohere to get the embeddings
                cohere_embeddings_response = co.embed(
                    texts=[tool],
                    model="embed-english-v3.0",
                    input_type="search_document",
                )

            except Exception as e:
                if isinstance(e, cohere.errors.TooManyRequestsError):
                    print("Rate limit error, retrying...")
                    # If rate limited, sleep for 60 seconds (or however long you want to wait)
                    time.sleep(60)

                    # Then retry the request
                    cohere_embeddings_response = co.embed(
                        texts=[tool],
                        model="embed-english-v3.0",
                        input_type="classification",
                    )
                else:
                    print("Some embed error that is not too many requests ")
            # store embeddings in chroma
            try:
                embeddings = cohere_embeddings_response.embeddings[0]
                collection.add(
                    ids=str(uuid.uuid4()),
                    embeddings=embeddings,
                    metadatas=[{"text": tool}],
                )
            except Exception as e:
                print(f"Error while adding to chroma: {e}")
                collection.delete()
                exit()
            else:
                print(f"Embeddings added to collection: {collection.name}")

query = "How to create a pull request in github?"
query = query.strip()
# embed the question
query_embedding = co.embed(
    texts=[query], model="embed-english-v3.0", input_type="search_query"
)

# now lets query the collection with a specific question I have
results = collection.query(
    query_embeddings=query_embedding.embeddings[0],
    n_results=5,
)


context = ""

for metadatas in results["metadatas"]:
    for index, metadata in enumerate(metadatas):
        context += f"[{index}] {metadata['text']}\n"
context = context.strip()
print(context)
anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
response = anthropic_client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    system="You are a helpful assistant that explains how to use APIs",
    messages=[
        {
            "role": "user",
            "content": "What API is used for creating a pull request in github? Give responses only from the context.",
        },
        {"role": "assistant", "content": context},
    ],
)

print("Response from Anthropic:")
print(response.content)
print("")


# crewai_agent = Agent(
#     role="Github Agent",
#     goal="""You take action on Github using Github APIs""",
#     backstory="""You are AI agent that is responsible for taking actions on Github on users behalf. You need to take action on Github using Github APIs""",
#     verbose=True,
#     tools=tools,
#     llm=llm,
# )
# task = Task(
#     description="Star a repo Sushmithamallesh/sushispot on GitHub",
#     agent=crewai_agent,
#     expected_output="if the star happened",
# )

# task.execute()

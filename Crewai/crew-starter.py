import os
from crewai import Agent, Task, Crew

# Importing crewAI tools
from crewai_tools import DirectoryReadTool, FileReadTool, DirectorySearchTool
from langchain_community.agent_toolkits import GmailToolkit
from dotenv import load_dotenv

load_dotenv()
# Set up API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  # OpenAI API key

# Instantiate tools
gmail_tool = GmailToolkit()

# init agent
gmail_reader = Agent(
    role="Curator/Editor",
    goal="Answer the question",
    backstory="You are a curator/editor with a passion for technology.",
    verbose=True,
)

# writer = Agent(
#     role="Content Writer",
#     goal="Craft a file containing of the mail",
#     backstory="A skilled writer with a passion for technology.",
#     tools=[docs_tool, file_tool],
#     verbose=True,
# )

present = Task(
    description="List all the emails I have received from byrne hobart in the last 30 days.",
    expected_output="The subject of the email.",
    tools=[gmail_tool],
    agent=gmail_reader,
)

# write = Task(
#     description="Write the contents to a file",
#     expected_output="A file with the contents of email. Each email separated by a --- demarcator.",
#     agent=writer,
#     output_path="./blog-posts/summary.txt",
# )

# Assemble a crew
crew = Crew(agents=[gmail_reader], tasks=[present], verbose=2)

# Execute tasks
crew.kickoff()

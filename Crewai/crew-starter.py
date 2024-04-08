import os
from crewai import Agent, Task, Crew

# Importing crewAI tools
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
)
from langchain_community.agent_toolkits import GmailToolkit
from dotenv import load_dotenv

load_dotenv()
# Set up API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  # OpenAI API key

# Instantiate tools
docs_tool = DirectoryReadTool(directory="./blog-posts")
file_tool = FileReadTool()
gmail_tool = GmailToolkit()


# init agent
gmail_reader = Agent(
    role="Curator/Editor",
    goal="Curate and summarize the mails",
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

summarize = Task(
    description="Find the latest email in my inbox and summarize it like a curator would. The email should be in the last 3 hours. Use query paramaters to limit the number of emails to 1",
    expected_output="A summary of the email.",
    tools=gmail_tool.get_tools(),
    agent=gmail_reader,
)

# write = Task(
#     description="Write the contents to a file",
#     expected_output="A file with the contents of email. Each email separated by a --- demarcator.",
#     agent=writer,
#     output_path="./blog-posts/summary.txt",
# )

# Assemble a crew
crew = Crew(agents=[gmail_reader], tasks=[summarize], verbose=2)

# Execute tasks
crew.kickoff()

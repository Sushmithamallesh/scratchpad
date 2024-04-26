import os
from crewai_tools import ScrapeWebsiteTool
from crewai import Agent, Task, Crew
from dotenv import load_dotenv

load_dotenv()
# Set up API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  # OpenAI API key

scraper = Agent(
    role="Scraper",
    goal="Scrape the website for all the useful details of the product",
    backstory="You are a scraper.",
    verbose=True,
)

# To enable scrapping any website it finds during it's execution
tool = ScrapeWebsiteTool()

# Initialize the tool with the website URL, so the agent can only scrap the content of the specified website
tool = ScrapeWebsiteTool(
    website_url="https://www.uniqlo.com/in/en/products/E470316-000?colorCode=COL51&sizeCode=SMA004"
)

scrape = Task(
    description="Scrape the website and give all the product details, what is the fabric of the product?",
    expected_output="An answer to the question.",
    tools=[tool],
    agent=scraper,
)

crew = Crew(agents=[scraper], tasks=[scrape], verbose=2)

# Execute tasks
crew.kickoff()

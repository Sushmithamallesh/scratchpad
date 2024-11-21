import praw
import os
from dotenv import load_dotenv
import anthropic
import json
import time
from time import sleep

load_dotenv()

claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# print all env variables
for key, value in os.environ.items():
    if key in [
        "REDDIT_CLIENT_ID",
        "REDDIT_CLIENT_SECRET",
        "REDDIT_USERNAME",
        "REDDIT_PASSWORD",
    ]:
        print(f"{key}: {value}")
# Init reddit instance
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="rep.ly",
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
)

print(reddit.user.me())


def is_relevant(submission, company_metadata, keywords):
    # Combine submission title and text
    content = f"{submission.title}\n\n{submission.selftext}\n\n"
    company_info = company_metadata["company_info"]
    company_url = company_metadata["company_url"]
    company_name = company_metadata["company_name"]
    # Prepare the prompt for Claude
    prompt = f"""Here is the context of what my company does {content}. 
        Here is the reddit post title {submission.title}. 
        Here is the reddit post text {submission.selftext}. 
        Here is the company info {company_info}.
        Additionally here are the keywords that I am using to search for relevant posts {keywords}.
        
        I want to determine whether this post is relevant to my company.
        I also want to determine if the post is relevant to the keywords that I am using to search for relevant posts.
        If the post is about how someone building agents usign certain tools then its relevant. 
        If the post is relevant to what my company solves for then I want to reply with an appropriate response.
        If you are responding with I had the same problem then analyse if the problem is relavent to what my company solves for.
        
        I want the respose to be very very short and to the point. 
        I want it to have URL of the company {company_url} and maybe if necessary the name of the company {company_name}.
        Here are some examples of responses:
        "Do try out {company_url}. Hope this helps!"
        "One tool I use is {company_url}. Quick and easy to use. Helps integrate with other tools in a single line of code"
        "I was able to improve the efficiency of using tools with {company_url}"
        "If you are looking for tools to help when building this check out {company_url}"
        "How was your experience using {company_name}?"
        
        Use these examples wisely if the post doesnt talk about tools and that they are facing issue with function calling or tools or efficiency then dont say I had the same problem.
        Use the context of the post very well and only write responses that are helpful and relevant while only promoting the company if its very relavant.
        If the post is not relevant to what my company solves for then say it is not relevant.
        If the post already mentions my company then ask how was your experience using {company_name}.
        
        Please respond just with a JSON object with the following keys, nothing else:
        - is_relevant: a boolean indicating whether the post is relevant to my company
        - response: a string indicating the appropriate response to the post. If the post is not relevant, please respond with None.
        """
    try:
        response = claude.completions.create(
            model="claude-2.0",
            prompt=anthropic.HUMAN_PROMPT + prompt + anthropic.AI_PROMPT,
            max_tokens_to_sample=100,
            temperature=0.7,
        )

        # Parse the JSON response
        result = json.loads(response.completion.strip())

        return result["is_relevant"], result

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Raw response: {response.completion.strip()}")
        return False, {
            "error": "JSON decode error",
            "raw_response": response.completion.strip(),
        }
    except Exception as e:
        print(f"Error in relevance check: {e}")
        return False, {"error": str(e)}


def main():
    keywords = [
        "function calling",
        "agenticai",
        "agents",
        "tool",
        "external tools",
        "external api",
        "integrations",
    ]
    subreddit = reddit.subreddit("LocalLLaMA")
    company_metadata = {
        "company_info": "Composio is a platform that empowers agents to tackle complex tasks. We offer a wide range of tools and integrations to help you get the most out of our platform.",
        "company_url": "https://composio.dev",
        "company_name": "Composio",
    }
    try:
        for submission in subreddit.search(" ".join(keywords), limit=5):
            relevant, response = is_relevant(
                submission=submission,
                company_metadata=company_metadata,
                keywords=keywords,
            )
            if relevant:
                print(
                    "--------------------------------------------------------------------------------"
                )
                print("\nRelevant submission:")
                print(f"Title: {submission.title}")
                print(f"URL: {submission.url}")
                print(f"Text: {submission.selftext}")
                print(f"Response from LLM: {response}")
                print(
                    "--------------------------------------------------------------------------------"
                )
            else:
                print(
                    "--------------------------------------------------------------------------------"
                )
                print("\nNot relevant submission:")
                print(f"Title: {submission.title}")
                print(f"URL: {submission.url}")
                print(f"Text: {submission.selftext}")
                print(f"Response from LLM: {response}")
                print(
                    "--------------------------------------------------------------------------------"
                )
            sleep(10)
    except praw.exceptions.RedditAPIException as e:
        print(f"reddit error: {e}")
    except Exception as e:
        print(f"error: {e}")


if __name__ == "__main__":
    main()

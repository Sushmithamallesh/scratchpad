import os
from pathlib import Path
import pickle
from dotenv import load_dotenv
from bs4 import BeautifulSoup, NavigableString
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI


def path_to_uri(path, scheme="https://", domain="docs.ray.io"):
    return scheme + domain + str(path).split(domain)[-1]


def extract_text_from_section(section):
    texts = []
    for elem in section.children:
        if isinstance(elem, NavigableString):
            if elem.strip():
                texts.append(elem.strip())
        elif elem.name == "section":
            continue
        else:
            texts.append(elem.get_text().strip())
    return "\n".join(texts)


def extract_sections(record):
    # Open the HTML file specified in the record
    with open(record["path"], "r", encoding="utf-8") as html_file:
        # Parse the HTML file using BeautifulSoup
        soup = BeautifulSoup(html_file, "html.parser")
    # Find all the 'section' tags in the parsed HTML
    sections = soup.find_all("section")
    # Initialize an empty list to store the sections
    section_list = []
    # Iterate over each section
    for section in sections:
        # Get the 'id' attribute of the section
        section_id = section.get("id")
        # Extract the text from the section using the helper function
        section_text = extract_text_from_section(section)
        # If the section has an 'id', add it to the list
        if section_id:
            # Convert the path to a URI
            uri = path_to_uri(path=record["path"])
            # Append the section to the list with its source URI and text
            section_list.append({"source": f"{uri}#{section_id}", "text": section_text})
    # Return the list of sections
    return section_list


# load environment variables
load_dotenv()
OPEN_AI_API_KEY = os.environ["OPENAI_AI_KEY"]

# create a chat LLM
llm = ChatOpenAI(openai_api_key=OPEN_AI_API_KEY)

EFS_DIR = Path().resolve().parent
DOCS_DIR = Path(EFS_DIR, "docs.ray.io/en/master/")


SECTIONS_FILE_PATH = Path("sections.pkl")

if Path(SECTIONS_FILE_PATH).exists():
    print("sections.pkl file already exists")
    with open(SECTIONS_FILE_PATH, "rb") as f:
        sections = pickle.load(f)
else:
    print("sections.pkl file does not exist")
    # Create a data set of documents
    ds = [{"path": path} for path in DOCS_DIR.rglob("*.html") if not path.is_dir()]

    # Extract sections
    # Use a list comprehension to apply the extract_sections function to each item in ds
    sections_ds = [extract_sections(item) for item in ds]

    # Flatten the list of lists into a single list
    sections = [item for sublist in sections_ds for item in sublist]

    print(f"Sections: {len(sections)}")

    # Store the sections in the file for future use
    with open(SECTIONS_FILE_PATH, "wb") as file:
        pickle.dump(sections, file)

print(f"Sections: {len(sections)}")
# Create an instance of RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Initialize an empty list to store the chunks
chunks = []

# Iterate over each section
for section in sections:
    # Split the section text into chunks
    section_chunks = text_splitter.split_text(section["text"])
    # Add the chunks to the list
    chunks.extend(section_chunks)

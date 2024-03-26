from bs4 import BeautifulSoup, NavigableString


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


def path_to_uri(path, scheme="https://", domain="docs.ray.io"):
    return scheme + domain + str(path).split(domain)[-1]


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

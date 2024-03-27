import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
import psycopg
from pgvector.psycopg import register_vector


def chunk_section(section, chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = text_splitter.create_documents(
        texts=[section["text"]], metadatas=[{"source": section["source"]}]
    )
    return [
        {"text": chunk.page_content, "source": chunk.metadata["source"]}
        for chunk in chunks
    ]


class StoreResults:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

    def __call__(self, batch):
        try:
            self.logger.debug(f"Storing results: {batch}")
            with psycopg.connect(
                "dbname=test_rag user=sushmithamallesh host=localhost password=postgres"
            ) as conn:
                register_vector(conn)
                with conn.cursor() as cur:
                    for text, source, embedding in zip(
                        batch["text"], batch["source"], batch["embeddings"]
                    ):
                        cur.execute(
                            "INSERT INTO document (text, source, embedding) VALUES (%s, %s, %s)",
                            (
                                text,
                                source,
                                embedding,
                            ),
                        )
            return {}
        except Exception as e:
            self.logger.error(f"Error while storing results: {e}")
            return {}

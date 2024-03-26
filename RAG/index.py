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
    def __call__(self, batch):
        print("store results")
        try:
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
            print(e)
            return {}

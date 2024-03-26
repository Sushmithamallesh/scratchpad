from functools import partial
import ray
from pathlib import Path
from chunks import EmbedChunks
from index import StoreResults, chunk_section
from data import extract_sections
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ray.data import ActorPoolStrategy
from utils import execute_bash

EFS_DIR = Path().resolve().parent
print(f"{EFS_DIR.exists()} {EFS_DIR} exists")
DOCS_DIR = Path(EFS_DIR, "docs.composio.dev/")
print(f"{DOCS_DIR.exists()} {DOCS_DIR} exists")

# Create a data set of documents
ds = ray.data.from_items(
    [{"path": path} for path in DOCS_DIR.rglob("*.html") if not path.is_dir()]
)
print(f"{ds.count()} documents")

# Extract sections
sections_ds = ds.flat_map(extract_sections)
sections = sections_ds.take_all()
print(len(sections))

chunk_size = 300
chunk_overlap = 50
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    length_function=len,
)

# Chunk a sample section
chunks_ds = sections_ds.flat_map(
    partial(chunk_section, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
)


# Embed the chunks
embedding_model_name = "thenlper/gte-base"
embedded_chunks = chunks_ds.map_batches(
    EmbedChunks,
    fn_constructor_kwargs={"model_name": embedding_model_name},
    batch_size=100,
    num_gpus=1,
    compute=ActorPoolStrategy(size=1),
)

print(f"{embedded_chunks.count()} embedded chunks")
embedded_chunks.map_batches(
    StoreResults,
    batch_size=128,
    num_cpus=1,
    compute=ActorPoolStrategy(size=1),
).count()

# Ensure the directory exists
sql_dump_dir = Path("sql_dumps")
sql_dump_dir.mkdir(parents=True, exist_ok=True)

sql_dump_fp = (
    sql_dump_dir
    / f"{embedding_model_name.split('/')[-1]}_{chunk_size}_{chunk_overlap}.sql"
)

# Save to SQL dump
database_name = "test_rag"
output, error = execute_bash(
    f"sudo -u sushmithamallesh pg_dump -c {database_name} > {sql_dump_fp}"
)
print("Updated the index!")

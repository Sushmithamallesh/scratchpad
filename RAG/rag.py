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
DOCS_DIR = Path(EFS_DIR, "docs.ray.io/en/master/")
print(f"{DOCS_DIR.exists()} {DOCS_DIR} exists")

# Create a data set of documents
ds = ray.data.from_items(
    [{"path": path} for path in DOCS_DIR.rglob("*.html") if not path.is_dir()]
)
print(f"{ds.count()} documents")

# Extract sections
sections_ds = ds.flat_map(extract_sections)
sections = sections_ds.take_all()
print(f"Sections: {len(sections)}")

chunk_size = 300
chunk_overlap = 50


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
try:
    count = embedded_chunks.map_batches(
        StoreResults,
        batch_size=128,
        num_cpus=1,
        compute=ActorPoolStrategy(size=1),
    ).count()
    print(f"Count of embedded chunks after mapping batches: {count}")
except Exception as e:
    print(f"Error while mapping batches: {e}")

# Ensure the directory exists
sql_dump_dir = Path("sql_dumps")
sql_dump_dir.mkdir(parents=True, exist_ok=True)

sql_dump_fp = (
    sql_dump_dir
    / f"{embedding_model_name.split('/')[-1]}_{chunk_size}_{chunk_overlap}.sql"
)
print(f"SQL dump file: {sql_dump_fp}")
# Save to SQL dump
database_name = "test_rag"
try:
    output, error = execute_bash(
        f"sudo -u sushmithamallesh pg_dump -c {database_name} > {sql_dump_fp}"
    )
    if error:
        raise Exception(f"Error occurred: {error}")
    print("Updated the index!")
except Exception as e:
    print(f"Failed to update the index: {e}")

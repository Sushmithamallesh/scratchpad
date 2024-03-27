from functools import partial
from pathlib import Path

import ray
from chunks import EmbedChunks
from index import chunk_section
from ray.data import ActorPoolStrategy

from data import extract_sections
import pickle
from dotenv import load_dotenv

load_dotenv()
EFS_DIR = Path().resolve().parent
DOCS_DIR = Path(EFS_DIR, "docs.ray.io/en/master/")

ds = ray.data.from_items(
    [{"path": path} for path in DOCS_DIR.rglob("*.html") if not path.is_dir()]
)
print(f"{ds.count()} documents")

# Load sections_ds from a file
sections_ds = ray.data.read_parquet("./sections")
print("Loaded sections dataset: ", sections_ds.count())

# Extract sections only if loaded_sections_ds is empty
if sections_ds.count() == 0:
    sections_ds = ds.flat_map(extract_sections)
    sections = sections_ds.take_all()
    print("Sections: ", len(sections))
    # Save sections_ds to a file
    sections_ds.write_parquet("./sections")
    print("Sections dataset saved to ./sections")

# We are chunking data into batches of 300 and overlapping by 50
chunk_size = 300
chunk_overlap = 50

chunks_ds = sections_ds.flat_map(
    partial(chunk_section, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
)
print(f"{chunks_ds.count()} chunks")
chunks_ds.show(1)


# Embed chunks
embedding_model_name = "thenlper/gte-base"
embedded_chunks = chunks_ds.map(
    EmbedChunks,
    fn_constructor_kwargs={"model_name": embedding_model_name},
    concurrency=2,
)

print(f"{embedded_chunks.count()} embedded chunks")
embedded_chunks.show(1)

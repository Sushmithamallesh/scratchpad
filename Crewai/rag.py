from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.storage import (
    LocalFileStore,
)
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings


def create_vector_db():
    # we use sentence transformer to get the vector embeddings for the database
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": False}
    hf = HuggingFaceEmbeddings(
        model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
    )

    # load all the transcripts stored in the data folder
    loader = DirectoryLoader("mails/", glob="**/*.txt", show_progress=True)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0)
    documents = text_splitter.split_documents(docs)

    # cache the embeddings for faster loadup
    fs = LocalFileStore("./cache/")
    cached_embedder = CacheBackedEmbeddings.from_bytes_store(
        hf, fs, namespace="sentence"
    )

    # create the vector db
    db = FAISS.from_documents(documents, cached_embedder)
    return db


def retrieve_documents(db, query):
    # retrieve the documents that match the query
    similarity_threshold = 0.5
    retrieved_docs = db.similarity_search(query, k=10, threshold=similarity_threshold)
    return retrieved_docs


db = create_vector_db()
retrieve_documents(db, "benefits")

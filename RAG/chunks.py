import os
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import numpy as np
from ray.data import ActorPoolStrategy


class EmbedChunks:
    def __init__(self, model_name):
        if model_name == "text-embedding-ada-002":
            self.embedding_model = OpenAIEmbeddings(
                model=model_name,
                openai_api_base=os.environ["OPENAI_AI_BASE"],
                openai_api_key=os.environ["OPENAI_AI_KEY"],
            )
        else:
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"device": "cpu", "batch_size": 100},
            )

    def __call__(self, batch):
        print("embed chunks")
        embeddings = self.embedding_model.embed_documents(batch["text"])
        return {
            "text": batch["text"],
            "source": batch["source"],
            "embeddings": embeddings,
        }

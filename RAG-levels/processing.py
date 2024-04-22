import os
from uuid import uuid4
import numpy as np
from dataclasses import dataclass
from pydantic import BaseModel, Field


class TextChunk(BaseModel):
    id: int
    text: str
    embedding: np.array
    filename: str
    uuid: str = Field(default_factory=uuid4)


def get_texts():
    source_directory = "./docs.ray.io/en/master/"
    # read the files
    for file in os.listdir(source_directory):
        if file.endswith(".html"):
            yield TextChunk(
                text=open(os.path.join(source_directory, file)).read(),
                embedding=None,
                filename=file.name,
            )


if __name__ == "__main__":
    # get texts from the files
    texts = get_texts()
    print(texts)

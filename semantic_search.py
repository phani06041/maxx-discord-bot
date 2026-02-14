import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class SemanticSearch:
    def __init__(self, chunks):
        if not chunks:
            raise ValueError(
                "SemanticSearch received empty chunks. "
                "Check manual loading and extraction."
            )

        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.chunks = chunks

        self.embeddings = self.model.encode(
            chunks, convert_to_numpy=True, show_progress_bar=True
        )

        if self.embeddings.ndim != 2:
            raise ValueError(
                f"Invalid embeddings shape: {self.embeddings.shape}"
            )

        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)

    def search(self, query, top_k=3):
        query_embedding = self.model.encode(
            [query], convert_to_numpy=True
        )

        distances, indices = self.index.search(query_embedding, top_k)
        return [self.chunks[i] for i in indices[0]]

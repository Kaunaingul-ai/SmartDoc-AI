import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class SemanticRetriever:
    """
    Create semantic embeddings for document chunks
    and retrieve the most relevant chunks for a user question.
    """

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []

    def build_index(self, chunks):
        """
        Convert document chunks into embeddings
        and store them inside a FAISS search index.
        """

        self.chunks = chunks

        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        embeddings = embeddings.astype("float32")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(embeddings)

    def search(self, question, top_k=3):
        """
        Search the indexed document and return
        the most relevant text chunks.
        """

        if self.index is None:
            raise ValueError(
                "The document index has not been created yet."
            )

        question_embedding = self.model.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        question_embedding = question_embedding.astype("float32")

        scores, indices = self.index.search(
            question_embedding,
            top_k
        )

        results = []

        for score, index in zip(scores[0], indices[0]):

            if index == -1:
                continue

            chunk = self.chunks[index]

            results.append(
                {
                    "page_number": chunk["page_number"],
                    "text": chunk["text"],
                    "score": float(score)
                }
            )

        return results
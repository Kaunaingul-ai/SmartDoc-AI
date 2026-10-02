import re

import numpy as np
from sentence_transformers import SentenceTransformer


class DocumentSummarizer:
    """
    Reliable extractive summarizer for SmartDoc AI.

    The summarizer selects the most representative
    sentences directly from the uploaded PDF instead
    of generating unsupported text.
    """

    def __init__(
        self,
        model_name="all-MiniLM-L6-v2"
    ):
        self.model = SentenceTransformer(
            model_name
        )


    def _split_into_sentences(
        self,
        text
    ):
        """
        Split document text into clean sentences.
        """

        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text
        )

        cleaned_sentences = []

        for sentence in sentences:

            sentence = sentence.strip()

            if len(sentence) >= 35:
                cleaned_sentences.append(
                    sentence
                )

        return cleaned_sentences


    def summarize_document(
        self,
        page_texts,
        max_sentences=5
    ):
        """
        Generate an extractive summary by selecting
        the most semantically representative sentences.
        """

        if not page_texts:

            return (
                "No readable text was available "
                "for summarization."
            )

        # -----------------------------------------
        # Combine document text
        # -----------------------------------------

        full_text = " ".join(
            page["text"]
            for page in page_texts
            if page["text"].strip()
        )

        sentences = self._split_into_sentences(
            full_text
        )

        if not sentences:

            return (
                "No suitable text was available "
                "for summarization."
            )

        # Short documents do not need aggressive
        # sentence selection.
        if len(sentences) <= max_sentences:

            return " ".join(
                sentences
            )

        # -----------------------------------------
        # Create document representation
        # -----------------------------------------

        document_embedding = self.model.encode(
            [full_text],
            convert_to_numpy=True,
            normalize_embeddings=True
        )[0]

        # -----------------------------------------
        # Create sentence representations
        # -----------------------------------------

        sentence_embeddings = self.model.encode(
            sentences,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        # Cosine similarity becomes dot product
        # because embeddings are normalized.
        similarity_scores = np.dot(
            sentence_embeddings,
            document_embedding
        )

        # -----------------------------------------
        # Select strongest sentences
        # -----------------------------------------

        top_indices = np.argsort(
            similarity_scores
        )[-max_sentences:]

        # Restore original document order
        top_indices = sorted(
            top_indices.tolist()
        )

        selected_sentences = [
            sentences[index]
            for index in top_indices
        ]

        summary = " ".join(
            selected_sentences
        )

        return summary
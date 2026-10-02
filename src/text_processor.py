def create_text_chunks(page_texts, chunk_size=700, overlap=120):
    """
    Split extracted PDF text into smaller overlapping chunks.

    Parameters:
        page_texts: List of dictionaries containing page number and text.
        chunk_size: Maximum number of characters in each chunk.
        overlap: Number of characters shared between consecutive chunks.

    Returns:
        chunks: List of dictionaries containing chunk text and page number.
    """

    chunks = []

    for page_data in page_texts:
        page_number = page_data["page_number"]
        text = page_data["text"]

        if not text:
            continue

        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "page_number": page_number,
                        "text": chunk_text
                    }
                )

            start += chunk_size - overlap

    return chunks

def split_text_into_chunks(
    extracted_pages,
    chunk_size=500,
    overlap=100
):
    """
    Split extracted PDF text into smaller chunks.

    Each chunk retains its original PDF page number.
    """

    chunks = []

    for page_data in extracted_pages:
        text = page_data["text"]
        page_number = page_data["page"]

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "page": page_number
                })

            if end >= len(text):
                break

            start = end - overlap

    return chunks

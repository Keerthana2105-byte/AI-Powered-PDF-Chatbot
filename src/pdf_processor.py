
from pypdf import PdfReader
from pathlib import Path


def extract_text_from_pdf(pdf_file):
    """
    Extract text from an uploaded PDF file.
    """

    reader = PdfReader(pdf_file)

    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and text.strip():
            extracted_pages.append({
                "page": page_number,
                "text": text.strip()
            })

    if not extracted_pages:
        raise ValueError(
            "No readable text found. This PDF may be scanned or image-based."
        )

    return extracted_pages


def get_pdf_info(pdf_file):
    """
    Get basic information about a PDF.
    """

    reader = PdfReader(pdf_file)

    return {
        "total_pages": len(reader.pages),
        "metadata": reader.metadata
    }

from pypdf import PdfReader


def extract_text_from_pdf(pdf_file):
    """
    Extract text from all pages of an uploaded PDF file.

    Parameters:
        pdf_file: Uploaded PDF file object.

    Returns:
        full_text: Extracted text from the PDF.
        page_texts: List containing text from each page.
        total_pages: Number of pages in the PDF.
    """

    reader = PdfReader(pdf_file)

    page_texts = []
    full_text = ""

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text:
            cleaned_text = text.strip()
            page_texts.append(
                {
                    "page_number": page_number,
                    "text": cleaned_text
                }
            )

            full_text += f"\n\n--- Page {page_number} ---\n{cleaned_text}"

    total_pages = len(reader.pages)

    return full_text.strip(), page_texts, total_pages
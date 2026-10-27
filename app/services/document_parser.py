from io import BytesIO

from pypdf import PdfReader


def extract_pdf_text(content: bytes) -> str:
    """Extract embedded text from a PDF. Scanned PDFs need OCR."""
    if not content.startswith(b"%PDF-"):
        raise ValueError("The uploaded content is not a PDF.")

    try:
        reader = PdfReader(BytesIO(content), strict=True)
        if reader.is_encrypted:
            raise ValueError("Encrypted PDFs are not supported.")
        if len(reader.pages) > 100:
            raise ValueError("PDF exceeds the 100-page limit.")

        text = "\\n".join(page.extract_text() or "" for page in reader.pages).strip()
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError("Unable to parse this PDF.") from exc

    if not text:
        raise ValueError("No readable text found. OCR is needed for scanned PDFs.")

    return text

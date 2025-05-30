import fitz  # PyMuPDF
import pdfplumber
from typing import List, Optional, Dict, Any
import os
import tempfile
import re


def extract_text_with_pymupdf(pdf_path: str) -> str:
    """
    Extract text from a PDF file using PyMuPDF (fitz)

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text as a string
    """
    doc = fitz.open(pdf_path)
    text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()

    doc.close()
    return text


def extract_text_with_pdfplumber(pdf_path: str) -> str:
    """
    Extract text from a PDF file using pdfplumber

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text as a string
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def save_upload_file_temp(upload_file) -> str:
    """
    Save an uploaded file to a temporary file

    Args:
        upload_file: The uploaded file

    Returns:
        Path to the temporary file
    """
    try:
        suffix = os.path.splitext(upload_file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            temp.write(upload_file.file.read())
            temp_path = temp.name
        return temp_path
    except Exception:
        return ""


def clean_academic_text(text: str) -> str:
    """
    Clean text extracted from PDFs to reduce noise and improve chunking.

    Args:
        text: Raw text extracted from PDF

    Returns:
        Cleaned text
    """
    # Remove excessive whitespace while preserving paragraph breaks
    text = re.sub(r"\s*\n\s*\n\s*", "\n\n", text)
    text = re.sub(r"\s*\n\s*", " ", text)

    # Clean up common PDF artifacts
    text = re.sub(r"\s+", " ", text)  # Multiple spaces to single space
    text = re.sub(r"\f", "", text)  # Remove form feeds
    text = re.sub(
        r"(?<=[.!?])\s+", "\n\n", text
    )  # Add paragraph breaks after sentences

    # Clean up mathematical notation artifacts
    text = re.sub(r"\{\s*\}", "", text)  # Remove empty LaTeX brackets
    text = re.sub(r"\s*\(\s*", " (", text)  # Clean up parentheses
    text = re.sub(r"\s*\)\s*", ") ", text)

    # Remove headers and footers patterns
    text = re.sub(
        r"^.*?Abstract\s*", "Abstract\n\n", text, flags=re.DOTALL
    )  # Clean pre-abstract content
    text = re.sub(r"\d+\s*$", "", text)  # Remove page numbers

    # Final cleanup
    text = text.strip()
    return text


def split_into_chunks(
    text: str, chunk_size: int = 4000, overlap: int = 200
) -> List[str]:
    """
    Split the text extracted from a PDF into chunks suitable for LLM processing.

    Args:
        text: The text to split into chunks
        chunk_size: Maximum size of each chunk in characters
        overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    if not text or not isinstance(text, str):
        return []

    # Clean the text to improve chunking
    text = clean_academic_text(text)

    # For short texts, return as a single chunk
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    paragraphs = re.split(r"\n\s*\n|\r\n\s*\r\n", text)
    current_chunk = ""

    # Try to maintain paragraph integrity when possible
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        # If adding this paragraph would exceed chunk size and we already have content
        if len(current_chunk) + len(paragraph) > chunk_size and current_chunk:
            chunks.append(current_chunk)
            # Start new chunk with overlap from previous chunk if possible
            if overlap > 0 and len(current_chunk) > overlap:
                current_chunk = current_chunk[-overlap:] + "\n\n" + paragraph
            else:
                current_chunk = paragraph
        else:
            if current_chunk:
                current_chunk += "\n\n"
            current_chunk += paragraph

    # Don't forget the last chunk
    if current_chunk:
        chunks.append(current_chunk)

    # If chunking by paragraphs failed (e.g., huge paragraphs), force split by sentences
    if len(chunks) <= 1 and len(text) > chunk_size:
        chunks = []
        sentences = re.split(r"(?<=[.!?])\s+", text)
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
                chunks.append(current_chunk)
                current_chunk = sentence
            else:
                if current_chunk:
                    current_chunk += " "
                current_chunk += sentence

        if current_chunk:
            chunks.append(current_chunk)

    # Last resort: if we still don't have good chunks, force split by characters
    if len(chunks) <= 1 and len(text) > chunk_size:
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            end = min(i + chunk_size, len(text))
            # Try to find a sentence break near the end
            if end < len(text):
                for j in range(min(end, len(text) - 1), max(i, end - 200), -1):
                    if text[j] in ".!?" and (
                        j + 1 >= len(text) or text[j + 1].isspace()
                    ):
                        end = j + 1
                        break

            chunk = text[i:end].strip()
            if chunk:
                chunks.append(chunk)

    return chunks

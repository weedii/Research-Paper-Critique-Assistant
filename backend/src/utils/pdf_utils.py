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

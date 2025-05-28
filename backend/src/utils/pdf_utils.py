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
    Clean text extracted from academic PDFs to reduce noise and improve chunking.

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


def chunk_text(text: str, chunk_size: int = 4000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks of specified size

    Args:
        text: Text to split
        chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    # Input validation
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    if not text:
        return []

    # Clean the text first
    text = clean_academic_text(text)

    # Adjust parameters based on text length
    text_len = len(text)
    if text_len < 1000:  # For very short texts
        return [text]  # Return as single chunk

    # Enforce minimum chunk size and maximum overlap
    MIN_CHUNK_SIZE = 1000  # Increased minimum size
    MAX_OVERLAP_RATIO = 0.1  # Overlap should not be more than 10% of chunk size

    # Adjust chunk_size if needed
    chunk_size = max(chunk_size, MIN_CHUNK_SIZE)
    # Adjust overlap if needed
    overlap = min(overlap, int(chunk_size * MAX_OVERLAP_RATIO))

    chunks = []
    start = 0

    while start < text_len:
        # Calculate end point
        end = min(start + chunk_size, text_len)

        if end < text_len:
            # Look for a good break point within the last 20% of the chunk
            search_start = max(start + int(chunk_size * 0.8), start)

            # Try to find paragraph break first
            break_point = text.rfind("\n\n", search_start, end)
            if break_point == -1:
                # Try sentence endings
                for punct in [". ", "? ", "! "]:
                    break_point = text.rfind(punct, search_start, end)
                    if break_point != -1:
                        break_point += 2  # Include the punctuation and space
                        break

            # If no good break point found, use space
            if break_point == -1:
                break_point = text.rfind(" ", search_start, end)

            if break_point != -1 and break_point > start + MIN_CHUNK_SIZE:
                end = break_point

        # Get the chunk and clean it
        chunk = text[start:end].strip()

        # Only add non-empty chunks that meet minimum size
        if chunk and len(chunk) >= MIN_CHUNK_SIZE:
            chunks.append(chunk)
        elif chunk:  # If chunk is too small and we're not at the end
            if start + chunk_size < text_len:
                end = min(start + chunk_size, text_len)
                chunk = text[start:end].strip()
                if chunk:
                    chunks.append(chunk)
            else:  # If it's the last chunk, append it to the previous one
                if chunks:
                    chunks[-1] = chunks[-1] + " " + chunk
                else:
                    chunks.append(chunk)

        # Move to next chunk
        start = end - overlap
        if start >= end:  # Prevent infinite loop
            break

    # Final validation - merge any chunks that are too small
    if len(chunks) > 1:
        final_chunks = []
        current_chunk = chunks[0]

        for next_chunk in chunks[1:]:
            if len(current_chunk) < MIN_CHUNK_SIZE:
                current_chunk += " " + next_chunk
            else:
                final_chunks.append(current_chunk)
                current_chunk = next_chunk

        final_chunks.append(current_chunk)
        chunks = final_chunks

    return chunks

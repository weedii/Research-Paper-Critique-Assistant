from typing import Dict, Any, List, Optional
import os
import asyncio
import logging
from fastapi import UploadFile

from ..utils.pdf_utils import (
    extract_text_with_pymupdf,
    extract_text_with_pdfplumber,
    save_upload_file_temp,
)
from .dspy_modules import analyze_paper

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def process_pdf_file(file: UploadFile) -> Dict[str, Any]:
    """
    Process an uploaded PDF file

    Args:
        file: The uploaded PDF file

    Returns:
        Dictionary with the analysis results
    """
    logger.info(f"Received file upload: {file.filename}")

    if not file or not file.filename.lower().endswith(".pdf"):
        logger.error(f"Invalid file format: {file.filename}")
        return {"error": "Invalid file format. Please upload a PDF file."}

    # Save the uploaded file to a temporary location
    logger.info("Saving uploaded file to temporary location")
    temp_path = save_upload_file_temp(file)
    if not temp_path:
        logger.error("Failed to save the uploaded file")
        return {"error": "Failed to save the uploaded file."}

    logger.info(f"File saved to temporary path: {temp_path}")

    try:
        # Try extracting text with PyMuPDF first
        logger.info("Attempting to extract text with PyMuPDF")
        text = extract_text_with_pymupdf(temp_path)

        # If PyMuPDF fails, try with pdfplumber
        if not text.strip():
            logger.info("PyMuPDF extraction yielded no text, trying pdfplumber")
            text = extract_text_with_pdfplumber(temp_path)

        logger.info(f"Text extraction complete. Extracted {len(text)} characters")

        if not text.strip():
            logger.error("Failed to extract any text from the PDF")
            return {"error": "Failed to extract text from the PDF."}

        # Process the paper with DSPy
        logger.info("Starting paper analysis with DSPy")
        analysis_result = analyze_paper(text)
        logger.info("Paper analysis complete")

        # Remove temporary file
        try:
            logger.info(f"Removing temporary file: {temp_path}")
            os.unlink(temp_path)
        except Exception as e:
            logger.warning(f"Failed to remove temporary file: {str(e)}")

        return analysis_result

    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}", exc_info=True)

        # Clean up on exception
        try:
            logger.info(f"Removing temporary file after error: {temp_path}")
            os.unlink(temp_path)
        except Exception as cleanup_e:
            logger.warning(
                f"Failed to remove temporary file during cleanup: {str(cleanup_e)}"
            )

        return {"error": f"Error processing PDF: {str(e)}"}

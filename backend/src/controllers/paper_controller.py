from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request
from typing import Dict, Any
import logging
import time

from ..services.paper_service import process_pdf_file
from ..schemas.pdf_schemas import PaperAnalysisResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/upload", response_model=PaperAnalysisResponse)
async def upload_pdf(request: Request, file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload and process a PDF file

    Args:
        file: The PDF file to upload

    Returns:
        Analysis of the paper including sections, critique, and reviewer questions
    """
    # Log request information
    request_id = id(request)
    client_host = request.client.host if request.client else "unknown"
    start_time = time.time()

    logger.info(f"Request {request_id}: Received upload request from {client_host}")
    logger.info(
        f"Request {request_id}: File information - name: {file.filename}, content-type: {file.content_type}"
    )

    if not file or not file.filename.lower().endswith(".pdf"):
        logger.error(f"Request {request_id}: Invalid file format: {file.filename}")
        raise HTTPException(
            status_code=400, detail="Invalid file format. Please upload a PDF file."
        )

    try:
        logger.info(f"Request {request_id}: Processing PDF file")
        result = await process_pdf_file(file)

        if "error" in result:
            logger.error(
                f"Request {request_id}: Error processing file - {result['error']}"
            )
            raise HTTPException(status_code=500, detail=result["error"])

        processing_time = time.time() - start_time
        logger.info(
            f"Request {request_id}: Successfully processed PDF in {processing_time:.2f} seconds"
        )

        # Log the structure of the result
        if result:
            log_fields = {
                "goal": len(result.get("goal", "")),
                "hypothesis": len(result.get("hypothesis", "")),
                "methods": len(result.get("methods", "")),
                "results": len(result.get("results", "")),
                "conclusion": len(result.get("conclusion", "")),
                "critique": len(result.get("critique", "")),
                "reviewer_questions": len(result.get("reviewer_questions", [])),
            }
            logger.info(f"Request {request_id}: Response structure - {log_fields}")

        return result
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log unexpected errors
        logger.error(
            f"Request {request_id}: Unexpected error - {str(e)}", exc_info=True
        )
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )

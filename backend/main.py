from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
import time
import traceback
import uvicorn

from src.controllers.paper_controller import router as paper_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Research Paper Critique Assistant API",
    description="API for analyzing and critiquing research papers",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(paper_router, prefix="/api/papers", tags=["papers"])


# Add middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = id(request)
    client_host = request.client.host if request.client else "unknown"

    logger.info(
        f"Request {request_id}: {request.method} {request.url.path} from {client_host}"
    )

    start_time = time.time()

    try:
        response = await call_next(request)
        process_time = time.time() - start_time

        logger.info(
            f"Request {request_id}: {request.method} {request.url.path} completed "
            f"with status {response.status_code} in {process_time:.3f}s"
        )

        return response
    except Exception as e:
        logger.error(
            f"Request {request_id}: {request.method} {request.url.path} failed with error: {str(e)}",
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )


# Exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)},
    )


# Generic exception handler
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred"},
    )


@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Research Paper Critique Assistant API", "docs": "/docs"}


# For local development
if __name__ == "__main__":
    logger.info("Starting application server")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

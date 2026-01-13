"""

API ROUTES

ALL PLACEHOLDERS NOTHING HAS BEEN IMPLEMENTED YET

"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks, Request

from app.api.schemas import DocumentInfo, QueryRequest, QueryResponse, UploadResponse
from app.core.config import Config
from app.core.state import AppState


router = APIRouter()


def get_state(request: Request) -> AppState:
    return request.app.state

# POST /upload
@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    raise HTTPException(
        status_code=501,
        detail="Upload endpoint not implemented yet",
    )

# POST /query
@router.post("/query", response_model=QueryResponse)
async def query_documents(
    request: Request,
    body: QueryRequest,
):
    raise HTTPException(
        status_code=501,
        detail="Query endpoint not implemented yet",
    )

# GET /documents
@router.get("/documents", response_model=List[DocumentInfo])
async def list_documents(request: Request):
    raise HTTPException(
        status_code=501,
        detail="List documents endpoint not implemented yet",
    )

# GET /documents/{doc_id}
@router.get("/documents/{doc_id}")
async def get_document(request: Request, doc_id: str):
    raise HTTPException(
        status_code=501,
        detail="Get document endpoint not implemented yet",
    )

# DELETE /document/{doc_id}
@router.delete("/document/{doc_id}")
async def delete_document(request: Request, doc_id: str):
    raise HTTPException(
        status_code=501,
        detail="Delete document endpoint not implemented yet",
    )

# GET /health
@router.get("/health")
async def health_check(request: Request):
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "api",
    }

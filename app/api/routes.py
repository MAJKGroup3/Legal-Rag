from __future__ import annotations

from datetime import datetime
from typing import List, Dict, Any

# fast api imports

from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks, Request

# schema imports

from app.api.schemas import DocumentInfo, QueryRequest, QueryResponse, UploadResponse

from app.core.config import Config
from app.core.state import AppState

from app.agents.legalrag_agent import build_agent, extract_agent_text, extract_agent_response

# Router
router = APIRouter()
agent = build_agent()

def get_state(request: Request) -> AppState:
    return request.app.state.app_state

# POST /upload
@router.post("/upload", response_model = UploadResponse)
async def upload_document(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    ):
    state = get_state(request)

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code = 400, detail = "Only PDF files are supported")

    if state.doc_processor is None:
        raise HTTPException(status_code = 500, detail = "Document processor is not intialized") 

    try:
        pdf_bytes = await file.read()
        result = state.doc_processor.process_document(pdf_bytes, file.filename)

        state.document_store[result["doc_id"]] = result

        return UploadResponse(
            success = True,
            doc_id = result["doc_id"],
            filename = result["filename"],
            message = f"Documents '{file.filename}' processed successfully",
            chunk_count = result["chunk_count"],
        )
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Error processing documents: {str(e)}")


# POST /query
@router.post("/query", response_model = QueryResponse)

async def query_documents(request: Request, body: QueryRequest):

    state = get_state(request)

    if state.rag_system is None:
        raise HTTPException(status_code = 500, detail = "RAG system is not intialized")

    try:
        result = state.rag_system.query(body.query, top_k = body.top_k or Config.TOP_K_CHUNKS)

        return QueryResponse(
            query = result["query"],
            answer = result["answer"],
            retrieved_chunks = result["retrieved_chunks"],
            num_chunks = result["num_chunks"],
            timestamp=datetime.now().isoformat(),
        )
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Error processing query: {str(e)}")


@router.post("/agent-query")
async def agent_query(request: Request, body: QueryRequest):
    """
    Agent-based query router:
    - Uses rag_query for corpus-grounded questions
    - Uses get_weather for weather questions
    """
    try:
        result = agent.invoke(
            {"messages": [{"role": "user", "content": body.query}]}
        )
        agent_data = extract_agent_response(result)

        return {
            "query": body.query,
            "answer": agent_data["answer"],
            "retrieved_chunks": agent_data["retrieved_chunks"],
            "num_chunks": agent_data["num_chunks"],
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing agent query: {str(e)}")


# GET /documents
@router.get("/documents", response_model = list[DocumentInfo])
async def list_documents(request: Request):
    state = get_state(request)

    documents = []

    for doc_id, doc_data in state.document_store.items():

        documents.append(
            DocumentInfo(
                doc_id = doc_id,
                filename = doc_data["filename"],
                doc_type = doc_data["meta_data"]["doc_type"],
                word_count = doc_data["meta_data"]["word_count"],
                chunk_count = doc_data["chunk_count"],
                timestamp = doc_data["meta_data"]["timestamp"],
            )
        )

    return documents
    
# GET /documents/{doc_id}
@router.get("/documents/{doc_id}")

async def get_document(request: Request, doc_id: str):
    state = get_state(request)

    if doc_id not in state.document_store:
        raise HTTPException(status_code = 404, detail = "Document not found")
    
    return state.document_store[doc_id]

# DELETE /document/{doc_id}
@router.delete("/document/{doc_id}")

async def delete_document(request: Request, doc_id: str):
    state = get_state(request)

    if doc_id not in state.document_store:
        raise HTTPException(status_code = 404, detail = "Document not found")
    
    if state.doc_processor is None:
        raise HTTPException(status_code = 500, detail = "Document processor is not initialized")
    
    try:
        
        # Del from chromadb
        state.doc_processor.chroma_manager.delete_by_doc_id(doc_id)

        # del raw from s3
        filename = state.document_store[doc_id]["filename"]

        state.doc_processor.s3_manager.delete_object(Config.RAW_BUCKET, filename)

        del state.document_store[doc_id]
        return {"Success": True, "Message": f"Document {doc_id} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Error deleting document: {str(e)}")

# GET
@router.get("/health")
async def health_check(request: Request):
    state = get_state(request)

    return { 
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "documents_count": len(state.document_store),
        "chroma_collection" : Config.COLLECTION_NAME,
    }

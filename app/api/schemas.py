from pydantic import BaseModel

from typing import Optional, List, Dict, Any

class QueryRequest(BaseModel): 
    query: str
    
    top_k: Optional[int] = 5


class QueryResponse(BaseModel):
    query: str
    
    answer: str
    
    retrieved_chunks: List[Dict]
    
    num_chunks: int
    
    timestamp: str

class DocumentInfo(BaseModel):
    doc_id: str
    
    filename: str

    doc_type: str
    
    word_count: int
    
    chunk_count: int
    
    timestamp: str

class UploadResponse(BaseModel):
    success: bool

    doc_id: str
    
    filename: str

    message: str
    
    chunk_count: int

class AgentQueryRequest(BaseModel):
    query: str

class AgentQueryResponse(BaseModel):
    query: str
    answer: str
    tool_used: Optional[str] = None
    tool_result: Optional[Dict[str, Any]] = None
    timestamp: str
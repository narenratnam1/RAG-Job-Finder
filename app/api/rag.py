"""
RAG (Retrieval Augmented Generation) endpoints
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List
from app.services.vector_store import VectorService
from app.services.rag_engine import RAGEngine

router = APIRouter()
vector_store_service = VectorService()
rag_engine = RAGEngine(vector_store_service)


class QueryRequest(BaseModel):
    """Request model for RAG queries"""
    query: str = Field(..., description="The user's question or query")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of relevant chunks to retrieve")
    include_sources: bool = Field(default=True, description="Include source documents in response")


class QueryResponse(BaseModel):
    """Response model for RAG queries"""
    query: str
    answer: str
    sources: Optional[List[dict]] = None
    retrieved_chunks: int


@router.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Query the RAG system with a question
    
    Args:
        request: Query request containing the question and parameters
    
    Returns:
        QueryResponse: The generated answer with sources
    """
    try:
        result = await rag_engine.query(
            query=request.query,
            top_k=request.top_k,
            include_sources=request.include_sources
        )
        
        return QueryResponse(
            query=request.query,
            answer=result["answer"],
            sources=result.get("sources") if request.include_sources else None,
            retrieved_chunks=result["retrieved_chunks"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )


@router.post("/search")
async def semantic_search(query: str, top_k: int = 5):
    """
    Perform semantic search without generation
    
    Args:
        query: The search query
        top_k: Number of results to return
    
    Returns:
        dict: Search results with relevant document chunks
    """
    try:
        results = vector_store_service.search(
            query=query,
            k=top_k
        )
        
        return {
            "status": "success",
            "query": query,
            "results_count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing search: {str(e)}"
        )

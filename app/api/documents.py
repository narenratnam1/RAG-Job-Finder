"""
Document management endpoints
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import List
from app.services.ingestion import IngestionService
from app.core.config import settings

router = APIRouter()
ingestion_service = IngestionService()


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and ingest a document into the vector store
    
    Args:
        file: The document file to upload (PDF, TXT, DOC, DOCX)
    
    Returns:
        dict: Upload status and document metadata
    """
    # Validate file extension
    file_ext = f".{file.filename.split('.')[-1].lower()}"
    allowed_exts = settings.ALLOWED_EXTENSIONS.split(",")
    
    if file_ext not in allowed_exts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_ext} not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
        )
    
    # Read file content
    content = await file.read()
    
    # Check file size
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE} bytes"
        )
    
    try:
        # Ingest document
        result = await ingestion_service.ingest_document(
            file_name=file.filename,
            file_content=content,
            file_type=file_ext
        )
        
        return {
            "status": "success",
            "message": "Document uploaded and ingested successfully",
            "document_id": result["document_id"],
            "chunks_created": result["chunks_created"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing document: {str(e)}"
        )


@router.get("/list")
async def list_documents():
    """
    List all documents in the vector store
    
    Returns:
        dict: List of document metadata
    """
    try:
        documents = await ingestion_service.list_documents()
        return {
            "status": "success",
            "count": len(documents),
            "documents": documents
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing documents: {str(e)}"
        )


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """
    Delete a document from the vector store
    
    Args:
        document_id: The ID of the document to delete
    
    Returns:
        dict: Deletion status
    """
    try:
        await ingestion_service.delete_document(document_id)
        return {
            "status": "success",
            "message": f"Document {document_id} deleted successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting document: {str(e)}"
        )

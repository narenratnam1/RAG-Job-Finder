"""
Document ingestion service
"""

import uuid
from typing import List, Dict, Any
from datetime import datetime
from io import BytesIO
from pypdf import PdfReader
from app.services.vector_store import VectorService
from app.core.config import settings


class IngestionService:
    """Service for ingesting and processing documents"""
    
    def __init__(self):
        """Initialize ingestion service with vector store"""
        self.vector_store = VectorService()
        self.chunk_size = 1000
        self.chunk_overlap = 200
    
    async def ingest_document(
        self,
        file_name: str,
        file_content: bytes,
        file_type: str
    ) -> Dict[str, Any]:
        """
        Ingest a document into the vector store
        
        Args:
            file_name: Name of the file
            file_content: File content as bytes
            file_type: File extension/type
        
        Returns:
            dict: Ingestion result with document ID and chunk count
        """
        try:
            # Extract text based on file type
            if file_type == ".pdf":
                text = self._extract_text_from_pdf(file_content)
            elif file_type in [".txt"]:
                text = file_content.decode('utf-8')
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            # Generate document ID
            document_id = str(uuid.uuid4())
            
            # Split text into chunks
            chunks = self._split_text(text)
            
            # Prepare metadata
            metadatas = []
            for i, chunk in enumerate(chunks):
                metadatas.append({
                    "document_id": document_id,
                    "file_name": file_name,
                    "file_type": file_type,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "ingested_at": datetime.utcnow().isoformat()
                })
            
            # Add to vector store
            self.vector_store.add_documents(
                texts=chunks,
                metadatas=metadatas
            )
            
            return {
                "document_id": document_id,
                "file_name": file_name,
                "chunks_created": len(chunks)
            }
        except Exception as e:
            raise Exception(f"Error ingesting document: {str(e)}")
    
    def _extract_text_from_pdf(self, file_content: bytes) -> str:
        """
        Extract text from PDF file
        
        Args:
            file_content: PDF file content as bytes
        
        Returns:
            str: Extracted text
        """
        try:
            pdf_file = BytesIO(file_content)
            pdf_reader = PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def _split_text(self, text: str) -> List[str]:
        """
        Split text into chunks with overlap
        
        Args:
            text: Text to split
        
        Returns:
            list: List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < text_length:
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > self.chunk_size // 2:
                    chunk = text[start:start + break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - self.chunk_overlap
        
        return [c for c in chunks if c]  # Filter empty chunks
    
    async def list_documents(self) -> List[Dict[str, Any]]:
        """
        List all documents in the vector store
        
        Returns:
            list: List of document metadata
        """
        try:
            # Simplified implementation - requires document registry for full functionality
            total_count = self.vector_store.collection.count()
            return [{
                "message": "Document listing requires document registry implementation",
                "total_chunks": total_count
            }]
        except Exception as e:
            raise Exception(f"Error listing documents: {str(e)}")
    
    async def delete_document(self, document_id: str) -> Dict[str, Any]:
        """
        Delete a document from the vector store
        
        Args:
            document_id: The document ID to delete
        
        Returns:
            dict: Deletion result
        """
        try:
            # Query for all chunks with this document_id
            results = self.vector_store.collection.get(
                where={"document_id": document_id}
            )
            
            if results and results['ids']:
                self.vector_store.collection.delete(ids=results['ids'])
                return {
                    "status": "success",
                    "chunks_deleted": len(results['ids'])
                }
            else:
                return {
                    "status": "success",
                    "chunks_deleted": 0,
                    "message": "No documents found with that ID"
                }
        except Exception as e:
            raise Exception(f"Error deleting document: {str(e)}")

"""
Main FastAPI application entry point with MCP integration
"""

import os
import tempfile
from typing import List, Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.services.vector_store import VectorService
from app.services.ingestor import process_pdf

# Initialize FastAPI
app = FastAPI(
    title="Agentic RAG API",
    version="1.0.0",
    description="Agentic RAG API with ChromaDB, LangChain, and MCP"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize VectorService (singleton)
vector_service = VectorService()


# Helper function for candidate screening (used by both MCP tool and HTTP endpoint)
def _screen_candidate_logic(job_description: str) -> str:
    """
    Core logic for screening candidates against job descriptions
    
    Args:
        job_description: The job description to compare the resume against
    
    Returns:
        Formatted string with resume context and comparison task
    """
    try:
        # Search vector store for top 10 most relevant chunks (to get most of resume)
        results = vector_service.search(query=job_description, k=10)
        
        # Format output
        if not results:
            return "No resume information found in the database. Please upload a resume first."
        
        # Build context section with retrieved chunks
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"[Part {i} - Page {result['metadata'].get('page', 'N/A')}]:\n{result['text']}"
            )
        
        context_section = "\n\n".join(context_parts)
        
        # Build final prompt
        formatted_output = f"""CONTEXT: Here are the relevant parts of the candidate's resume:

{context_section}

TASK: Compare the resume parts above against this Job Description:

{job_description}"""
        
        return formatted_output
    
    except Exception as e:
        return f"Error screening candidate: {str(e)}"


# Initialize FastMCP (optional - for MCP tool integration)
try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("AgentPolicy")
    
    @mcp.tool()
    def consult_policy_db(query: str) -> str:
        """
        Consult the policy database using semantic search
        
        Args:
            query: The search query to find relevant policy information
        
        Returns:
            Formatted string with relevant policy information
        """
        try:
            # Search vector store
            results = vector_service.search(query=query, k=3)
            
            # Format output
            if not results:
                return "No relevant policy information found."
            
            formatted_output = f"Found {len(results)} relevant policy documents:\n\n"
            
            for i, result in enumerate(results, 1):
                formatted_output += f"--- Result {i} ---\n"
                formatted_output += f"Source: {result['metadata'].get('source', 'Unknown')}\n"
                formatted_output += f"Page: {result['metadata'].get('page', 'N/A')}\n"
                formatted_output += f"Relevance Score: {1 - result['distance']:.4f}\n"
                formatted_output += f"Content:\n{result['text']}\n\n"
            
            return formatted_output
        
        except Exception as e:
            return f"Error querying policy database: {str(e)}"
    
    @mcp.tool()
    def screen_candidate(job_description: str) -> str:
        """
        Screen a candidate by comparing their resume against a job description
        
        Args:
            job_description: The job description to compare the resume against
        
        Returns:
            Formatted string with resume context and comparison task
        """
        return _screen_candidate_logic(job_description)
    
    @mcp.tool()
    def get_screener_instructions() -> str:
        """
        Get instructions for using the candidate screening tool
        
        Returns:
            String with step-by-step usage instructions
        """
        return """1. Upload a PDF Resume. 2. In the chat, paste the Job Description and ask: "Evaluate this candidate for this role." """
    
    print("✓ MCP tools registered: 'consult_policy_db', 'screen_candidate', 'get_screener_instructions'")
except ImportError:
    print("⚠️  MCP not available - running without MCP tools")
    mcp = None


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file, process it, and add to vector store
    
    Args:
        file: PDF file to upload
    
    Returns:
        dict: Status and processing results
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        # Write uploaded file to temp location
        content = await file.read()
        temp_file.write(content)
        temp_path = temp_file.name
    
    try:
        # Process PDF using ingestor
        chunks = process_pdf(temp_path)
        
        # Prepare data for vector store
        texts: List[str] = []
        metadatas: List[dict] = []
        
        for chunk in chunks:
            texts.append(chunk.page_content)
            metadatas.append({
                "source": file.filename,
                "page": chunk.metadata.get("page", 0),
                **chunk.metadata
            })
        
        # Add to vector store
        vector_service.add_documents(texts=texts, metadatas=metadatas)
        
        return {
            "status": "success",
            "filename": file.filename,
            "chunks_processed": len(chunks),
            "message": f"Successfully processed and stored {len(chunks)} chunks"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing PDF: {str(e)}"
        )
    
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/consult")
async def consult_policy_endpoint(query: str):
    """
    HTTP endpoint to consult the policy database
    
    Args:
        query: The search query
    
    Returns:
        Search results from the policy database
    """
    try:
        # Search vector store
        results = vector_service.search(query=query, k=3)
        
        # Format output
        if not results:
            return {
                "status": "success",
                "query": query,
                "message": "No relevant policy information found.",
                "results": []
            }
        
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append({
                "rank": i,
                "source": result['metadata'].get('source', 'Unknown'),
                "page": result['metadata'].get('page', 'N/A'),
                "relevance_score": round(1 - result['distance'], 4),
                "content": result['text']
            })
        
        return {
            "status": "success",
            "query": query,
            "results_count": len(formatted_results),
            "results": formatted_results
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error querying policy database: {str(e)}"
        )


@app.post("/screen_candidate")
async def screen_candidate_endpoint(job_description: str):
    """
    Screen a candidate by comparing their resume against a job description
    
    Args:
        job_description: The job description to compare the resume against
    
    Returns:
        Screening results with resume context and comparison task
    """
    try:
        # Call the core screening logic
        result = _screen_candidate_logic(job_description)
        
        return {
            "status": "success",
            "job_description": job_description,
            "screening_result": result
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error screening candidate: {str(e)}"
        )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Agentic RAG API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "POST /upload - Upload PDF files",
            "consult": "POST /consult?query=your_question - Query the policy database",
            "screen_candidate": "POST /screen_candidate?job_description=... - Screen candidate against job description",
            "docs": "GET /docs - Interactive API documentation",
            "health": "GET /health - Health check"
        },
        "mcp_tools": "consult_policy_db, screen_candidate, get_screener_instructions" if mcp else "MCP not configured"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "vector_store": "operational",
        "mcp": "available" if mcp else "unavailable"
    }


if __name__ == "__main__":
    import uvicorn
    import sys
    import os
    
    # Add parent directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

"""
Main FastAPI application entry point with MCP integration
"""

import os
import tempfile
import logging
from typing import List, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.services.vector_store import VectorService
from app.services.ingestor import process_pdf
from app.services.pdf_generator import PDFService
from app.services.resume_tailor import tailor_resume_with_ai
from app.services.pdf_extractor import extract_text_from_pdf

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import ChatOpenAI at startup
try:
    from langchain_openai import ChatOpenAI
    logger.info("✓ ChatOpenAI imported successfully")
except ImportError as e:
    logger.warning(f"⚠️  ChatOpenAI import failed: {e}. AI features will run in demo mode.")
    ChatOpenAI = None

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

# Initialize PDFService
pdf_service = PDFService()

# Define uploads directory
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)
logger.info(f"✓ Uploads directory: {UPLOADS_DIR}")


# Pydantic models for request validation
class TailorResumeRequest(BaseModel):
    """Request model for resume tailoring"""
    job_description: str
    current_resume_text: str

class GeneratePDFRequest(BaseModel):
    """Request model for PDF generation"""
    content: str


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
    Also saves a copy to the uploads directory for reuse
    
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
        
        # Save a copy to uploads directory for reuse
        saved_path = os.path.join(UPLOADS_DIR, file.filename)
        with open(saved_path, 'wb') as f:
            f.write(content)
        logger.info(f"✓ Saved resume to library: {file.filename}")
        
        return {
            "status": "success",
            "filename": file.filename,
            "chunks_processed": len(chunks),
            "saved_to_library": True,
            "message": f"Successfully processed and stored {len(chunks)} chunks. Resume saved to library."
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


@app.get("/resumes")
async def list_resumes():
    """
    Get list of all saved resumes in the uploads directory
    
    Returns:
        dict: List of resume filenames
    """
    try:
        # Get all PDF files in uploads directory
        resumes = [f for f in os.listdir(UPLOADS_DIR) if f.endswith('.pdf')]
        resumes.sort()  # Sort alphabetically
        
        logger.info(f"✓ Listed {len(resumes)} saved resumes")
        
        return {
            "status": "success",
            "count": len(resumes),
            "resumes": resumes
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing resumes: {str(e)}"
        )


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
async def screen_candidate_endpoint(
    job_description: str = Form(...),
    resume_filename: str = Form(...)
):
    """
    Screen a candidate by analyzing their full resume against a job description using AI
    
    Args:
        job_description: The job description to compare against
        resume_filename: Filename of the saved resume in the library
    
    Returns:
        AI-powered analysis with score, match status, missing skills, and reasoning
    """
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check if resume exists in library
        resume_path = os.path.join(UPLOADS_DIR, resume_filename)
        if not os.path.exists(resume_path):
            raise HTTPException(
                status_code=404,
                detail=f"Resume '{resume_filename}' not found in library"
            )
        
        # Extract full text from resume PDF
        resume_text = extract_text_from_pdf(resume_path)
        logger.info(f"✓ Screening resume: {resume_filename}")
        
        # Check if OpenAI API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key or api_key == "your_openai_api_key_here":
            # Return demo response if no API key
            return {
                "status": "success",
                "score": 75,
                "match_status": "Demo Mode",
                "missing_skills": ["Add OPENAI_API_KEY to enable real analysis"],
                "reasoning": "Demo Mode: Add your OpenAI API key to .env to enable AI-powered resume screening.",
                "resume_filename": resume_filename
            }
        
        # Use ChatOpenAI to analyze
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage, SystemMessage
        import json
        
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,
            api_key=api_key
        )
        
        # Create structured prompt for ATS analysis
        system_prompt = """You are an expert ATS (Applicant Tracking System) and recruitment specialist. 
Your task is to analyze a candidate's resume against a job description and provide a structured assessment.

You MUST respond with ONLY a valid JSON object in this exact format (no additional text):
{
  "score": 85,
  "match_status": "High Match",
  "missing_skills": ["React", "AWS"],
  "reasoning": "Detailed explanation of the assessment"
}

Score Guidelines:
- 90-100: Excellent Match (exceeds requirements)
- 75-89: High Match (meets most requirements)
- 60-74: Moderate Match (meets some requirements)
- 40-59: Low Match (significant gaps)
- 0-39: Poor Match (major misalignment)

Match Status Options: "Excellent Match", "High Match", "Moderate Match", "Low Match", "Poor Match"
"""
        
        user_prompt = f"""Analyze this candidate's resume against the job description:

JOB DESCRIPTION:
{job_description}

CANDIDATE RESUME:
{resume_text}

Provide your analysis as a JSON object with:
1. score (0-100): Overall match percentage
2. match_status: One of the five categories
3. missing_skills: Array of key skills from JD that are missing or weak in the resume
4. reasoning: 2-3 sentences explaining the score, highlighting strengths and gaps

Remember: Respond with ONLY the JSON object, no other text."""
        
        # Call the LLM
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        
        # Parse JSON response
        try:
            # Clean the response (remove markdown code blocks if present)
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            analysis = json.loads(content)
            
            return {
                "status": "success",
                "score": analysis.get("score", 0),
                "match_status": analysis.get("match_status", "Unknown"),
                "missing_skills": analysis.get("missing_skills", []),
                "reasoning": analysis.get("reasoning", "No reasoning provided"),
                "resume_filename": resume_filename
            }
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            logger.error(f"Raw response: {response.content}")
            
            # Return fallback response
            return {
                "status": "success",
                "score": 50,
                "match_status": "Analysis Error",
                "missing_skills": ["Unable to parse AI response"],
                "reasoning": f"AI analysis completed but response format was invalid. Please try again.",
                "resume_filename": resume_filename
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error screening candidate: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error screening candidate: {str(e)}"
        )


@app.post("/tailor_resume")
async def tailor_resume(
    job_description: str = Form(...),
    resume_filename: str = Form(None),
    resume_file: UploadFile = File(None)
):
    """
    Tailor a resume to match a job description using AI (returns preview text)
    
    Args:
        job_description: The target job description
        resume_filename: Optional - filename of saved resume in library
        resume_file: Optional - PDF file to upload (if not using saved resume)
    
    Returns:
        JSON with tailored_text for preview
    """
    temp_path = None
    filename = None
    
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Option 1: Use saved resume from library
        if resume_filename:
            saved_path = os.path.join(UPLOADS_DIR, resume_filename)
            if not os.path.exists(saved_path):
                raise HTTPException(
                    status_code=404,
                    detail=f"Resume '{resume_filename}' not found in library"
                )
            resume_text = extract_text_from_pdf(saved_path)
            filename = resume_filename
            logger.info(f"✓ Using saved resume: {resume_filename}")
        
        # Option 2: Use uploaded file
        elif resume_file:
            # Validate file type
            if not resume_file.filename.endswith('.pdf'):
                raise HTTPException(
                    status_code=400,
                    detail="Only PDF files are supported"
                )
            
            # Create temporary file for the uploaded resume
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                content = await resume_file.read()
                temp_file.write(content)
                temp_path = temp_file.name
            
            resume_text = extract_text_from_pdf(temp_path)
            filename = resume_file.filename
            logger.info(f"✓ Using uploaded resume: {resume_file.filename}")
        
        else:
            raise HTTPException(
                status_code=400,
                detail="Either resume_filename or resume_file must be provided"
            )
        
        # Use AI to tailor the resume
        tailored_text = tailor_resume_with_ai(
            job_description=job_description,
            current_resume_text=resume_text
        )
        
        return {
            "status": "success",
            "tailored_text": tailored_text,
            "original_filename": filename
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error tailoring resume: {str(e)}"
        )
    
    finally:
        # Clean up temporary file if one was created
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/generate_pdf")
async def generate_pdf(request: GeneratePDFRequest):
    """
    Generate a PDF from tailored resume text
    
    Args:
        request: GeneratePDFRequest containing content
    
    Returns:
        FileResponse: Generated PDF file
    """
    try:
        # Extract only the resume content (after the marker)
        marker = "## 📄 TAILORED RESUME CONTENT"
        pdf_content = request.content
        
        if marker in request.content:
            # Split and take everything after the marker
            parts = request.content.split(marker, 1)
            if len(parts) > 1:
                pdf_content = parts[1].strip()
                logger.info("✓ Extracted resume content after marker for PDF generation")
            else:
                logger.warning("⚠️  Marker found but no content after it, using full text")
        else:
            logger.warning("⚠️  Resume content marker not found, using full text for PDF")
        
        # Generate PDF from extracted content only (sanitization happens inside)
        pdf_path = pdf_service.generate_resume_pdf(
            text_content=pdf_content,
            filename="tailored_resume.pdf"
        )
        
        logger.info("✓ PDF generated successfully")
        
        # Return the PDF file
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename="tailored_resume.pdf",
            headers={
                "Content-Disposition": "attachment; filename=tailored_resume.pdf"
            }
        )
    
    except Exception as e:
        logger.error(f"❌ PDF generation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating PDF: {str(e)}"
        )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Agentic RAG API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "POST /upload - Upload PDF files and save to library",
            "resumes": "GET /resumes - List all saved resumes in library",
            "consult": "POST /consult?query=your_question - Query the policy database",
            "screen_candidate": "POST /screen_candidate?job_description=... - Screen candidate against job description",
            "tailor_resume": "POST /tailor_resume - Tailor resume (use saved or upload new, returns preview text)",
            "generate_pdf": "POST /generate_pdf - Generate PDF from tailored text",
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

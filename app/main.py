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
from fastapi.staticfiles import StaticFiles
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

# Mount uploads directory as static files for PDF viewing
app.mount("/static/resumes", StaticFiles(directory=UPLOADS_DIR), name="resumes")
logger.info(f"✓ Mounted static files: /static/resumes → {UPLOADS_DIR}")


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
        
        # IMPORTANT: Store only the original filename (basename), NOT temp paths
        original_filename = os.path.basename(file.filename)
        
        for chunk in chunks:
            texts.append(chunk.page_content)
            # Store clean filename in metadata, not temp paths
            metadatas.append({
                "source": original_filename,  # Clean filename only
                "filename": original_filename,  # Redundant but explicit
                "page": chunk.metadata.get("page", 0),
                **chunk.metadata
            })
        
        # Add to vector store
        vector_service.add_documents(texts=texts, metadatas=metadatas)
        
        # Save a copy to uploads directory for reuse
        saved_path = os.path.join(UPLOADS_DIR, original_filename)
        with open(saved_path, 'wb') as f:
            f.write(content)
        logger.info(f"✓ Saved resume to library: {original_filename}")
        
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


@app.get("/resumes/{filename}")
async def download_resume(filename: str):
    """
    Download a resume file from the library
    
    Args:
        filename: Name of the resume file to download
    
    Returns:
        FileResponse: The resume PDF file
    """
    try:
        # Security: Only allow filenames without path traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            logger.warning(f"⚠️  Invalid filename attempt: {filename}")
            raise HTTPException(
                status_code=400,
                detail="Invalid filename - path traversal detected"
            )
        
        # Build file path
        file_path = os.path.join(UPLOADS_DIR, filename)
        
        # DEBUG: Log the exact path being looked for
        logger.info(f"🔍 Download request for: '{filename}'")
        logger.info(f"🔍 Looking in UPLOADS_DIR: {UPLOADS_DIR}")
        logger.info(f"🔍 Full path to check: {file_path}")
        logger.info(f"🔍 File exists: {os.path.exists(file_path)}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            # List available files for debugging
            try:
                available_files = [f for f in os.listdir(UPLOADS_DIR) if f.endswith('.pdf')]
                logger.error(f"❌ File not found: {filename}")
                logger.error(f"📁 Available files in uploads: {available_files}")
            except Exception as list_error:
                logger.error(f"❌ Could not list files in uploads: {list_error}")
            
            raise HTTPException(
                status_code=404,
                detail=f"Resume '{filename}' not found in library. Please ensure the file has been uploaded."
            )
        
        logger.info(f"✓ Serving resume file: {filename}")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="application/pdf"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error serving resume: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error serving resume: {str(e)}"
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


@app.post("/search_candidates")
async def search_candidates(job_description: str = Form(...)):
    """
    Search and rank candidates using RAG + AI reranking
    
    Args:
        job_description: The job description to search for matching candidates
    
    Returns:
        JSON list of top 7 ranked candidates with scores and reasoning
    """
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Step 1: Search vector store for top 10 matches
        results = vector_service.search(query=job_description, k=10)
        
        if not results:
            return {
                "status": "success",
                "count": 0,
                "candidates": [],
                "message": "No candidates found in the database. Please upload resumes first."
            }
        
        logger.info(f"✓ Found {len(results)} initial candidates from vector search")
        
        # Step 2: Prepare candidate data for AI reranking
        candidates_text = []
        candidates_metadata = []  # Track metadata for each candidate
        
        for i, result in enumerate(results, 1):
            # SAFETY FIX: Extract clean filename from metadata (remove any path components)
            # Handle both 'source' and 'filename' fields (redundant storage for safety)
            source = result['metadata'].get('source', result['metadata'].get('filename', 'Unknown'))
            clean_filename = os.path.basename(source) if source != 'Unknown' else 'Unknown'
            
            logger.info(f"Processing candidate #{i}: source='{source}' → clean_filename='{clean_filename}'")
            
            candidate_info = f"""
Candidate #{i}
Filename: {clean_filename}
Resume Content:
{result['text']}
---"""
            candidates_text.append(candidate_info)
            candidates_metadata.append({
                'filename': clean_filename,
                'text': result['text'][:500]  # Store snippet for preview
            })
        
        combined_candidates = "\n".join(candidates_text)
        
        # Step 3: Check OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key or api_key == "your_openai_api_key_here":
            # Return demo response if no API key
            demo_candidates = []
            for i, result in enumerate(results[:7], 1):
                # SAFETY FIX: Extract clean filename
                source = result['metadata'].get('source', result['metadata'].get('filename', 'Unknown'))
                clean_filename = os.path.basename(source) if source != 'Unknown' else 'Unknown'
                
                logger.info(f"Demo mode - candidate #{i}: source='{source}' → clean_filename='{clean_filename}'")
                
                # Try to extract a name from filename (remove .pdf, replace _ with space)
                demo_name = clean_filename.replace('.pdf', '').replace('_', ' ').replace('-', ' ').title() if clean_filename != 'Unknown' else clean_filename
                
                demo_candidates.append({
                    "rank": i,
                    "filename": clean_filename,
                    "name": demo_name,
                    "score": max(50, 95 - (i * 5)),  # Demo scores
                    "reasoning": f"Demo Mode: Add OPENAI_API_KEY to enable AI-powered ranking. This is candidate #{i} from vector search.",
                    "download_url": f"/static/resumes/{clean_filename}"
                })
            
            return {
                "status": "success",
                "count": len(demo_candidates),
                "candidates": demo_candidates,
                "message": "Demo Mode - Add OpenAI API key for AI-powered reranking"
            }
        
        # Step 4: Use AI to rerank candidates
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage, SystemMessage
        import json
        
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,
            api_key=api_key
        )
        
        # Create reranking prompt
        system_prompt = """You are a Senior Technical Recruiter and ATS expert. 
Your task is to evaluate candidates and select the top 7 best matches for the job.

CRITICAL NAME EXTRACTION RULES:
1. Analyze the resume text carefully to identify the candidate's FULL NAME
2. The name is usually at the top of the resume or in a header section
3. If you CANNOT find a clear name in the text, you MUST return exactly "Unknown Candidate"
4. DO NOT invent or fabricate names like "John Doe", "Jane Smith", etc.
5. DO NOT use the filename as the name - return "Unknown Candidate" instead

You MUST respond with ONLY a valid JSON array in this exact format (no additional text):
[
  {
    "filename": "candidate_resume.pdf",
    "name": "Sarah Johnson",
    "score": 95,
    "reasoning": "Excellent match because..."
  },
  ...
]

If no name found in resume, use:
{
  "filename": "candidate_resume.pdf",
  "name": "Unknown Candidate",
  "score": 85,
  "reasoning": "Strong skills match..."
}

Evaluation Criteria:
- Skills match (technical and soft skills)
- Experience level alignment
- Education requirements
- Industry background
- Achievement relevance
- Cultural fit indicators

Score Guidelines:
- 90-100: Exceptional match, exceeds requirements
- 80-89: Strong match, meets all key requirements
- 70-79: Good match, meets most requirements
- 60-69: Adequate match, meets core requirements
- 50-59: Weak match, missing key skills

Return EXACTLY 7 candidates ranked from best to worst. If fewer than 7 candidates are available, return all available candidates.
Each candidate MUST have the "name" field (real name from resume or "Unknown Candidate" - NO invented names)."""
        
        user_prompt = f"""Job Description:
{job_description}

Candidates to Evaluate:
{combined_candidates}

Analyze these candidates, select the top 7 best matches, and rank them from best to worst. 
Return ONLY the JSON array with no additional text."""
        
        # Call the LLM
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        
        # Parse JSON response
        try:
            # Clean the response
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            ranked_candidates = json.loads(content)
            
            # Add rank numbers and download URLs
            for i, candidate in enumerate(ranked_candidates, 1):
                candidate['rank'] = i
                # Add download URL for frontend
                filename = candidate.get('filename', 'unknown.pdf')
                candidate['download_url'] = f"/static/resumes/{filename}"
            
            logger.info(f"✓ AI reranked and selected top {len(ranked_candidates)} candidates")
            
            return {
                "status": "success",
                "count": len(ranked_candidates),
                "candidates": ranked_candidates
            }
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            logger.error(f"Raw response: {response.content}")
            
            # Return fallback with original search results
            fallback_candidates = []
            for i, result in enumerate(results[:7], 1):
                # SAFETY FIX: Extract clean filename
                source = result['metadata'].get('source', result['metadata'].get('filename', 'Unknown'))
                clean_filename = os.path.basename(source) if source != 'Unknown' else 'Unknown'
                
                logger.info(f"Fallback mode - candidate #{i}: source='{source}' → clean_filename='{clean_filename}'")
                
                # Try to extract a name from filename (remove .pdf, replace _ with space)
                fallback_name = clean_filename.replace('.pdf', '').replace('_', ' ').replace('-', ' ').title() if clean_filename != 'Unknown' else clean_filename
                
                fallback_candidates.append({
                    "rank": i,
                    "filename": clean_filename,
                    "name": fallback_name,
                    "score": max(50, int((1 - result['distance']) * 100)),
                    "reasoning": "AI ranking unavailable. Showing vector similarity results.",
                    "download_url": f"/static/resumes/{clean_filename}"
                })
            
            return {
                "status": "success",
                "count": len(fallback_candidates),
                "candidates": fallback_candidates,
                "message": "Using fallback ranking (AI parsing failed)"
            }
    
    except Exception as e:
        logger.error(f"Error searching candidates: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error searching candidates: {str(e)}"
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
            "download_resume": "GET /resumes/{filename} - Download a specific resume PDF",
            "search_candidates": "POST /search_candidates - Search and rank top candidates for a job",
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

# Usage Guide - Agentic RAG API

## Quick Start

### 1. Setup Environment

```bash
# Run setup script
chmod +x setup_env.sh
./setup_env.sh

# Activate virtual environment
source venv/bin/activate
```

### 2. Start the Server

```bash
python app/main.py
```

Or with uvicorn:

```bash
uvicorn app.main:app --reload
```

The server will start at: `http://localhost:8000`

## API Endpoints

### 📤 Upload PDF Endpoint

**POST /upload**

Upload a PDF file to be processed and stored in the vector database.

```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_document.pdf"
```

Response:
```json
{
  "status": "success",
  "filename": "your_document.pdf",
  "chunks_processed": 42,
  "message": "Successfully processed and stored 42 chunks"
}
```

**What happens:**
1. PDF file is saved temporarily
2. `process_pdf()` loads and splits the document (chunk_size=1000, overlap=100)
3. Chunks are embedded and stored in ChromaDB via `VectorService`
4. Temporary file is cleaned up

### 🔍 MCP Tool - consult_policy_db

**MCP Tool mounted at /mcp**

The `consult_policy_db(query: str)` tool is available through the MCP interface.

**Tool Signature:**
```python
@mcp.tool()
def consult_policy_db(query: str) -> str:
    """
    Consult the policy database using semantic search
    """
```

**Functionality:**
- Calls `VectorService.search(query, k=3)`
- Returns top 3 most relevant document chunks
- Formatted output includes:
  - Source filename
  - Page number
  - Relevance score
  - Content text

**Example Output:**
```
Found 3 relevant policy documents:

--- Result 1 ---
Source: company_policy.pdf
Page: 5
Relevance Score: 0.8532
Content:
[Document chunk content here...]

--- Result 2 ---
Source: company_policy.pdf
Page: 12
Relevance Score: 0.7821
Content:
[Document chunk content here...]

--- Result 3 ---
...
```

## Interactive API Documentation

Visit these URLs when the server is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Root**: http://localhost:8000/

## Architecture

```
┌─────────────┐
│   FastAPI   │
│   /upload   │  ← Upload PDFs
└──────┬──────┘
       │
       ├─────────────┐
       │             │
┌──────▼──────┐  ┌──▼─────────┐
│  Ingestor   │  │  FastMCP   │
│ process_pdf │  │  /mcp      │
└──────┬──────┘  └──┬─────────┘
       │            │
       │     ┌──────▼──────────────┐
       │     │ consult_policy_db() │
       │     └──────┬──────────────┘
       │            │
       └────────────┘
              │
       ┌──────▼──────────┐
       │  VectorService  │
       │   - ChromaDB    │
       │   - Embeddings  │
       └─────────────────┘
```

## Component Details

### VectorService
- **Location**: `app/services/vector_store.py`
- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Storage**: `./chroma_db` (persistent)
- **Methods**:
  - `add_documents(texts, metadatas)`
  - `search(query, k=3)`

### Ingestor
- **Location**: `app/services/ingestor.py`
- **Function**: `process_pdf(file_path)`
- **Loader**: PyPDFLoader
- **Splitter**: RecursiveCharacterTextSplitter
  - chunk_size: 1000
  - chunk_overlap: 100

### MCP Integration
- **Server Name**: "AgentPolicy"
- **Mount Point**: `/mcp`
- **Tools**: `consult_policy_db`

## Example Workflow

1. **Upload a PDF document:**
   ```bash
   curl -X POST "http://localhost:8000/upload" \
     -F "file=@employee_handbook.pdf"
   ```

2. **Query via MCP Tool:**
   - The MCP tool `consult_policy_db` can be called by MCP clients
   - Query example: "What is the vacation policy?"
   - Returns relevant sections from uploaded documents

3. **View in ChromaDB:**
   - Documents are persisted in `./chroma_db/`
   - Survives server restarts

## Troubleshooting

### Import Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### ChromaDB Errors
If you encounter ChromaDB issues, delete the database and restart:
```bash
rm -rf ./chroma_db
python app/main.py
```

### PDF Processing Errors
Ensure the PDF is not corrupted and is a valid PDF file format.

## Next Steps

- Add authentication to the upload endpoint
- Implement batch upload functionality
- Add document deletion endpoint
- Enhance metadata tracking
- Add more MCP tools for advanced queries

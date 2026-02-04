# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Setup Environment

```bash
# Make the scripts executable
chmod +x setup_env.sh run.sh

# Run setup (creates venv and installs dependencies)
./setup_env.sh
```

**Or manually:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
# Simple way
./run.sh

# Or manually
source venv/bin/activate
python app/main.py
```

The server will start at: **http://localhost:8000**

### Step 3: Test It!

**Option A: Using the Browser**
1. Open: http://localhost:8000/docs
2. Try the `/upload` endpoint
3. Upload a PDF file

**Option B: Using curl**
```bash
# Upload a PDF
curl -X POST "http://localhost:8000/upload" \
  -F "file=@/path/to/your/document.pdf"

# Test the root endpoint
curl http://localhost:8000/
```

## 📋 What You Get

### Endpoints Available:

- **GET /** - API information
- **POST /upload** - Upload and process PDF files
- **GET /docs** - Interactive API documentation
- **GET /mcp** - MCP server endpoint

### MCP Tool Available:

- **consult_policy_db(query: str)** - Search the policy database

## 🔧 Troubleshooting

### Import Errors?
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Virtual Environment Issues?
```bash
rm -rf venv
./setup_env.sh
```

### Port Already in Use?
Edit `app/main.py` line 157 to change the port:
```python
port=8001,  # Change from 8000 to 8001
```

### ChromaDB Issues?
```bash
rm -rf ./chroma_db
python app/main.py
```

## 📖 Example Workflow

1. **Start the server:**
   ```bash
   ./run.sh
   ```

2. **Upload a PDF:**
   ```bash
   curl -X POST "http://localhost:8000/upload" \
     -F "file=@employee_handbook.pdf"
   ```
   
   Response:
   ```json
   {
     "status": "success",
     "filename": "employee_handbook.pdf",
     "chunks_processed": 45,
     "message": "Successfully processed and stored 45 chunks"
   }
   ```

3. **Query via MCP:**
   - The MCP tool `consult_policy_db` is now available
   - It searches the uploaded documents
   - Returns the top 3 most relevant chunks

## 🎯 What Happens When You Upload?

1. ✅ PDF is saved temporarily
2. ✅ PyPDFLoader extracts text from all pages
3. ✅ RecursiveCharacterTextSplitter chunks the text (size=1000, overlap=100)
4. ✅ HuggingFace embeddings are generated (all-MiniLM-L6-v2)
5. ✅ Chunks are stored in ChromaDB (./chroma_db)
6. ✅ Temp file is cleaned up

## 📊 Project Structure

```
app/
├── main.py              # Main FastAPI + MCP application
├── services/
│   ├── vector_store.py  # VectorService (ChromaDB)
│   └── ingestor.py      # PDF processing
└── ...

./chroma_db/             # Vector database (auto-created)
requirements.txt         # Dependencies
```

## 🔍 Testing the Installation

```bash
# Activate environment
source venv/bin/activate

# Test imports
python test_imports.py

# Should see:
# ✓ Testing FastAPI...
# ✓ Testing MCP...
# ✓ Testing ChromaDB...
# ✓ Testing LangChain...
# ✅ All imports successful!
```

## 💡 Next Steps

- Upload your first PDF document
- Test the MCP tool through an MCP client
- Modify chunk size/overlap in `ingestor.py`
- Add more MCP tools in `main.py`

## 🆘 Need Help?

Check the full documentation:
- `README.md` - Complete project overview
- `USAGE.md` - Detailed usage guide
- API docs at http://localhost:8000/docs

## 🎉 You're Ready!

Your Agentic RAG API is now running with:
- ✅ FastAPI web framework
- ✅ ChromaDB vector storage
- ✅ HuggingFace embeddings
- ✅ LangChain document processing
- ✅ MCP tool integration

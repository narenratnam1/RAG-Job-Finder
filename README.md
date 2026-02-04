# Agentic RAG FastAPI Project

A modular FastAPI application for Retrieval Augmented Generation (RAG) using ChromaDB, LangChain, and HuggingFace embeddings.

## 🏗️ Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   ├── health.py          # Health check endpoints
│   │   ├── documents.py       # Document management endpoints
│   │   └── rag.py             # RAG query endpoints
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── vector_store.py    # ChromaDB vector store service
│   │   ├── ingestion.py       # Document ingestion service
│   │   └── rag_engine.py      # RAG query engine
│   └── core/                   # Core configuration
│       ├── __init__.py
│       └── config.py          # Application settings
├── data/                       # Data directory (created automatically)
│   └── chroma_db/             # ChromaDB persistence
├── requirements.txt            # Python dependencies
├── setup_env.sh               # Virtual environment setup script
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore file
└── README.md                  # This file
```

## 🚀 Quick Start

### 1. Setup Virtual Environment

Run the setup script to create a virtual environment and install dependencies:

```bash
chmod +x setup_env.sh
./setup_env.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file and update with your settings:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys if needed.

### 3. Run the Application

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Start the FastAPI server
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 API Endpoints

### Health Checks
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/ready` - Readiness check with service status

### Document Management
- `POST /api/v1/documents/upload` - Upload and ingest a document
- `GET /api/v1/documents/list` - List all documents
- `DELETE /api/v1/documents/{document_id}` - Delete a document

### RAG Operations
- `POST /api/v1/rag/query` - Query the RAG system with a question
- `POST /api/v1/rag/search` - Perform semantic search without generation

## 📝 Example Usage

### Upload a Document

```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_document.pdf"
```

### Query the RAG System

```bash
curl -X POST "http://localhost:8000/api/v1/rag/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main topic of the document?",
    "top_k": 5,
    "include_sources": true
  }'
```

### Perform Semantic Search

```bash
curl -X POST "http://localhost:8000/api/v1/rag/search?query=machine%20learning&top_k=5"
```

## 🛠️ Technologies Used

- **FastAPI**: Modern web framework for building APIs
- **ChromaDB**: Vector database for embeddings
- **LangChain**: Framework for LLM applications
- **HuggingFace**: Embeddings models
- **PyPDF**: PDF text extraction
- **Uvicorn**: ASGI server

## 🔧 Configuration

Key configuration options in `.env`:

- `CHROMA_PERSIST_DIRECTORY`: Where to store vector database
- `EMBEDDING_MODEL_NAME`: HuggingFace embedding model to use
- `MAX_UPLOAD_SIZE`: Maximum file upload size in bytes
- `ALLOWED_EXTENSIONS`: Comma-separated list of allowed file extensions

## 📦 Dependencies

See `requirements.txt` for all dependencies. Key packages:

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `mcp[cli]` - Model Context Protocol
- `chromadb` - Vector database
- `langchain-community` - LangChain integrations
- `langchain-huggingface` - HuggingFace embeddings
- `pypdf` - PDF processing
- `python-multipart` - File upload support

## 🔮 Next Steps

1. **Integrate LLM**: Add OpenAI, Anthropic, or local LLM for answer generation
2. **Add Authentication**: Implement user authentication and authorization
3. **Enhance Chunking**: Implement more sophisticated text chunking strategies
4. **Add Caching**: Cache embeddings and responses for better performance
5. **Monitoring**: Add logging, metrics, and monitoring
6. **Testing**: Add unit and integration tests

## 📄 License

MIT License

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

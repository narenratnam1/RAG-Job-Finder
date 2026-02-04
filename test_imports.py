"""
Quick test to verify all imports work correctly
"""

print("Testing imports...")

try:
    print("✓ Testing FastAPI...")
    from fastapi import FastAPI, UploadFile, File
    
    print("✓ Testing MCP...")
    from mcp.server.fastmcp import FastMCP
    
    print("✓ Testing ChromaDB...")
    import chromadb
    from chromadb.config import Settings as ChromaSettings
    
    print("✓ Testing LangChain...")
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain.schema import Document
    
    print("✓ Testing LangChain HuggingFace...")
    from langchain_huggingface import HuggingFaceEmbeddings
    
    print("✓ Testing PyPDF...")
    from pypdf import PdfReader
    
    print("✓ Testing app services...")
    from app.services.vector_store import VectorService
    from app.services.ingestor import process_pdf
    
    print("\n✅ All imports successful!")
    print("Your project is ready to run!")
    
except ImportError as e:
    print(f"\n❌ Import error: {e}")
    print("\nPlease run: pip install -r requirements.txt")
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")

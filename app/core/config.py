"""
Application configuration and settings
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application Settings
    APP_NAME: str = "Agentic RAG API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Vector Store Settings
    CHROMA_PERSIST_DIRECTORY: str = "./data/chroma_db"
    CHROMA_COLLECTION_NAME: str = "rag_documents"
    
    # Model Settings
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL_NAME: str = "gpt-3.5-turbo"
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    HUGGINGFACE_API_KEY: Optional[str] = None
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_INDEX_NAME: str = "resume-index"
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: str = ".pdf,.txt,.doc,.docx"
    
    # MCP Settings (frontend dev server URL — informational)
    MCP_SERVER_URL: str = "http://localhost:3000"
    # Streamable HTTP MCP endpoint (this API’s FastMCP mount); used by the in-process MCP client
    MCP_STREAMABLE_HTTP_URL: str = "http://127.0.0.1:8000/mcp/"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

"""
Document ingestion and processing service
"""

from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def process_pdf(file_path: str) -> List[Document]:
    """
    Process a PDF file and return document chunks ready for vector store
    
    Args:
        file_path: Path to the PDF file to process
    
    Returns:
        List of Document chunks with text and metadata
    """
    # Load the PDF file using PyPDFLoader
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # Initialize RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    
    # Split documents into chunks
    chunks = text_splitter.split_documents(documents)
    
    return chunks

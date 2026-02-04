"""
Vector store service using ChromaDB
"""

import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any
from langchain_huggingface import HuggingFaceEmbeddings
import os
import uuid


class VectorService:
    """Service for managing vector store operations with ChromaDB"""
    
    def __init__(self):
        """Initialize ChromaDB client and HuggingFace embeddings"""
        # Initialize HuggingFace embeddings with all-MiniLM-L6-v2 model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Set persist directory
        self.persist_directory = "./chroma_db"
        
        # Create persist directory if it doesn't exist
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize persistent ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Get or create default collection
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"description": "RAG document embeddings"}
        )
        
        print(f"✓ VectorService initialized with {self.persist_directory}")
    
    def add_documents(self, texts: List[str], metadatas: List[dict]) -> None:
        """
        Add documents to the vector store
        
        Args:
            texts: List of text chunks to save
            metadatas: List of metadata dictionaries for each chunk
        """
        # Generate unique IDs for each document
        ids = [str(uuid.uuid4()) for _ in texts]
        
        # Generate embeddings
        embeddings = self.embeddings.embed_documents(texts)
        
        # Add to ChromaDB collection
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✓ Added {len(texts)} documents to vector store")
    
    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve similar chunks based on query
        
        Args:
            query: The search query string
            k: Number of similar chunks to retrieve (default: 3)
        
        Returns:
            List of dictionaries containing similar documents with metadata
        """
        # Generate query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        # Query ChromaDB for similar documents
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        # Format results
        formatted_results: List[Dict[str, Any]] = []
        
        if results and results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "id": results['ids'][0][i],
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i]
                })
        
        return formatted_results

"""
Vector store service using Pinecone (production) or ChromaDB (local fallback)
"""

import os
from typing import List, Dict, Any
from langchain_huggingface import HuggingFaceEmbeddings
import uuid

# Try to import Pinecone
try:
    from pinecone import Pinecone, ServerlessSpec
    from langchain_pinecone import PineconeVectorStore
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False
    print("⚠️  Pinecone not installed. Falling back to ChromaDB.")

# Always import ChromaDB as fallback
import chromadb
from chromadb.config import Settings as ChromaSettings


class VectorService:
    """Service for managing vector store operations with Pinecone (production) or ChromaDB (local)"""
    
    def __init__(self):
        """Initialize vector store (Pinecone or ChromaDB) and HuggingFace embeddings"""
        # Initialize HuggingFace embeddings with all-MiniLM-L6-v2 model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Check for Pinecone configuration
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "resume-index")
        
        # Try to initialize Pinecone if credentials are available
        if PINECONE_AVAILABLE and pinecone_api_key and pinecone_api_key != "your_pinecone_api_key_here":
            try:
                self._init_pinecone(pinecone_api_key, pinecone_index_name)
                self.backend = "pinecone"
                print(f"✓ VectorService initialized with Pinecone (index: {pinecone_index_name})")
                return
            except Exception as e:
                print(f"⚠️  Pinecone initialization failed: {e}")
                print("⚠️  Falling back to ChromaDB")
        
        # Fallback to ChromaDB
        self._init_chromadb()
        self.backend = "chromadb"
        print(f"✓ VectorService initialized with ChromaDB (local)")
    
    def _init_pinecone(self, api_key: str, index_name: str):
        """Initialize Pinecone vector store"""
        # Initialize Pinecone client
        pc = Pinecone(api_key=api_key)
        
        # Check if index exists, create if not
        existing_indexes = [index.name for index in pc.list_indexes()]
        
        if index_name not in existing_indexes:
            print(f"⚠️  Index '{index_name}' not found. Creating...")
            pc.create_index(
                name=index_name,
                dimension=384,  # all-MiniLM-L6-v2 embedding dimension
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            print(f"✓ Created Pinecone index: {index_name}")
        
        # Initialize LangChain Pinecone vector store
        self.vectorstore = PineconeVectorStore(
            index_name=index_name,
            embedding=self.embeddings,
            pinecone_api_key=api_key
        )
        
        self.index_name = index_name
    
    def _init_chromadb(self):
        """Initialize ChromaDB vector store (fallback)"""
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
    
    def add_documents(self, texts: List[str], metadatas: List[dict]) -> None:
        """
        Add documents to the vector store
        
        Args:
            texts: List of text chunks to save
            metadatas: List of metadata dictionaries for each chunk
        """
        if self.backend == "pinecone":
            # Pinecone: Use LangChain's add_texts method
            self.vectorstore.add_texts(
                texts=texts,
                metadatas=metadatas
            )
            print(f"✓ Added {len(texts)} documents to Pinecone")
        
        else:
            # ChromaDB: Use direct collection method
            ids = [str(uuid.uuid4()) for _ in texts]
            embeddings = self.embeddings.embed_documents(texts)
            
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✓ Added {len(texts)} documents to ChromaDB")
    
    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve similar chunks based on query
        
        Args:
            query: The search query string
            k: Number of similar chunks to retrieve (default: 3)
        
        Returns:
            List of dictionaries containing similar documents with metadata
        """
        if self.backend == "pinecone":
            # Pinecone: Use LangChain's similarity_search_with_score
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            
            # Format results to match ChromaDB structure
            formatted_results: List[Dict[str, Any]] = []
            for doc, score in results:
                formatted_results.append({
                    "id": doc.metadata.get("id", str(uuid.uuid4())),
                    "text": doc.page_content,
                    "metadata": doc.metadata,
                    "distance": 1 - score  # Convert score to distance (Pinecone uses similarity, ChromaDB uses distance)
                })
            
            return formatted_results
        
        else:
            # ChromaDB: Use direct collection query
            query_embedding = self.embeddings.embed_query(query)
            
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

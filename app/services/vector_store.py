"""
Vector store service using Pinecone (production) with client-side embeddings or ChromaDB (local fallback)
"""

import os
import time
from typing import List, Dict, Any
import uuid
from dotenv import load_dotenv

# Load environment variables before anything else
load_dotenv()

# Try to import Pinecone and LangChain Pinecone
try:
    from pinecone import Pinecone, ServerlessSpec
    from langchain_pinecone import PineconeVectorStore
    PINECONE_AVAILABLE = True
except ImportError as e:
    PINECONE_AVAILABLE = False
    print(f"⚠️  Pinecone not installed: {e}. Falling back to ChromaDB.")

# Try to import OpenAI Embeddings for Pinecone
try:
    from langchain_openai import OpenAIEmbeddings
    OPENAI_EMBEDDINGS_AVAILABLE = True
except ImportError:
    OPENAI_EMBEDDINGS_AVAILABLE = False
    print("⚠️  OpenAI embeddings not available. Will use HuggingFace.")

# Always import ChromaDB and HuggingFace as fallback
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_huggingface import HuggingFaceEmbeddings


class VectorService:
    """Service for managing vector store operations with Pinecone (production) or ChromaDB (local)"""
    
    def __init__(self):
        """Initialize vector store (Pinecone or ChromaDB)"""
        # Check for Pinecone configuration
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "resume-index")
        
        print(f"🔍 DEBUG: PINECONE_API_KEY={'SET' if pinecone_api_key else 'NOT SET'}")
        print(f"🔍 DEBUG: PINECONE_INDEX_NAME={pinecone_index_name}")
        print(f"🔍 DEBUG: PINECONE_AVAILABLE={PINECONE_AVAILABLE}")
        
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
        
        # Fallback to ChromaDB with HuggingFace embeddings
        self._init_chromadb()
        self.backend = "chromadb"
        print(f"✓ VectorService initialized with ChromaDB (local)")
    
    def _init_pinecone(self, api_key: str, index_name: str):
        """Initialize Pinecone vector store with CLIENT-SIDE OpenAI embeddings"""
        # Initialize Pinecone client
        self.pc = Pinecone(api_key=api_key)
        self.index_name = index_name
        
        # Initialize OpenAI embeddings for CLIENT-SIDE generation
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key or openai_api_key == "your_openai_api_key_here":
            raise Exception("OPENAI_API_KEY required for Pinecone client-side embeddings")
        
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",  # 1536 dimensions
            api_key=openai_api_key
        )
        print(f"  Using OpenAI embeddings (text-embedding-3-small, 1536d)")
        
        # Check if index exists
        existing_indexes = [index.name for index in self.pc.list_indexes()]
        
        if index_name not in existing_indexes:
            print(f"⚠️  Index '{index_name}' not found. Creating...")
            # Create index with correct dimension for OpenAI embeddings
            self.pc.create_index(
                name=index_name,
                dimension=1536,  # text-embedding-3-small dimension
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            print(f"✓ Created Pinecone index: {index_name}")
            # Wait for index to be ready
            time.sleep(5)
        
        # Initialize LangChain PineconeVectorStore with CLIENT-SIDE embeddings
        self.vectorstore = PineconeVectorStore(
            index_name=index_name,
            embedding=self.embeddings,  # CRITICAL: Client-side embeddings
            pinecone_api_key=api_key
        )
        
        # Get index stats for verification
        index = self.pc.Index(index_name)
        stats = index.describe_index_stats()
        print(f"  Index stats: {stats.get('total_vector_count', 0)} vectors")
    
    def _init_chromadb(self):
        """Initialize ChromaDB vector store (fallback) with HuggingFace embeddings"""
        # Initialize HuggingFace embeddings for ChromaDB fallback
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
    
    def add_documents(self, texts: List[str], metadatas: List[dict]) -> None:
        """
        Add documents to the vector store
        
        Args:
            texts: List of text chunks to save
            metadatas: List of metadata dictionaries for each chunk
        """
        if self.backend == "pinecone":
            # Pinecone: Use LangChain's add_texts method with CLIENT-SIDE embeddings
            # The embeddings are generated by OpenAI (client-side), NOT Pinecone inference
            self.vectorstore.add_texts(
                texts=texts,
                metadatas=metadatas
            )
            print(f"✓ Added {len(texts)} documents to Pinecone (client-side OpenAI embeddings)")
        
        else:
            # ChromaDB: Use direct collection method with HuggingFace embeddings
            ids = [str(uuid.uuid4()) for _ in texts]
            embeddings = self.embeddings.embed_documents(texts)
            
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✓ Added {len(texts)} documents to ChromaDB")
    
    def search(self, query: str, k: int = 3, namespace: str = None) -> List[Dict[str, Any]]:
        """
        Retrieve similar chunks based on query
        
        Args:
            query: The search query string
            k: Number of similar chunks to retrieve (default: 3)
            namespace: Optional namespace to search in (Pinecone only, not used with client-side embeddings)
        
        Returns:
            List of dictionaries containing similar documents with metadata
        """
        if self.backend == "pinecone":
            # Pinecone: Use LangChain's similarity_search_with_score
            # Embeddings are generated CLIENT-SIDE by OpenAI, NOT by Pinecone inference
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            
            # Format results to match ChromaDB structure
            formatted_results: List[Dict[str, Any]] = []
            for doc, score in results:
                formatted_results.append({
                    "id": doc.metadata.get("id", str(uuid.uuid4())),
                    "text": doc.page_content,
                    "metadata": doc.metadata,
                    "distance": 1 - score,  # Convert similarity score to distance
                    "score": score
                })
            
            return formatted_results
        
        else:
            # ChromaDB: Use direct collection query with manual embeddings
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
                        "distance": results['distances'][0][i],
                        "score": 1 - results['distances'][0][i]  # Convert distance to similarity score
                    })
            
            return formatted_results
    
    def delete_namespace(self, namespace: str) -> bool:
        """
        Delete all records in a namespace (Pinecone only)
        Note: When using client-side embeddings, namespaces are handled by LangChain
        and deletion is not directly supported. Use Pinecone dashboard instead.
        
        Args:
            namespace: The namespace to delete
        
        Returns:
            False (not supported with client-side embeddings)
        """
        print("⚠️  Namespace deletion not directly supported with client-side embeddings")
        print("   Use Pinecone dashboard to delete specific vectors by metadata filters")
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store
        
        Returns:
            Dictionary with stats about the vector store
        """
        if self.backend == "pinecone":
            index = self.pc.Index(self.index_name)
            stats = index.describe_index_stats()
            return {
                "backend": "pinecone",
                "index_name": self.index_name,
                "total_vectors": stats.get('total_vector_count', 0),
                "dimension": 1536,
                "embedding_model": "text-embedding-3-small (OpenAI)"
            }
        else:
            count = self.collection.count()
            return {
                "backend": "chromadb",
                "total_documents": count,
                "persist_directory": self.persist_directory,
                "embedding_model": "all-MiniLM-L6-v2 (HuggingFace)"
            }

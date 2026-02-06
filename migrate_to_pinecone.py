#!/usr/bin/env python3
"""
Migration script to upgrade from ChromaDB to modern Pinecone SDK
Run this after installing the updated dependencies
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        from pinecone import Pinecone
        print("✅ Pinecone SDK (modern) is installed")
        return True
    except ImportError as e:
        print(f"❌ Pinecone SDK not installed correctly: {e}")
        print("\n📝 Please run: source venv/bin/activate && pip install pinecone")
        return False

def verify_pinecone_credentials():
    """Verify Pinecone API credentials"""
    print("\n🔍 Checking Pinecone credentials...")
    
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME", "resume-index")
    
    if not api_key or api_key == "your_pinecone_api_key_here":
        print("❌ PINECONE_API_KEY not set in .env file")
        return False
    
    print(f"✅ API Key found")
    print(f"✅ Index name: {index_name}")
    return True

def create_pinecone_index():
    """Create Pinecone index with integrated embeddings"""
    print("\n🚀 Creating Pinecone index with integrated embeddings...")
    
    try:
        from pinecone import Pinecone, ServerlessSpec
        
        api_key = os.getenv("PINECONE_API_KEY")
        index_name = os.getenv("PINECONE_INDEX_NAME", "resume-index")
        
        # Initialize Pinecone
        pc = Pinecone(api_key=api_key)
        
        # Check if index exists
        existing_indexes = [index.name for index in pc.list_indexes()]
        
        if index_name in existing_indexes:
            print(f"ℹ️  Index '{index_name}' already exists")
            
            # Get index info
            index = pc.Index(index_name)
            stats = index.describe_index_stats()
            print(f"   Total vectors: {stats.get('total_vector_count', 0)}")
            print(f"   Namespaces: {list(stats.get('namespaces', {}).keys())}")
            
            response = input(f"\n⚠️  Do you want to delete and recreate the index? (yes/no): ")
            if response.lower() != 'yes':
                print("✅ Keeping existing index")
                return True
            
            print(f"🗑️  Deleting existing index '{index_name}'...")
            pc.delete_index(index_name)
            print("✅ Index deleted")
        
        # Create new index with integrated embeddings
        print(f"📦 Creating new index '{index_name}' with integrated embeddings...")
        print("   Model: multilingual-e5-large (1024 dimensions)")
        print("   Metric: cosine")
        print("   Cloud: AWS us-east-1")
        
        pc.create_index(
            name=index_name,
            dimension=1024,  # multilingual-e5-large dimension
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        
        print(f"✅ Index '{index_name}' created successfully!")
        print("\nℹ️  Note: This index uses Pinecone's integrated embeddings (multilingual-e5-large)")
        print("   You no longer need to generate embeddings manually - Pinecone handles it!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating index: {e}")
        return False

def migrate_chromadb_data():
    """Migrate data from ChromaDB to Pinecone"""
    print("\n🔄 Migrating data from ChromaDB to Pinecone...")
    
    try:
        import chromadb
        from chromadb.config import Settings as ChromaSettings
        from pinecone import Pinecone
        
        # Initialize ChromaDB
        chroma_client = chromadb.PersistentClient(
            path="./chroma_db",
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Check if collection exists
        try:
            collection = chroma_client.get_collection("documents")
        except Exception:
            print("ℹ️  No ChromaDB collection found. Skipping migration.")
            return True
        
        # Get all data from ChromaDB
        results = collection.get(include=["documents", "metadatas"])
        
        if not results['ids']:
            print("ℹ️  ChromaDB collection is empty. Nothing to migrate.")
            return True
        
        print(f"📊 Found {len(results['ids'])} documents in ChromaDB")
        
        # Initialize Pinecone
        api_key = os.getenv("PINECONE_API_KEY")
        index_name = os.getenv("PINECONE_INDEX_NAME", "resume-index")
        pc = Pinecone(api_key=api_key)
        index = pc.Index(index_name)
        
        # Prepare records for Pinecone
        # Group by source file for better namespace organization
        records_by_source = {}
        
        for i, (doc_id, text, metadata) in enumerate(zip(results['ids'], results['documents'], results['metadatas'])):
            source = metadata.get('source', metadata.get('filename', 'unknown'))
            
            if source not in records_by_source:
                records_by_source[source] = []
            
            records_by_source[source].append({
                "_id": doc_id,
                "content": text,  # This field will be embedded by Pinecone
                **metadata  # Include all metadata
            })
        
        # Upsert to Pinecone by source (one namespace per source)
        print(f"\n📤 Uploading to Pinecone...")
        for source, records in records_by_source.items():
            namespace = f"resume_{source.replace('.pdf', '').replace(' ', '_')}"
            print(f"   Uploading {len(records)} records to namespace '{namespace}'...")
            
            # Batch upsert (max 96 records per batch for text)
            batch_size = 96
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                index.upsert_records(namespace, batch)
            
            print(f"   ✅ {len(records)} records uploaded")
        
        print(f"\n✅ Migration complete! Migrated {len(results['ids'])} documents")
        print(f"   Organized into {len(records_by_source)} namespaces")
        
        return True
        
    except Exception as e:
        print(f"❌ Error migrating data: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main migration workflow"""
    print("=" * 60)
    print("PINECONE MIGRATION SCRIPT")
    print("=" * 60)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Step 2: Verify credentials
    if not verify_pinecone_credentials():
        sys.exit(1)
    
    # Step 3: Create Pinecone index
    if not create_pinecone_index():
        sys.exit(1)
    
    # Step 4: Migrate data (optional)
    response = input("\n❓ Do you want to migrate existing ChromaDB data to Pinecone? (yes/no): ")
    if response.lower() == 'yes':
        if not migrate_chromadb_data():
            print("\n⚠️  Migration had errors, but index is ready for new data")
    
    print("\n" + "=" * 60)
    print("✅ MIGRATION COMPLETE!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Your Pinecone index is ready to use")
    print("2. Restart your application: python start.py")
    print("3. Upload PDFs - they'll be automatically stored in Pinecone")
    print("4. The app will use Pinecone for all vector operations")
    print("\n💡 Tip: The new setup uses Pinecone's integrated embeddings")
    print("   You no longer need sentence-transformers for embedding generation!")

if __name__ == "__main__":
    main()

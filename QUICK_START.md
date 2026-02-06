# 🚀 Quick Start: Pinecone Migration

**You're ready to migrate to modern Pinecone!** Here's what to do next.

## ⚡ Quick Installation (3 Steps)

### Step 1: Install the Modern Pinecone SDK

Open your terminal and run:

```bash
cd "/Users/narenratnam/Desktop/RAG and MCP Project"
./install_pinecone.sh
```

This script will:
- ✅ Activate your virtual environment
- ✅ Remove the old `pinecone-client` package
- ✅ Install the new `pinecone` SDK
- ✅ Verify the installation

### Step 2: Create Your Pinecone Index

```bash
# Make sure you're still in the project directory
python migrate_to_pinecone.py
```

This interactive script will:
1. ✅ Check your dependencies
2. ✅ Verify your API credentials
3. ✅ Create a new Pinecone index with integrated embeddings
4. ✅ Ask if you want to migrate existing ChromaDB data (optional)

### Step 3: Use the New Vector Store

Replace your old `vector_store.py`:

```bash
# Backup old file
mv app/services/vector_store.py app/services/vector_store_old.py

# Use new implementation
mv app/services/vector_store_new.py app/services/vector_store.py

# Restart your app
python start.py
```

## ✅ Verification

After starting your app, look for this message in the console:

```
✓ VectorService initialized with Pinecone (index: resume-index)
  Using integrated embeddings: multilingual-e5-large (1024d)
```

If you see that, you're all set! 🎉

## 🔍 What Changed?

### Before (Old Setup)
```python
# Manual embedding generation
embeddings = HuggingFaceEmbeddings(...)
vectors = embeddings.embed_documents(texts)
index.upsert(vectors=vectors, ...)
```

### After (New Setup)
```python
# Automatic embedding generation by Pinecone
index.upsert_records(namespace, [
    {"_id": "1", "content": "text here", "metadata": {...}}
])
```

## 📊 Benefits You Get

1. **Better Embeddings**: Upgraded from 384d to 1024d model
2. **Auto Embeddings**: Pinecone handles it - no manual generation needed
3. **Built-in Reranking**: Better search results automatically
4. **Simpler Code**: Less complexity, easier maintenance
5. **Production Ready**: Using current, maintained SDK
6. **Faster Performance**: Optimized infrastructure

## 🆘 Troubleshooting

### "Permission denied" when running scripts

```bash
chmod +x install_pinecone.sh migrate_to_pinecone.py
./install_pinecone.sh
```

### "Index not found" error

Run the migration script to create the index:
```bash
python migrate_to_pinecone.py
```

### Still using ChromaDB after migration

Check:
1. Is your PINECONE_API_KEY set correctly in `.env`?
2. Did you run `migrate_to_pinecone.py` successfully?
3. Did you replace `vector_store.py` with the new version?
4. Did you restart the application?

### Import errors after installation

```bash
source venv/bin/activate
pip install pinecone
python -c "from pinecone import Pinecone; print('✅ Import successful')"
```

## 📚 Reference Files

- **Detailed Guide**: `PINECONE_MIGRATION_GUIDE.md`
- **Python SDK Guide**: `.agents/PINECONE-python.md`
- **Quickstart Examples**: `.agents/PINECONE-quickstart.md`
- **Universal Guide**: `.agents/PINECONE.md`

## 🎯 Next Steps After Migration

1. **Upload Resumes**: Your app will automatically use Pinecone
2. **Test Search**: Try the candidate search feature
3. **Check Dashboard**: Visit [app.pinecone.io](https://app.pinecone.io/) to see your data
4. **Optimize**: Use namespaces to organize data by user/session/category

## 💡 Pro Tips

### Tip 1: Namespace Strategy
Organize your data with namespaces:
```python
# One namespace per resume
namespace = f"resume_{filename.replace('.pdf', '')}"

# Or per user
namespace = f"user_{user_id}"
```

### Tip 2: Use Reranking
The new code includes reranking for better search results:
```python
results = index.search(
    namespace=namespace,
    query={"inputs": {"text": query}, "top_k": 10},
    rerank={
        "model": "bge-reranker-v2-m3",
        "top_n": 5,
        "rank_fields": ["content"]
    }
)
```

### Tip 3: Monitor Usage
Check your index stats:
```python
stats = vector_service.get_stats()
print(f"Total vectors: {stats['total_vectors']}")
print(f"Namespaces: {stats['namespaces']}")
```

## ✨ You're All Set!

Your RAG system is now powered by modern Pinecone with:
- ✅ State-of-the-art embeddings (multilingual-e5-large)
- ✅ Automatic embedding generation
- ✅ Built-in reranking
- ✅ Production-ready infrastructure
- ✅ Better search quality

**Questions?** Check the guides in `.agents/` folder or the detailed migration guide.

Happy building! 🚀

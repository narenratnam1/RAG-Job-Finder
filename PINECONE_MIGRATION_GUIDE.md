# 🚀 Pinecone Migration Guide

This guide will help you migrate from the old `pinecone-client` to the modern `pinecone` SDK with integrated embeddings.

## ⚠️ Important Changes

### Before (Old Setup)
- ❌ Used `pinecone-client` (deprecated)
- ❌ Required manual embedding generation with sentence-transformers
- ❌ More complex code for vector operations

### After (New Setup)
- ✅ Uses `pinecone` (current SDK)
- ✅ Pinecone handles embeddings automatically with integrated models
- ✅ Simpler code, better performance

## 📋 Migration Steps

### Step 1: Install Updated Dependencies

Open your terminal and run:

```bash
cd "/Users/narenratnam/Desktop/RAG and MCP Project"

# Activate your virtual environment
source venv/bin/activate

# Uninstall old package (if exists)
pip uninstall -y pinecone-client

# Install new Pinecone SDK
pip install pinecone

# Verify installation
pip show pinecone
```

### Step 2: Verify Your .env Configuration

Make sure your `.env` file has:

```bash
# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=resume-index
```

✅ Your .env file is already configured correctly!

### Step 3: Run Migration Script

```bash
# Make sure you're in the project directory with venv activated
python migrate_to_pinecone.py
```

The script will:
1. ✅ Check that dependencies are installed
2. ✅ Verify your Pinecone credentials
3. ✅ Create a new Pinecone index with integrated embeddings
4. ✅ Optionally migrate existing ChromaDB data

### Step 4: Update Your Vector Store Code

I've prepared an updated `vector_store.py` that uses the modern Pinecone SDK. The key changes:

- Uses Pinecone's integrated embeddings (no manual embedding required)
- Simpler upsert/search operations
- Better namespace handling
- Automatic fallback to ChromaDB if Pinecone unavailable

### Step 5: Test Your Setup

```bash
# Restart your application
python start.py
```

Then test by:
1. Uploading a PDF resume
2. Searching for candidates
3. Screening candidates

## 🎯 Key Benefits of New Setup

### 1. Integrated Embeddings
```python
# OLD WAY (manual embeddings)
embeddings = self.embeddings.embed_documents(texts)
index.upsert(vectors=embeddings, ...)

# NEW WAY (automatic embeddings)
index.upsert_records(namespace, [
    {"_id": "1", "content": "text here", "metadata": {...}}
])
```

### 2. Simpler Search
```python
# OLD WAY
query_vector = embeddings.embed_query(query)
results = index.query(vector=query_vector, ...)

# NEW WAY
results = index.search(
    namespace="resumes",
    query={"inputs": {"text": query}, "top_k": 5}
)
```

### 3. Built-in Reranking
```python
results = index.search(
    namespace="resumes",
    query={"inputs": {"text": query}, "top_k": 10},
    rerank={
        "model": "bge-reranker-v2-m3",
        "top_n": 5,
        "rank_fields": ["content"]
    }
)
```

## 📊 Comparing Old vs New Approach

| Feature | Old (pinecone-client) | New (pinecone) |
|---------|----------------------|----------------|
| Package | `pinecone-client` | `pinecone` |
| Embeddings | Manual (sentence-transformers) | Integrated (Pinecone handles it) |
| Embedding Model | all-MiniLM-L6-v2 (384d) | multilingual-e5-large (1024d) |
| Code Complexity | High | Low |
| Performance | Good | Better |
| Reranking | Not built-in | Built-in |
| Maintenance | Deprecated | Actively maintained |

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pinecone'"

**Solution:**
```bash
source venv/bin/activate
pip install pinecone
```

### Issue: "Index not found"

**Solution:**
```bash
python migrate_to_pinecone.py
# This will create the index for you
```

### Issue: "API key invalid"

**Solution:**
1. Check your `.env` file has correct `PINECONE_API_KEY`
2. Get a new key from: https://app.pinecone.io/
3. Update `.env` and restart the app

### Issue: "Still using ChromaDB"

**Solution:**
Check the console output when starting the app:
- ✅ `✓ VectorService initialized with Pinecone` = Success!
- ⚠️ `✓ VectorService initialized with ChromaDB` = Pinecone failed to initialize

If Pinecone failed:
1. Check API key in .env
2. Verify index exists: Run migration script
3. Check error messages in console

## 📚 Additional Resources

- **Pinecone Documentation**: https://docs.pinecone.io/
- **Python SDK Guide**: See `.agents/PINECONE-python.md` in your project
- **Quickstart Examples**: See `.agents/PINECONE-quickstart.md`

## ✅ Post-Migration Checklist

- [ ] Installed new `pinecone` package
- [ ] Ran migration script successfully
- [ ] Verified index exists in Pinecone dashboard
- [ ] Tested upload functionality
- [ ] Tested search functionality
- [ ] Confirmed app uses Pinecone (check console logs)
- [ ] (Optional) Migrated old ChromaDB data

## 🎉 You're All Set!

Your RAG system is now using modern Pinecone with:
- ✅ Better embeddings (multilingual-e5-large)
- ✅ Automatic embedding generation
- ✅ Built-in reranking for better search results
- ✅ Production-ready infrastructure
- ✅ Future-proof codebase

Need help? Check the Pinecone agent guides in `.agents/` folder!

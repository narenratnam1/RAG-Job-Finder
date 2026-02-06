# 🚀 Pinecone Migration Guide

## Overview

Your application now supports **Pinecone** as a production vector database, with automatic fallback to ChromaDB for local development.

---

## ✅ What's Been Done

### 1. Updated Dependencies
```txt
# requirements.txt
pinecone-client>=3.0.0
langchain-pinecone>=0.1.0
```

### 2. Refactored VectorService
- **Dual-mode support**: Pinecone (production) or ChromaDB (local)
- **Automatic fallback**: If Pinecone credentials not found, uses ChromaDB
- **Compatible API**: Same `add_documents()` and `search()` methods

### 3. Environment Variables
```env
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=resume-index
```

---

## 🔧 Setup Instructions

### Step 1: Get Pinecone API Key

1. **Sign up** at https://www.pinecone.io/
2. **Create a new project** (free tier available)
3. **Copy your API key** from the dashboard
4. **Note your region** (default: us-east-1)

### Step 2: Install New Dependencies

```bash
cd /Users/narenratnam/Desktop/RAG\ and\ MCP\ Project
pip install pinecone-client>=3.0.0 langchain-pinecone>=0.1.0
```

### Step 3: Update .env File

Add these lines to your `.env` file:

```env
# Pinecone Configuration
PINECONE_API_KEY=your_actual_api_key_from_pinecone
PINECONE_INDEX_NAME=resume-index
```

**Important:** Replace `your_actual_api_key_from_pinecone` with your real API key!

### Step 4: Restart Backend

```bash
# Press Ctrl+C to stop
python start.py
```

You should see:
```
✓ VectorService initialized with Pinecone (index: resume-index)
```

---

## 🎯 How It Works

### Automatic Backend Selection

The `VectorService` automatically chooses the backend:

```python
if PINECONE_API_KEY is set and valid:
    ✅ Use Pinecone (production)
else:
    ✅ Use ChromaDB (local fallback)
```

### Index Auto-Creation

If the Pinecone index doesn't exist, it will be created automatically:

```python
Index: resume-index
Dimension: 384 (all-MiniLM-L6-v2)
Metric: cosine
Cloud: AWS
Region: us-east-1
```

### Unified API

No code changes needed! Both backends use the same methods:

```python
# Works with both Pinecone and ChromaDB
vector_service.add_documents(texts, metadatas)
vector_service.search(query, k=10)
```

---

## 📊 Comparison: Pinecone vs ChromaDB

| Feature | ChromaDB (Local) | Pinecone (Cloud) |
|---------|------------------|------------------|
| **Deployment** | Local files | Cloud-hosted |
| **Scaling** | Limited | Unlimited |
| **Cost** | Free | Free tier + paid |
| **Speed** | Fast (local) | Fast (distributed) |
| **Persistence** | File-based | Cloud storage |
| **Best For** | Development | Production |

---

## 🧪 Testing

### Test Local (ChromaDB)

1. **Don't set** `PINECONE_API_KEY` in `.env` (or leave it empty)
2. **Start backend**: `python start.py`
3. **Should see**: `✓ VectorService initialized with ChromaDB (local)`

### Test Production (Pinecone)

1. **Set** `PINECONE_API_KEY` in `.env` with real key
2. **Start backend**: `python start.py`
3. **Should see**: `✓ VectorService initialized with Pinecone (index: resume-index)`
4. **Upload a resume** to test
5. **Search** to verify it works

---

## 🔄 Migrating Existing Data

If you have existing resumes in ChromaDB and want to migrate to Pinecone:

### Option 1: Re-upload (Recommended)

1. **Enable Pinecone** (add API key to `.env`)
2. **Restart backend**
3. **Re-upload all resumes** through the UI
   - Go to `http://localhost:3000`
   - Upload each resume again
   - They'll be stored in Pinecone

### Option 2: Migration Script (Advanced)

Create `migrate_to_pinecone.py`:

```python
from app.services.vector_store import VectorService
import os
from dotenv import load_dotenv

load_dotenv()

# This would require custom migration logic
# Not implemented yet - recommend Option 1 instead
```

---

## 🔍 Verification

### Check Which Backend Is Active

Look at the startup logs:

```bash
# ChromaDB (local)
✓ VectorService initialized with ChromaDB (local)

# Pinecone (cloud)
✓ VectorService initialized with Pinecone (index: resume-index)
```

### Check Pinecone Dashboard

1. Go to https://app.pinecone.io/
2. Click on your project
3. View `resume-index`
4. Should see vectors after uploading resumes

---

## 🛠️ Troubleshooting

### Error: "Pinecone initialization failed"

**Cause:** Invalid API key or network issue

**Solution:**
1. Check API key is correct in `.env`
2. Verify internet connection
3. Check Pinecone dashboard is accessible
4. App will automatically fall back to ChromaDB

### Error: "Index not found"

**Cause:** Index doesn't exist (normal on first run)

**Solution:**
- Index is auto-created on first startup
- Wait 30-60 seconds for Pinecone to create it
- Restart backend after index creation

### Different Results Between Backends

**Cause:** Different distance metrics

**Solution:**
- ChromaDB uses L2 distance
- Pinecone uses cosine similarity
- Results should be similar but not identical
- This is expected behavior

---

## 💰 Cost Considerations

### Pinecone Free Tier
- **1 pod** (serverless)
- **1 index**
- **1GB storage**
- Good for ~1M 384-dim vectors

### When to Upgrade
- More than 1M vectors
- Need multiple indexes
- Need dedicated pods
- Higher QPS requirements

---

## 🔒 Security

### API Key Protection
```env
# ✅ GOOD: In .env file (gitignored)
PINECONE_API_KEY=your_key_here

# ❌ BAD: Hard-coded in source
PINECONE_API_KEY="pc-1234..."  # Never do this!
```

### .gitignore Already Configured
```
.env
__pycache__/
*.pyc
```

---

## 📁 Files Modified

### Updated Files
1. ✅ `requirements.txt` - Added Pinecone dependencies
2. ✅ `app/services/vector_store.py` - Dual-mode support
3. ✅ `.env.example` - Added Pinecone variables

### No Changes Needed
- ❌ `app/main.py` (uses same VectorService API)
- ❌ Frontend files (backend change only)
- ❌ Other backend services

---

## 🎯 Production Deployment Checklist

- [ ] Sign up for Pinecone account
- [ ] Get API key from dashboard
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Add `PINECONE_API_KEY` to production `.env`
- [ ] Add `PINECONE_INDEX_NAME` to production `.env`
- [ ] Deploy application
- [ ] Verify Pinecone initialization in logs
- [ ] Test upload functionality
- [ ] Test search functionality
- [ ] Monitor Pinecone dashboard

---

## 🚀 Quick Start

### For Development (ChromaDB)
```bash
# No changes needed!
python start.py
```

### For Production (Pinecone)
```bash
# 1. Add to .env:
echo "PINECONE_API_KEY=your_key" >> .env
echo "PINECONE_INDEX_NAME=resume-index" >> .env

# 2. Install dependencies:
pip install pinecone-client langchain-pinecone

# 3. Start:
python start.py
```

---

## 📖 Additional Resources

- **Pinecone Docs:** https://docs.pinecone.io/
- **LangChain Pinecone:** https://python.langchain.com/docs/integrations/vectorstores/pinecone
- **Pricing:** https://www.pinecone.io/pricing/

---

## ✅ Summary

**What Changed:**
- ✅ Added Pinecone support for production
- ✅ Kept ChromaDB for local development
- ✅ Automatic fallback between backends
- ✅ Same API, no code changes needed

**Next Steps:**
1. Get Pinecone API key
2. Add to `.env` file
3. Install dependencies
4. Restart backend
5. Upload resumes
6. Enjoy cloud-scale vector search!

---

**Status:** ✅ Ready for Production  
**Date:** February 5, 2026  
**Migration Path:** Seamless (no data loss)

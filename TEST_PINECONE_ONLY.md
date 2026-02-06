# 🧪 Test Pinecone-Only Setup

**Status:** Ready to test

---

## ✅ What Changed

1. **Removed ChromaDB completely** - No fallback logic
2. **Pinecone is now REQUIRED** - App fails fast if credentials missing
3. **Cleaner code** - Removed ~150 lines of fallback code

---

## 🚀 Quick Test

### 1. Start Backend

```bash
cd "/Users/narenratnam/Desktop/RAG and MCP Project"
python start.py
```

**Expected logs:**
```
🔍 DEBUG: PINECONE_API_KEY=SET
🔍 DEBUG: PINECONE_INDEX_NAME=resume-index
  Using OpenAI embeddings (text-embedding-3-small, 1536d)
✓ VectorService initialized with Pinecone (index: resume-index)
  Index stats: N vectors
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Should NOT see:**
- ❌ "Falling back to ChromaDB"
- ❌ "ChromaDB initialized"
- ❌ Any ChromaDB mentions

### 2. Test Health Endpoint

```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{
  "status": "healthy",
  "vector_store": "operational"
}
```

### 3. Upload a Resume

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@/path/to/resume.pdf"
```

**Expected backend log:**
```
✓ Added 5 documents to Pinecone (client-side OpenAI embeddings)
```

### 4. Search Candidates

```bash
curl -X POST http://localhost:8000/search_candidates \
  -H "Content-Type: application/json" \
  -d '{"job_description": "Python developer with FastAPI experience"}'
```

**Should return:** Top 7 candidates from Pinecone

---

## 🚨 Error Scenarios (Now Fail Fast)

### If PINECONE_API_KEY Missing:

**Before (with ChromaDB fallback):**
```
⚠️  Pinecone initialization failed
⚠️  Falling back to ChromaDB
✓ VectorService initialized with ChromaDB (local)
```

**Now (Pinecone-only):**
```
ValueError: PINECONE_API_KEY is required. Please set it in your .env file.
Get your API key from: https://app.pinecone.io/
[App crashes - as expected]
```

### If OPENAI_API_KEY Missing:

**Error:**
```
ValueError: OPENAI_API_KEY required for Pinecone client-side embeddings
[App crashes - as expected]
```

---

## ✅ Success Criteria

- [ ] Backend starts without errors
- [ ] No ChromaDB logs appear
- [ ] Health endpoint returns 200
- [ ] Can upload resume (logs show Pinecone)
- [ ] Can search candidates (returns results)
- [ ] No import errors
- [ ] No "falling back" messages

---

## 📊 Code Verification

### Check Imports:

```bash
# Should find NO matches
grep -r "chromadb\|ChromaDB" app/*.py
```

**Result:** No matches ✅

### Check Active Code:

```python
# Test import
python -c "from app.services.vector_store import VectorService; print('✅ Success')"
```

**Result:** ✅ Success (no import errors)

---

## 🎯 Next Steps

1. **Test locally** (use commands above)
2. **Verify Pinecone dashboard** shows vectors after upload
3. **Commit changes:**
   ```bash
   git add app/services/vector_store.py app/main.py CHROMADB_REMOVED.md TEST_PINECONE_ONLY.md
   git commit -m "Remove ChromaDB - use Pinecone exclusively"
   git push origin main
   ```
4. **Deploy to Railway** (will be ~550MB lighter)

---

**Status:** ✅ Ready to test!

_Run `python start.py` to verify everything works!_

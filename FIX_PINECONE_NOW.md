# ⚡ Fix Pinecone Inference Error - Action Plan

## 🚨 Error Fixed!

**Error:** "Inference is not configured for this index"

**Cause:** Code was using Pinecone's server-side inference API, but your index is a standard vector store.

**Solution:** Updated code to use OpenAI client-side embeddings ✅

---

## 🚀 5-Step Fix (3 Minutes)

### Step 1: Delete Old Pinecone Index

1. Go to https://app.pinecone.io/
2. Find `resume-index`
3. Click "Delete" or "Remove"
4. Confirm deletion

**Why:** Old index has wrong dimensions (1024) - needs 1536 for OpenAI embeddings

### Step 2: Stop Backend

```bash
# In terminal 4
Ctrl+C
```

### Step 3: Clear Local Database

```bash
rm -rf chroma_db
```

### Step 4: Restart Backend

```bash
python start.py
```

### Step 5: Watch Logs

**You should see:**
```
🔍 DEBUG: PINECONE_API_KEY=SET
🔍 DEBUG: PINECONE_AVAILABLE=True
⚠️  Index 'resume-index' not found. Creating...
✓ Created Pinecone index: resume-index
  Using OpenAI embeddings (text-embedding-3-small, 1536d)
✓ VectorService initialized with Pinecone (index: resume-index)
  Index stats: 0 vectors
✓ Mounted static files: /static/resumes
```

---

## 🧪 Step 6: Test Upload

1. Go to `http://localhost:3000`
2. Upload a resume
3. **Backend should show:**
   ```
   ✓ Added 5 documents to Pinecone (client-side OpenAI embeddings)
   ```

4. **Pinecone dashboard** (https://app.pinecone.io/):
   - Refresh page
   - Click `resume-index`
   - Should see vectors appear!

---

## ✅ What Was Changed

### Fixed `vector_store.py`:

1. **Import OpenAI Embeddings:**
   ```python
   from langchain_openai import OpenAIEmbeddings
   from langchain_pinecone import PineconeVectorStore
   ```

2. **Initialize with Client-Side Embeddings:**
   ```python
   self.embeddings = OpenAIEmbeddings(
       model="text-embedding-3-small",  # 1536 dimensions
       api_key=openai_api_key
   )
   ```

3. **Create Index with Correct Dimensions:**
   ```python
   dimension=1536,  # For OpenAI text-embedding-3-small
   ```

4. **Pass Embeddings to PineconeVectorStore:**
   ```python
   self.vectorstore = PineconeVectorStore(
       index_name=index_name,
       embedding=self.embeddings,  # CLIENT-SIDE!
       pinecone_api_key=api_key
   )
   ```

5. **Use LangChain Methods (not direct Pinecone API):**
   ```python
   # Upload
   self.vectorstore.add_texts(texts, metadatas)
   
   # Search
   self.vectorstore.similarity_search_with_score(query, k)
   ```

---

## 🔍 How It Works

### Old Way (BROKEN):
```
Text → Pinecone.upsert_records() → Pinecone embeds it → Error!
```

### New Way (FIXED):
```
Text → OpenAI embeds it → Pinecone.add_texts() → Stored as vectors ✅
```

---

## 📊 Index Configuration

### New Index Specs:
```
Name: resume-index
Dimension: 1536 (OpenAI text-embedding-3-small)
Metric: cosine
Cloud: AWS us-east-1
Type: Serverless (standard, not inference)
```

---

## 🎯 Expected Results

### Startup (Success):
```
✓ VectorService initialized with Pinecone (index: resume-index)
  Using OpenAI embeddings (text-embedding-3-small, 1536d)
```

### Upload (Success):
```
✓ Added 5 documents to Pinecone (client-side OpenAI embeddings)
✓ Saved resume to library: filename.pdf
```

### Search (Success):
```
✓ Found 10 initial candidates from vector search
Processing candidate #1: source='filename.pdf' ← Clean!
```

---

## 🔍 If Error Still Occurs

### Error: "Dimension mismatch"
**Cause:** Old index still exists with wrong dimensions

**Solution:** Delete index from Pinecone dashboard and restart

### Error: "OPENAI_API_KEY required"
**Cause:** OpenAI API key not set

**Solution:** Check your `.env` has both keys:
```env
OPENAI_API_KEY=sk-proj-...
PINECONE_API_KEY=pcsk_...
```

### Error: "Index not found"
**Cause:** Index doesn't exist yet

**Solution:** Normal! Code will auto-create it. Wait 30-60 seconds.

---

## 📋 Quick Checklist

- [ ] Delete old `resume-index` from Pinecone dashboard
- [ ] Stop backend (Ctrl+C)
- [ ] Clear old database (`rm -rf chroma_db`)
- [ ] Restart backend (`python start.py`)
- [ ] See "Creating index" message
- [ ] Wait for "VectorService initialized with Pinecone"
- [ ] Upload a test resume
- [ ] Verify: "Added to Pinecone" in logs
- [ ] Check Pinecone dashboard shows vectors

---

## 💰 Cost Note

**OpenAI Embeddings:**
- text-embedding-3-small
- ~$0.00002 per 1K tokens
- Very cheap: 1000 resumes ≈ $0.50

---

## ✨ Summary

**Problem:** Pinecone inference error  
**Cause:** Wrong embedding approach  
**Fix:** Use OpenAI client-side embeddings  
**Status:** ✅ Code fixed  
**Action:** Delete old index, restart backend  

---

## 🚀 Ready!

**Next Steps:**
1. Delete `resume-index` from Pinecone dashboard
2. Restart backend
3. Upload resumes
4. Enjoy cloud vector storage!

---

**Date:** February 5, 2026  
**Status:** ✅ Fixed and ready  
**Time to fix:** ~3 minutes

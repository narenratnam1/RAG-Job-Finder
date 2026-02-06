# ⚡ Pinecone Quick Setup

## 🎯 3-Step Production Setup

### Step 1: Get Pinecone API Key (2 minutes)

1. Go to https://www.pinecone.io/
2. Sign up (free tier available)
3. Create a project
4. Copy your API key from dashboard

---

### Step 2: Update .env (30 seconds)

Add these two lines to your `.env` file:

```env
PINECONE_API_KEY=pc-your-actual-key-here
PINECONE_INDEX_NAME=resume-index
```

**Important:** Replace `pc-your-actual-key-here` with your real Pinecone API key!

---

### Step 3: Install & Restart (1 minute)

```bash
# Install new dependencies
pip install pinecone-client langchain-pinecone

# Restart backend
# Press Ctrl+C in terminal 4
python start.py
```

**Look for:**
```
✓ VectorService initialized with Pinecone (index: resume-index)
```

✅ **Done!** You're now using production Pinecone!

---

## 🧪 Quick Test

1. Go to `http://localhost:3000`
2. Upload a resume
3. Search for candidates
4. Check Pinecone dashboard: https://app.pinecone.io/

---

## 🔄 Switch Back to ChromaDB

**To use local ChromaDB again:**

1. Remove or comment out in `.env`:
   ```env
   # PINECONE_API_KEY=...
   ```

2. Restart backend

You'll see:
```
✓ VectorService initialized with ChromaDB (local)
```

---

## 📖 Full Documentation

See `PINECONE_MIGRATION.md` for:
- Detailed setup
- Migration guide
- Troubleshooting
- Cost information

---

## ✅ Benefits of Pinecone

✅ **Cloud-hosted** - No local storage needed  
✅ **Scalable** - Handles millions of vectors  
✅ **Fast** - Distributed, low-latency  
✅ **Reliable** - Production-grade infrastructure  
✅ **Free tier** - Great for getting started  

---

**Status:** ✅ Ready in 3 minutes!  
**Cost:** Free tier available  
**Effort:** Minimal (2 env variables + 1 command)

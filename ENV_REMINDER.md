# 🔔 ENVIRONMENT VARIABLE REMINDER

## ⚠️ Action Required for Production

To use **Pinecone** in production, you need to add these variables to your `.env` file:

---

## 📝 Add to .env File

Open your `.env` file and add:

```env
# Pinecone Configuration (Production Vector Database)
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=resume-index
```

---

## 🔑 How to Get Your API Key

### Step 1: Sign Up
Go to: https://www.pinecone.io/

### Step 2: Create Project
- Create a new project in the dashboard
- Free tier available (no credit card needed)

### Step 3: Get API Key
- Click on "API Keys" in the dashboard
- Copy your API key
- It looks like: `pc-abc123xyz...`

### Step 4: Update .env
Replace `your_pinecone_api_key_here` with your actual key:

```env
PINECONE_API_KEY=pc-abc123xyz...
PINECONE_INDEX_NAME=resume-index
```

---

## 🔄 Then Restart Backend

```bash
# Press Ctrl+C to stop
python start.py
```

You should see:
```
✓ VectorService initialized with Pinecone (index: resume-index)
```

✅ **Done!**

---

## 🧪 For Development (No Action Needed)

**If you DON'T add the Pinecone key:**
- App uses ChromaDB (local)
- Everything still works
- No external dependencies

This is perfect for local development!

---

## 📊 Quick Comparison

| Mode | Env Vars | Backend | Best For |
|------|----------|---------|----------|
| **Local** | None added | ChromaDB | Development |
| **Production** | + Pinecone vars | Pinecone | Deployment |

---

## 🔒 Security Note

**DO:**
- ✅ Store key in `.env` file
- ✅ Keep `.env` in `.gitignore`
- ✅ Never commit keys to git

**DON'T:**
- ❌ Hard-code keys in source
- ❌ Share keys publicly
- ❌ Commit `.env` to repository

---

## 📖 More Info

See these guides:
- `PINECONE_QUICK_SETUP.md` - 3-minute setup
- `PINECONE_MIGRATION.md` - Complete guide
- `MIGRATION_COMPLETE.md` - Full overview

---

**Status:** ✅ Code ready, waiting for your Pinecone key  
**Action:** Add variables to `.env` when ready for production  
**Urgency:** Optional (local dev works without it)

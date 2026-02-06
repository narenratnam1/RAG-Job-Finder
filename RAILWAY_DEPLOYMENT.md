# 🚂 Railway Deployment Guide

## ✅ Files Created

- **`Procfile`** - Tells Railway how to start your app
- **`runtime.txt`** - Specifies Python version (3.11.6)
- **`requirements.txt`** - Already exists with all dependencies ✅

---

## 🚀 Deploy to Railway

### Step 1: Push to GitHub

```bash
git add Procfile runtime.txt
git commit -m "Add Railway deployment files"
git push origin main
```

### Step 2: Create Railway Project

1. Go to https://railway.app/
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository: `RAG and MCP Project`
5. Railway will auto-detect the `Procfile` and deploy

### Step 3: Set Environment Variables

In Railway dashboard, go to **Variables** tab and add:

```env
# OpenAI API Key (for embeddings)
OPENAI_API_KEY=sk-proj-...

# Pinecone Configuration (for vector storage)
PINECONE_API_KEY=pcsk_...
PINECONE_INDEX_NAME=resume-index
```

**Important:** Do NOT commit `.env` file to git (it's already in `.gitignore`)

### Step 4: Configure Port

Railway automatically provides the `$PORT` environment variable. Your `Procfile` already handles this:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Step 5: Deploy

Railway will automatically:
1. Install Python 3.11.6 (from `runtime.txt`)
2. Install dependencies (from `requirements.txt`)
3. Run the command in `Procfile`
4. Assign a public URL (e.g., `https://your-app.up.railway.app`)

---

## 📦 What Railway Will Install

From `requirements.txt`:

### Core Framework:
- ✅ `fastapi>=0.109.0`
- ✅ `uvicorn[standard]>=0.27.0`

### Vector Database:
- ✅ `pinecone>=5.0.0`
- ✅ `langchain-pinecone>=0.1.0`
- ✅ `chromadb>=0.4.22` (fallback)

### AI/Embeddings:
- ✅ `langchain-openai>=0.0.5`
- ✅ `sentence-transformers>=2.2.0`
- ✅ `langchain-huggingface>=0.0.1`

### PDF Processing:
- ✅ `pypdf>=4.0.0`
- ✅ `fpdf2>=2.7.0`

### File Upload:
- ✅ `python-multipart>=0.0.7`

### Other:
- ✅ `python-dotenv>=1.0.0`
- ✅ `pydantic>=2.5.0`

---

## 🔧 Railway-Specific Configuration

### Build Command:
None needed (Railway auto-installs from `requirements.txt`)

### Start Command:
Defined in `Procfile`:
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Health Check:
Your app already has a health endpoint at `/health`

Railway will hit this to verify deployment.

---

## 🌐 Static Files

Your app serves static files from `/static/resumes`.

**Important:** Railway provides ephemeral storage. Uploaded files will be lost on restart.

### Solution Options:

#### Option 1: Use Pinecone Only (Recommended)
- Store all resume data in Pinecone (already implemented ✅)
- Don't rely on local file storage
- Update code to fetch resume content from Pinecone metadata

#### Option 2: Add Cloud Storage
Add to `requirements.txt`:
```
boto3>=1.34.0  # For AWS S3
```

Update upload logic to save PDFs to S3 instead of local `uploads/` folder.

#### Option 3: Railway Volume (Paid)
- Mount a persistent volume in Railway
- Files persist across deployments
- Costs extra

---

## 🔍 Verify Deployment

### Step 1: Check Logs

In Railway dashboard → **Deployments** → Click latest deployment → **View Logs**

Should see:
```
✓ VectorService initialized with Pinecone
  Using OpenAI embeddings (text-embedding-3-small, 1536d)
✓ Mounted static files: /static/resumes
INFO:     Uvicorn running on http://0.0.0.0:$PORT
```

### Step 2: Test Health Endpoint

```bash
curl https://your-app.up.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "vector_store": "operational"
}
```

### Step 3: Test Frontend

Update your Next.js frontend API URL:

`frontend/src/services/api.js`:
```javascript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://your-app.up.railway.app';
```

---

## ⚙️ Environment Variables Required

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | For client-side embeddings |
| `PINECONE_API_KEY` | ✅ Yes | For vector storage |
| `PINECONE_INDEX_NAME` | Optional | Default: `resume-index` |
| `PORT` | Auto | Provided by Railway |

---

## 🚨 Common Issues

### Issue 1: "No module named 'app'"
**Cause:** Railway running from wrong directory

**Fix:** Ensure `Procfile` uses `app.main:app` (not `main:app`)

### Issue 2: "Port already in use"
**Cause:** Not using `$PORT` variable

**Fix:** Verified ✅ - `Procfile` already uses `$PORT`

### Issue 3: "OPENAI_API_KEY required"
**Cause:** Environment variable not set

**Fix:** Add in Railway dashboard → Variables

### Issue 4: Static files not loading
**Cause:** Ephemeral storage on Railway

**Fix:** Use cloud storage (S3, Cloudflare R2) or Railway volume

---

## 📊 Expected Behavior

### Successful Deployment:

```
Railway Build:
  Installing Python 3.11.6
  Installing dependencies from requirements.txt
  Build complete!

Railway Start:
  ✓ VectorService initialized with Pinecone
  ✓ Mounted static files
  INFO: Application startup complete
  INFO: Uvicorn running on 0.0.0.0:3000
```

### Health Check:
```bash
GET /health → 200 OK
{
  "status": "healthy",
  "vector_store": "operational"
}
```

---

## 💰 Railway Costs

### Free Tier:
- $5 credit/month
- 500 hours execution time
- Good for testing

### Pro Plan ($20/month):
- Unlimited execution time
- Better performance
- Custom domains

### Estimated Usage:
- Small RAG app: ~$10-15/month
- Add storage volume: +$5-10/month

---

## 🔒 Security Checklist

- [x] `.env` in `.gitignore` ✅
- [x] Environment variables in Railway (not in code) ✅
- [x] API keys not committed to git ✅
- [x] CORS configured for production domain (update `app/main.py` if needed)

---

## 🎯 Next Steps

1. **Commit files:**
   ```bash
   git add Procfile runtime.txt RAILWAY_DEPLOYMENT.md
   git commit -m "Add Railway deployment configuration"
   git push origin main
   ```

2. **Deploy on Railway:**
   - Connect GitHub repo
   - Add environment variables
   - Deploy!

3. **Update Frontend:**
   - Deploy frontend to Vercel/Netlify
   - Set `NEXT_PUBLIC_API_URL` to Railway URL

4. **Test End-to-End:**
   - Upload resume via frontend
   - Search for candidates
   - Verify Pinecone dashboard shows vectors

---

## 📚 Railway Documentation

- Dashboard: https://railway.app/dashboard
- Docs: https://docs.railway.app/
- Support: https://discord.gg/railway

---

## ✅ Pre-Deployment Checklist

- [x] `Procfile` created ✅
- [x] `runtime.txt` created ✅
- [x] `requirements.txt` verified ✅
- [x] All dependencies listed ✅
- [ ] Committed to git (you need to do this)
- [ ] Pushed to GitHub (you need to do this)
- [ ] Railway project created (you need to do this)
- [ ] Environment variables set (you need to do this)
- [ ] Deployed and tested (you need to do this)

---

**Status:** ✅ **READY FOR DEPLOYMENT**

**Next Action:** Commit files → Push to GitHub → Deploy on Railway

**ETA:** ~10 minutes

---

_Last updated: February 5, 2026_

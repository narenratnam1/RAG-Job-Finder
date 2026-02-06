# ✅ Railway Deployment Checklist

## 📦 Files Created

- ✅ `Procfile` - Start command for Railway
- ✅ `runtime.txt` - Python 3.11.6 version specification
- ✅ `.railwayignore` - Exclude unnecessary files from deployment
- ✅ `RAILWAY_DEPLOYMENT.md` - Complete deployment guide

## 🎯 Quick Deploy (5 Steps)

### 1. Commit Files (2 minutes)

```bash
git add Procfile runtime.txt .railwayignore RAILWAY_DEPLOYMENT.md DEPLOYMENT_CHECKLIST.md
git commit -m "Add Railway deployment configuration"
git push origin main
```

### 2. Create Railway Project (1 minute)

1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select your repo: `RAG and MCP Project`
4. Click "Deploy Now"

### 3. Set Environment Variables (1 minute)

In Railway dashboard → **Variables** tab:

```env
OPENAI_API_KEY=<copy from your .env file>

PINECONE_API_KEY=<copy from your .env file>

PINECONE_INDEX_NAME=resume-index
```

**⚠️ IMPORTANT:** Copy these values from your `.env` file (which is NOT committed to git)

### 4. Wait for Deployment (2-3 minutes)

Railway will:
- Install Python 3.11.6
- Install all packages from `requirements.txt`
- Start app with `Procfile` command
- Assign a public URL

### 5. Test Deployment (1 minute)

Click the generated URL (e.g., `https://your-app.up.railway.app`)

Test health endpoint:
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

---

## 🔍 Verify Everything Works

### ✅ Checklist:

- [ ] Railway build succeeded (check **Deployments** tab)
- [ ] No errors in logs (check **Logs** tab)
- [ ] Health endpoint returns 200 OK
- [ ] Can upload a resume via API
- [ ] Can search candidates via API
- [ ] Pinecone dashboard shows vectors

---

## 📊 Expected Logs

### Good Deployment Logs:

```
[Build]
Installing Python 3.11.6
Installing dependencies...
  fastapi>=0.109.0
  uvicorn[standard]>=0.27.0
  pinecone>=5.0.0
  langchain-openai>=0.0.5
  [... more packages ...]
Build complete!

[Start]
🔍 DEBUG: PINECONE_API_KEY=SET
🔍 DEBUG: PINECONE_AVAILABLE=True
✓ VectorService initialized with Pinecone (index: resume-index)
  Using OpenAI embeddings (text-embedding-3-small, 1536d)
  Index stats: 0 vectors
✓ Mounted static files: /static/resumes
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:3000 (Press CTRL+C to quit)
```

### Bad Logs (Common Errors):

❌ **"No module named 'app'"**
- Fix: Ensure `Procfile` uses `app.main:app`

❌ **"OPENAI_API_KEY required"**
- Fix: Add environment variable in Railway dashboard

❌ **"Index 'resume-index' does not exist"**
- Fix: Will auto-create on first use (or create in Pinecone dashboard)

---

## 🌐 Update Frontend

After Railway deployment, update your frontend to point to the new API:

### Option 1: Environment Variable (Recommended)

`frontend/.env.production`:
```env
NEXT_PUBLIC_API_URL=https://your-app.up.railway.app
```

### Option 2: Code Update

`frontend/src/services/api.js`:
```javascript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 
                     'https://your-app.up.railway.app';
```

---

## 🚨 Important Notes

### 1. Static Files (PDFs)

⚠️ **Railway uses ephemeral storage** - uploaded PDFs will be lost on restart.

**Solution:** Your vector data is already in Pinecone (persistent) ✅

**For PDF downloads:** Consider adding cloud storage:
- AWS S3
- Cloudflare R2
- Railway Volume (paid)

### 2. ChromaDB Fallback

Your code has a fallback to local ChromaDB if Pinecone fails.

⚠️ **On Railway:** Local `chroma_db/` folder will be reset on restart.

**Solution:** Ensure Pinecone credentials are set correctly so fallback never triggers.

### 3. CORS Configuration

If your frontend is on a different domain, update CORS in `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local dev
        "https://your-frontend.vercel.app"  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 💰 Cost Estimate

### Railway Free Tier:
- $5 credit/month
- ~500 execution hours
- Good for testing

### Railway Pro ($20/month):
- Unlimited execution hours
- Priority support
- Custom domains

### This App Estimate:
- **Basic usage:** ~$10-15/month
- **With storage volume:** +$5-10/month
- **Total:** ~$20-25/month

### Other Costs:
- **Pinecone Free Tier:** Free (1 index, 1GB)
- **OpenAI Embeddings:** ~$0.50 per 1000 resumes (very cheap)

---

## 🔧 Troubleshooting

### Build Fails

**Check:**
1. Python version in `runtime.txt` (3.11.6)
2. All packages in `requirements.txt` are valid
3. No syntax errors in Python files

### Start Fails

**Check:**
1. Environment variables set correctly
2. `Procfile` command is correct
3. Port is `$PORT` (not hardcoded)

### App Crashes

**Check Railway logs:**
```
Dashboard → Deployments → Latest → Logs
```

Look for:
- Import errors
- Missing environment variables
- Pinecone connection errors

---

## 📚 Useful Railway Commands

### View Logs:
```bash
railway logs
```

### Restart Service:
```bash
railway restart
```

### Open Dashboard:
```bash
railway open
```

### Deploy from CLI:
```bash
railway up
```

---

## ✅ Final Pre-Commit Checklist

- [x] `Procfile` created ✅
- [x] `runtime.txt` created ✅
- [x] `.railwayignore` created ✅
- [x] `requirements.txt` verified (all packages present) ✅
- [x] `.env` in `.gitignore` (not committed) ✅
- [x] Documentation created ✅
- [ ] **Commit files** ← YOU ARE HERE
- [ ] **Push to GitHub**
- [ ] **Create Railway project**
- [ ] **Set environment variables**
- [ ] **Test deployment**

---

## 🎯 Ready to Deploy!

Run these commands now:

```bash
# 1. Stage deployment files
git add Procfile runtime.txt .railwayignore RAILWAY_DEPLOYMENT.md DEPLOYMENT_CHECKLIST.md

# 2. Commit
git commit -m "Add Railway deployment configuration

- Add Procfile with uvicorn start command
- Add runtime.txt for Python 3.11.6
- Add .railwayignore to exclude dev files
- Add deployment documentation"

# 3. Push
git push origin main

# 4. Go to Railway
# https://railway.app/new
```

---

**Status:** ✅ **READY TO COMMIT & DEPLOY**

**Time to Deploy:** ~10 minutes total

---

_Your API keys are ready, files are created, just commit and deploy!_

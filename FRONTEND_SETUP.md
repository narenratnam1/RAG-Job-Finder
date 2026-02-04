# 🚀 Complete Frontend + Backend Setup Guide

Step-by-step instructions to run the full Agentic RAG application with React frontend and FastAPI backend.

---

## 📋 Prerequisites

### Required Software
- **Python 3.8+** (for backend)
- **Node.js 16+** and **npm** (for frontend)
- **Git** (optional)

### Check Your Versions
```bash
python3 --version  # Should be 3.8+
node --version     # Should be 16+
npm --version      # Should be 7+
```

---

## 🎯 Quick Start (2 Commands)

### Terminal 1: Start Backend
```bash
cd "/Users/narenratnam/Desktop/RAG and MCP Project"
source venv/bin/activate
python start.py
```

### Terminal 2: Start Frontend
```bash
cd "/Users/narenratnam/Desktop/RAG and MCP Project/frontend"
npm install
npm start
```

**Access the app:** http://localhost:3000

---

## 📦 Detailed Setup

### Part 1: Backend Setup

#### Step 1: Navigate to Project
```bash
cd "/Users/narenratnam/Desktop/RAG and MCP Project"
```

#### Step 2: Activate Virtual Environment
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

#### Step 3: Install Dependencies (if needed)
```bash
pip install -r requirements.txt
```

#### Step 4: Start Backend Server
```bash
python start.py
```

**Expected Output:**
```
✓ VectorService initialized with ./chroma_db
✓ MCP tools registered: 'consult_policy_db', 'screen_candidate', 'get_screener_instructions'
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Backend is ready at:** http://localhost:8000

---

### Part 2: Frontend Setup

#### Step 1: Open New Terminal
Keep the backend terminal running, open a **new terminal window**.

#### Step 2: Navigate to Frontend Directory
```bash
cd "/Users/narenratnam/Desktop/RAG and MCP Project/frontend"
```

#### Step 3: Install Dependencies
```bash
npm install
```

This will install:
- react
- react-dom
- axios
- react-scripts

**Wait:** Installation takes ~1-2 minutes

#### Step 4: Start Frontend Server
```bash
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view rag-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.x:3000
```

**Frontend will auto-open at:** http://localhost:3000

---

## ✅ Verification Checklist

### Backend Verification
```bash
# In backend terminal, you should see:
✓ VectorService initialized
✓ MCP tools registered
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Test manually:**
```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "vector_store": "operational",
  "mcp": "available"
}
```

### Frontend Verification
```bash
# In frontend terminal, you should see:
Compiled successfully!
webpack compiled successfully
```

**Browser should auto-open to:** http://localhost:3000

**You should see:**
- Header: "🤖 Agentic RAG API"
- Green status: "System Operational"
- Three tabs: Upload, Search, Screen

---

## 🎨 Using the Application

### Step 1: Upload a Document
1. Click "📤 Upload Documents" tab
2. Drag-and-drop a PDF or click "Choose File"
3. Click "Upload Document"
4. Wait for success message

### Step 2: Search Documents
1. Click "🔍 Search Documents" tab
2. Enter a question (e.g., "What are the requirements?")
3. Click "Search"
4. View results with relevance scores

### Step 3: Screen Candidate
1. Upload a resume PDF first (via Upload tab)
2. Click "👤 Screen Candidate" tab
3. Click "Load Sample" or paste job description
4. Click "Screen Candidate"
5. Review matched sections

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────┐
│         Browser (http://localhost:3000)     │
│              React Frontend                 │
└────────────────┬────────────────────────────┘
                 │ HTTP/REST API
                 ▼
┌─────────────────────────────────────────────┐
│      FastAPI Backend (:8000)                │
│  • /upload - Upload PDFs                    │
│  • /consult - Search documents              │
│  • /screen_candidate - Screen candidates    │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│         Vector Database (ChromaDB)          │
│         Embeddings (HuggingFace)            │
└─────────────────────────────────────────────┘
```

---

## 🔧 Development Workflow

### Full Restart (Backend + Frontend)

**Terminal 1 (Backend):**
```bash
cd "/Users/narenratnam/Desktop/RAG and MCP Project"
source venv/bin/activate
python start.py
```

**Terminal 2 (Frontend):**
```bash
cd "/Users/narenratnam/Desktop/RAG and MCP Project/frontend"
npm start
```

### Hot Reload
Both servers support hot reload:
- **Backend**: Uvicorn auto-reloads on Python file changes
- **Frontend**: React auto-recompiles on JS/CSS changes

---

## 📁 Project Structure

```
RAG and MCP Project/
├── app/
│   ├── main.py              # FastAPI application
│   ├── services/            # Business logic
│   └── ...
├── frontend/                # React application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API layer
│   │   └── App.js           # Main app
│   ├── public/
│   └── package.json
├── requirements.txt         # Python dependencies
├── start.py                 # Backend startup
└── README.md
```

---

## 🐛 Troubleshooting

### Issue 1: Backend Won't Start

**Error:** `ModuleNotFoundError` or import errors

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Try again
python start.py
```

---

### Issue 2: Frontend Won't Start

**Error:** `npm: command not found`

**Solution:**
```bash
# Install Node.js from https://nodejs.org/
# Or via Homebrew:
brew install node

# Verify installation
node --version
npm --version
```

---

### Issue 3: CORS Errors

**Error:** "Access to fetch at... has been blocked by CORS policy"

**Solution:**
FastAPI backend already has CORS enabled. If you still see errors:

1. Check backend is running on port 8000
2. Check frontend is accessing http://localhost:8000
3. Restart both servers

---

### Issue 4: Port Already in Use

**Backend (Port 8000):**
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill

# Or use different port in start.py:
uvicorn.run("app.main:app", port=8001)
```

**Frontend (Port 3000):**
```bash
# Use different port
PORT=3001 npm start

# Or kill process on port 3000
lsof -ti:3000 | xargs kill
```

---

### Issue 5: Upload Fails

**Error:** Upload returns 500 error

**Solution:**
1. Check backend terminal for errors
2. Verify PDF file is valid
3. Check ChromaDB initialized: Look for "✓ VectorService initialized"
4. Restart backend if needed

---

### Issue 6: Search Returns No Results

**Problem:** Always empty results

**Solution:**
1. Upload a document first
2. Wait for upload confirmation
3. Try a simpler query
4. Check backend logs

---

## 🚀 Production Deployment

### Backend (FastAPI)

**Option 1: Docker**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Option 2: Cloud Platform**
- AWS EC2 + Gunicorn
- Google Cloud Run
- Azure App Service
- Heroku

---

### Frontend (React)

**Build for Production:**
```bash
cd frontend
npm run build
```

**Deploy to:**
1. **Vercel** (Recommended)
   ```bash
   npm install -g vercel
   vercel
   ```

2. **Netlify**
   ```bash
   npm install -g netlify-cli
   netlify deploy
   ```

3. **AWS S3 + CloudFront**
4. **GitHub Pages**

**Update API URL:**
Create `frontend/.env.production`:
```env
REACT_APP_API_URL=https://your-backend-url.com
```

---

## 📊 Performance Tips

### Backend Optimization
- Use Gunicorn with multiple workers
- Enable response caching
- Optimize vector search parameters
- Use faster embedding models

### Frontend Optimization
- Enable lazy loading
- Implement search debouncing
- Add response caching
- Optimize bundle size with code splitting

---

## 🔒 Security Considerations

### For Production:
1. **HTTPS**: Use SSL certificates
2. **Authentication**: Add JWT tokens
3. **Rate Limiting**: Prevent abuse
4. **Input Validation**: Sanitize uploads
5. **CORS**: Restrict to specific origins
6. **Environment Variables**: Hide API keys

---

## 📚 Additional Resources

### Backend Documentation
- FastAPI: https://fastapi.tiangolo.com/
- ChromaDB: https://docs.trychroma.com/
- LangChain: https://python.langchain.com/

### Frontend Documentation
- React: https://react.dev/
- Create React App: https://create-react-app.dev/
- Axios: https://axios-http.com/

---

## ✨ Feature Roadmap

**Phase 1 (Current):**
- ✅ Document upload
- ✅ Semantic search
- ✅ Candidate screening

**Phase 2 (Future):**
- [ ] Document management (list/delete)
- [ ] Search history
- [ ] Batch uploads
- [ ] Export results
- [ ] Dark mode

**Phase 3 (Advanced):**
- [ ] Real-time collaboration
- [ ] Advanced filters
- [ ] Analytics dashboard
- [ ] Multi-language support

---

## 🎉 Success!

If you see:
- ✅ Backend running at http://localhost:8000
- ✅ Frontend running at http://localhost:3000
- ✅ Green "System Operational" status
- ✅ All three tabs working

**You're all set! Start uploading and searching documents!**

---

## 💬 Support

**Common Questions:**

**Q: Can I use a different port?**
A: Yes, update PORT in `start.py` and `api.js`

**Q: How do I reset the database?**
A: Delete `./chroma_db` folder and restart

**Q: Can I upload non-PDF files?**
A: Currently only PDF. Add support in `upload_pdf()` endpoint

**Q: How many documents can I upload?**
A: No hard limit, but performance may degrade >10K documents

---

**Last Updated:** Just now  
**Status:** ✅ Complete Setup Guide  
**Next Step:** Run the commands and start building!

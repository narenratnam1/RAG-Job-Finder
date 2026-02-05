# 🎯 TalentHub - Complete Project Guide

## Overview

TalentHub is a professional recruiting dashboard that combines FastAPI backend with Next.js frontend to provide AI-powered resume screening and tailoring capabilities.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (Next.js)                       │
│                   http://localhost:3000                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Sidebar Navigation                                  │   │
│  │  ├─ Candidate Upload (PDF Upload)                   │   │
│  │  ├─ Resume Screener (AI Analysis)                   │   │
│  │  └─ AI Resume Tailor (PDF Generation)               │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │ Axios HTTP Requests
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                         │
│                   http://localhost:8000                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  API Endpoints:                                      │   │
│  │  ├─ POST /upload (PDF Processing)                   │   │
│  │  ├─ POST /screen_candidate (RAG Search)             │   │
│  │  └─ POST /tailor_resume (AI + PDF Gen)              │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Services:                                           │   │
│  │  ├─ Vector Store (ChromaDB)                         │   │
│  │  ├─ PDF Generator (fpdf2)                           │   │
│  │  ├─ Resume Tailor (OpenAI GPT-3.5)                  │   │
│  │  └─ Document Ingestor (PyPDF)                       │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start (2 Minutes)

### Option 1: Start Everything at Once
```bash
./start_both.sh
```
This starts both backend and frontend automatically!

### Option 2: Start Separately

**Terminal 1 - Backend:**
```bash
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install  # First time only
npm run dev
```

## 📦 What's Included

### Backend Features
- ✅ PDF document upload and processing
- ✅ Vector database (ChromaDB) for semantic search
- ✅ AI-powered resume screening
- ✅ AI-powered resume tailoring
- ✅ PDF generation from text
- ✅ CORS configured for frontend
- ✅ Interactive API docs at /docs

### Frontend Features
- ✅ Modern Next.js 14 with App Router
- ✅ Tailwind CSS styling
- ✅ Responsive sidebar navigation
- ✅ Drag-and-drop file upload
- ✅ Real-time toast notifications
- ✅ Professional "Corporate Clean" design
- ✅ Loading states and error handling
- ✅ Automatic PDF downloads

## 🎨 UI Preview

### Dashboard Layout
```
┌─────────────────────────────────────────────────────────────┐
│ ┌─────────┐ ┌──────────────────────────────────────────┐   │
│ │         │ │                                          │   │
│ │ Talent  │ │         Page Content Area               │   │
│ │  Hub    │ │                                          │   │
│ │         │ │  • Upload Page: Drag & Drop Zone        │   │
│ │ ─────── │ │  • Screener: Job Desc + Results         │   │
│ │         │ │  • Tailor: Input Fields + Generate      │   │
│ │ Upload  │ │                                          │   │
│ │ Screener│ │                                          │   │
│ │ Tailor  │ │                                          │   │
│ │         │ │                                          │   │
│ │         │ │                                          │   │
│ │ [API ●] │ │                                          │   │
│ └─────────┘ └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
  Sidebar       Main Content (Changes based on navigation)
```

### Color Scheme
- **Primary**: Corporate Blue (#3b82f6)
- **Sidebar**: Dark Blue Gradient
- **Background**: Light Gray (#f8fafc)
- **Text**: Slate (#0f172a)
- **Success**: Green, Error: Red, Warning: Yellow

## 🔌 API Endpoints

| Method | Endpoint | Purpose | Request | Response |
|--------|----------|---------|---------|----------|
| POST | `/upload` | Upload resume PDF | FormData | JSON (status, chunks) |
| POST | `/screen_candidate` | Screen candidate | Query param: job_description | JSON (screening result) |
| POST | `/tailor_resume` | Generate tailored PDF | JSON: job_description, current_resume_text | PDF file |
| GET | `/health` | Health check | None | JSON (status) |
| GET | `/docs` | API documentation | None | Interactive Swagger UI |

## 📂 File Structure

```
RAG and MCP Project/
├── app/                                    # Backend
│   ├── main.py                            # FastAPI app with endpoints
│   ├── core/
│   │   └── config.py                      # Configuration
│   └── services/
│       ├── vector_store.py                # ChromaDB integration
│       ├── ingestor.py                    # PDF processing
│       ├── pdf_generator.py               # PDF creation (NEW)
│       └── resume_tailor.py               # AI tailoring (NEW)
│
├── frontend/                              # Frontend
│   ├── app/
│   │   ├── layout.js                     # Root layout + sidebar
│   │   ├── page.js                       # Home (Upload)
│   │   ├── globals.css                   # Global styles
│   │   ├── screener/
│   │   │   └── page.js                   # Screener page
│   │   └── tailor/
│   │       └── page.js                   # Tailor page
│   ├── components/
│   │   └── Sidebar.js                    # Navigation
│   ├── lib/
│   │   └── api.js                        # API utilities
│   ├── package.json                      # Dependencies
│   ├── tailwind.config.js                # Tailwind config
│   └── next.config.js                    # Next.js config
│
├── .env                                   # Environment variables
├── requirements.txt                       # Python dependencies
├── start_both.sh                         # Start everything (NEW)
├── start_frontend.sh                     # Start frontend only (NEW)
└── COMPLETE_GUIDE.md                     # This file
```

## 🔧 Configuration

### Backend (.env)
```env
# Required for AI Resume Tailor
OPENAI_API_KEY=sk-proj-your-key-here

# ChromaDB Settings
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
CHROMA_COLLECTION_NAME=rag_documents

# Model Settings
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL_NAME=gpt-3.5-turbo
```

### Frontend (lib/api.js)
```javascript
const API_BASE_URL = 'http://localhost:8000'
```

## 🎯 Usage Workflows

### Workflow 1: Screen a Candidate
1. Go to "Candidate Upload" page
2. Upload candidate's resume PDF
3. Navigate to "Resume Screener"
4. Paste the job description
5. Click "Screen Candidate"
6. Review the AI-generated analysis

### Workflow 2: Tailor a Resume
1. Navigate to "AI Resume Tailor"
2. Paste the target job description
3. Paste the current resume text
4. Click "Generate Tailored Resume PDF"
5. PDF automatically downloads
6. Open and review the tailored resume

### Workflow 3: Bulk Processing
1. Upload multiple resumes (one at a time)
2. Use screener to evaluate each against same job
3. Compare results to find best matches
4. Tailor top candidate's resume for submission

## 🧪 Testing

### Quick Test
1. Start both services: `./start_both.sh`
2. Open http://localhost:3000
3. Upload a sample PDF resume
4. Test the screener with a job description
5. Test the tailor with sample text

### API Test (Backend Only)
```bash
# Health check
curl http://localhost:8000/health

# Upload test
curl -X POST http://localhost:8000/upload \
  -F "file=@sample_resume.pdf"

# View API docs
open http://localhost:8000/docs
```

## 🐛 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

**2. Module Not Found (Backend)**
```bash
pip install -r requirements.txt
```

**3. Module Not Found (Frontend)**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**4. CORS Error**
- Already configured in `app/main.py`
- Clear browser cache
- Hard reload (Cmd+Shift+R)

**5. AI Tailor Returns Demo Mode**
- Add OpenAI API key to `.env`
- Restart backend
- Check key is valid

**6. PDF Upload Fails**
- Verify file is PDF format
- Check file size < 10MB
- Review backend logs for errors

## 💰 Cost Considerations

### OpenAI API Usage
- **Model**: GPT-3.5-turbo
- **Cost**: ~$0.001-0.002 per resume tailoring
- **Free Tier**: $5 credit for new accounts
- **Monitor**: https://platform.openai.com/usage

### Infrastructure
- **Local Development**: Free
- **ChromaDB**: Free (local)
- **Deployment**: 
  - Vercel (Frontend): Free tier available
  - Render (Backend): Free tier available

## 🚢 Deployment

### Frontend (Vercel)
```bash
cd frontend
vercel deploy
```

### Backend (Render/AWS/DigitalOcean)
1. Push code to GitHub
2. Connect to deployment platform
3. Set environment variables
4. Update frontend API_BASE_URL

## 🔐 Security Checklist

- [ ] Never commit `.env` with real keys
- [ ] Use environment variables for all secrets
- [ ] Enable authentication in production
- [ ] Configure CORS for specific domains in production
- [ ] Use HTTPS in production
- [ ] Implement rate limiting
- [ ] Validate all file uploads
- [ ] Sanitize user inputs

## 📊 Performance

### Current Capabilities
- **Upload**: ~1-2 seconds per PDF
- **Screening**: ~2-3 seconds per query
- **Tailoring**: ~5-10 seconds (depends on OpenAI API)
- **PDF Generation**: <1 second

### Optimization Tips
- Use caching for repeated queries
- Implement batch processing
- Add Redis for session management
- Use CDN for frontend assets

## 🎓 Learning Resources

### Technologies Used
- **FastAPI**: https://fastapi.tiangolo.com/
- **Next.js**: https://nextjs.org/docs
- **Tailwind CSS**: https://tailwindcss.com/docs
- **ChromaDB**: https://docs.trychroma.com/
- **LangChain**: https://python.langchain.com/

## 🎉 What's Next?

### Potential Enhancements
1. User authentication and profiles
2. Save screening results to database
3. Batch resume processing
4. Email integration for sending tailored resumes
5. Analytics dashboard
6. Export screening results to CSV
7. ATS (Applicant Tracking System) integration
8. Resume templates selection
9. Multi-language support
10. Mobile app version

## 📞 Support

### Quick Links
- Backend API Docs: http://localhost:8000/docs
- Frontend Dev: http://localhost:3000
- OpenAI Dashboard: https://platform.openai.com/

### Debugging Steps
1. Check both services are running
2. Review terminal logs for errors
3. Check browser console (F12)
4. Verify `.env` configuration
5. Test API endpoints directly
6. Clear browser cache

---

**Made with ❤️ for Recruiters**

Ready to revolutionize your recruiting workflow! 🚀

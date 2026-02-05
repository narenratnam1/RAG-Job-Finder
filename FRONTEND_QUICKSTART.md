# TalentHub Dashboard - Quick Start Guide

## 🚀 Complete Setup & Launch

This guide will get both your FastAPI backend and Next.js frontend running.

## Prerequisites

- Python 3.8+
- Node.js 18+
- OpenAI API Key (for AI Resume Tailor feature)

## Step 1: Backend Setup

### Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Configure Environment Variables
1. The `.env` file has been created from `.env.example`
2. Add your OpenAI API key:
```bash
# Open .env and update this line:
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

### Start the Backend
```bash
python -m uvicorn app.main:app --reload
```

Backend will run at: **http://localhost:8000**

## Step 2: Frontend Setup

### Install Node Dependencies
```bash
cd frontend
npm install
```

### Start the Frontend
```bash
npm run dev
```

Frontend will run at: **http://localhost:3000**

## Step 3: Access the Dashboard

Open your browser to: **http://localhost:3000**

You should see the TalentHub dashboard with the sidebar navigation!

## 🎯 Features Overview

### 1. Candidate Upload (Home Page)
- **URL**: http://localhost:3000/
- **Purpose**: Upload candidate resume PDFs
- **How to use**:
  1. Drag and drop a PDF or click "Browse Files"
  2. Wait for processing to complete
  3. See success message with chunk count

### 2. Resume Screener
- **URL**: http://localhost:3000/screener
- **Purpose**: Compare resumes against job descriptions
- **How to use**:
  1. First, upload a resume on the home page
  2. Paste a job description in the text area
  3. Click "Screen Candidate"
  4. View the AI-powered comparison results

### 3. AI Resume Tailor
- **URL**: http://localhost:3000/tailor
- **Purpose**: Generate customized resumes for specific jobs
- **How to use**:
  1. Paste the target job description
  2. Paste the current resume text
  3. Click "Generate Tailored Resume PDF"
  4. PDF automatically downloads

## 🎨 Dashboard Features

✅ **Professional Sidebar Navigation**
- Clean, modern design
- Active page highlighting
- Easy navigation between features

✅ **Responsive Design**
- Works on desktop, tablet, and mobile
- Tailwind CSS styling
- Corporate blue color scheme

✅ **Real-time Feedback**
- Toast notifications for all actions
- Loading states during processing
- Error handling and user guidance

✅ **API Integration**
- Seamless connection to FastAPI backend
- File upload support
- PDF download handling

## 📁 Project Structure

```
RAG and MCP Project/
├── app/                          # FastAPI Backend
│   ├── main.py                   # Main API with all endpoints
│   └── services/
│       ├── pdf_generator.py      # PDF generation service
│       ├── resume_tailor.py      # AI tailoring logic
│       └── vector_store.py       # ChromaDB integration
├── frontend/                     # Next.js Frontend
│   ├── app/
│   │   ├── page.js              # Home (Upload)
│   │   ├── screener/page.js     # Resume Screener
│   │   └── tailor/page.js       # AI Tailor
│   ├── components/
│   │   └── Sidebar.js           # Navigation sidebar
│   └── lib/
│       └── api.js               # API utilities
├── requirements.txt              # Python dependencies
└── .env                         # Environment configuration
```

## 🔧 Troubleshooting

### Backend won't start
- Check if port 8000 is already in use
- Verify all Python dependencies are installed: `pip install -r requirements.txt`
- Check for errors in the terminal

### Frontend won't start
- Check if port 3000 is already in use
- Delete `node_modules` and `package-lock.json`, then run `npm install` again
- Verify Node.js version: `node --version` (should be 18+)

### CORS errors in browser
- Backend already has CORS configured for all origins
- Clear browser cache and hard reload (Cmd+Shift+R or Ctrl+Shift+R)

### Upload fails
- Ensure backend is running on port 8000
- Check file is a valid PDF
- Verify ChromaDB is working (check backend logs)

### Resume Tailor returns demo mode
- Add your OpenAI API key to `.env`
- Restart the backend after updating `.env`
- Verify the key is valid at https://platform.openai.com/api-keys

### PDF download doesn't work
- Check browser settings allow downloads
- Verify OpenAI API key is configured
- Check backend terminal for errors

## 🧪 Testing the System

### Test Flow:
1. **Upload a Resume**
   - Go to http://localhost:3000/
   - Upload a sample PDF resume
   - Verify success message

2. **Screen a Candidate**
   - Go to http://localhost:3000/screener
   - Paste a job description
   - Click "Screen Candidate"
   - Review the results

3. **Tailor a Resume**
   - Go to http://localhost:3000/tailor
   - Paste job description and resume text
   - Click "Generate"
   - Verify PDF downloads

## 💡 Pro Tips

- **Keep both terminals open** - one for backend, one for frontend
- **Watch the backend logs** - helpful for debugging API issues
- **Use the interactive API docs** - http://localhost:8000/docs
- **Check browser console** - for frontend debugging

## 🎨 UI/UX Features

- **Drag-and-drop** file uploads
- **Loading animations** for all async operations
- **Toast notifications** for user feedback
- **Responsive layouts** for all screen sizes
- **Professional color scheme** with blues and grays
- **Icon-based navigation** with Lucide React icons

## 🔐 Security Notes

- Never commit your `.env` file with real API keys
- The `.gitignore` already excludes `.env`
- Keep your OpenAI API key secure
- Backend CORS is set to allow all origins (fine for local dev)

## 📊 API Endpoints

Backend provides these endpoints:

- `GET /` - API info
- `GET /health` - Health check
- `POST /upload` - Upload PDF resumes
- `POST /screen_candidate` - Screen candidates
- `POST /tailor_resume` - Generate tailored resumes
- `GET /docs` - Interactive API documentation

## 🚀 Next Steps

1. Customize the branding in `Sidebar.js`
2. Add more features to the dashboard
3. Integrate with your existing HR systems
4. Deploy to production (Vercel for frontend, Render/AWS for backend)

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review backend logs for API errors
3. Check browser console for frontend errors
4. Verify all dependencies are installed correctly

---

**Happy Recruiting! 🎉**

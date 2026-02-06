# 🚀 Quick Start: Candidate Search & Rank

## What's New?

A new **"Candidate Search"** feature that uses AI to find and rank the best candidates for any job opening!

---

## ✅ Files Changed

### Backend
- ✅ `app/main.py` - New `/search_candidates` endpoint added

### Frontend
- ✅ `frontend/lib/api.js` - New `searchCandidates()` function
- ✅ `frontend/app/search/page.js` - New search page (NEW FILE)
- ✅ `frontend/components/Sidebar.js` - Added "Candidate Search" link

---

## 🎯 How to Use

### 1. Start the Backend
```bash
cd /Users/narenratnam/Desktop/RAG\ and\ MCP\ Project
python start.py
```

### 2. Start the Frontend (in a new terminal)
```bash
cd frontend
npm run dev
```

### 3. Open the App
Navigate to: `http://localhost:3000`

### 4. Try It Out!

1. **Upload some resumes first** (if you haven't already):
   - Click "Candidate Upload"
   - Upload 5-10 PDF resumes

2. **Go to "Candidate Search"** (new sidebar link)

3. **Paste a job description**, for example:
   ```
   Senior Full Stack Developer
   
   Requirements:
   - React, Node.js, Python
   - 5+ years of experience
   - Strong problem-solving skills
   
   Nice to have:
   - AWS, Docker, PostgreSQL
   - Team leadership experience
   ```

4. **Click "Find Top Talent"**

5. **See the results!**
   - Top 7 candidates ranked by AI
   - Score for each (0-100)
   - Detailed reasoning
   - Color-coded badges

---

## 🎨 UI Preview

The search page features:

- 🔍 **Large text area** for job descriptions
- ✨ **"Find Top Talent" button** with loading state
- 🏆 **Ranked candidate cards** with:
  - Rank badges (🥇 Gold, 🥈 Silver, 🥉 Bronze)
  - Score badges (color-coded by performance)
  - Detailed reasoning
  - Match quality indicators
- 📊 **Info panels** explaining how it works

---

## 🤖 How It Works

1. **Vector Search:** Finds top 10 semantically similar resumes
2. **AI Reranking:** GPT-3.5 evaluates and ranks them
3. **Top 7 Results:** Best candidates with scores and reasoning

---

## ⚙️ Requirements

- ✅ Backend running (`python start.py`)
- ✅ Frontend running (`npm run dev` in `/frontend`)
- ✅ `OPENAI_API_KEY` set in `.env` (or it runs in demo mode)
- ✅ At least a few resumes uploaded to the database

---

## 🎉 That's It!

You now have a complete AI-powered candidate search engine integrated into your recruiting dashboard.

**Next Steps:**
1. Upload more resumes to improve search results
2. Try different job descriptions
3. Compare results with "Resume Screener" for deep analysis
4. Use "AI Resume Tailor" to help selected candidates

---

## 📖 Full Documentation

See `CANDIDATE_SEARCH_FEATURE.md` for complete technical details, API reference, and advanced usage.

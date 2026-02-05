# 🚀 START HERE - Frontend Launch Guide

## ✅ What's Ready

Your complete **TalentHub Recruiting Dashboard** is built and ready to launch!

## 🏃 Quick Start (Choose One)

### Option A: Start Everything (Recommended)
```bash
./start_both.sh
```
This single command starts both backend and frontend!

### Option B: Start Frontend Only
```bash
./start_frontend.sh
```
(Make sure backend is already running)

### Option C: Manual Start
```bash
# Terminal 1 - Backend
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm install  # First time only
npm run dev
```

## 📍 Access Your Dashboard

Once started, open your browser to:

### **http://localhost:3000**

You'll see a professional dashboard with:
- 🔵 Blue sidebar navigation
- 📤 Upload page (home)
- 🔍 Resume screener
- ✨ AI resume tailor

## 🎯 First-Time Setup

### 1. Install Frontend Dependencies (Required)
```bash
cd frontend
npm install
```
This installs React, Next.js, Tailwind CSS, and all dependencies.
**Wait time**: ~2-3 minutes depending on internet speed.

### 2. Verify Backend is Ready
```bash
# Check backend is running
curl http://localhost:8000/health
```
Should return: `{"status":"healthy",...}`

### 3. Optional: Add OpenAI API Key
For full AI Resume Tailor functionality:
```bash
# Edit .env file and add:
OPENAI_API_KEY=sk-proj-your-key-here
```
Then restart backend.

## 🧪 Test Your Dashboard

### Test 1: Upload a Resume
1. Go to http://localhost:3000/
2. Drag a PDF or click "Browse Files"
3. Should see success message ✅

### Test 2: Screen a Candidate
1. Click "Resume Screener" in sidebar
2. Paste a job description
3. Click "Screen Candidate"
4. Should see analysis results ✅

### Test 3: Tailor a Resume
1. Click "AI Resume Tailor" in sidebar
2. Paste job description and resume text
3. Click "Generate"
4. PDF should download automatically ✅

## 📱 What You'll See

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ┌──────────┐  ┌─────────────────────────────────┐    │
│  │ TalentHub│  │                                 │    │
│  │ Sidebar  │  │   Your Page Content Here        │    │
│  │          │  │   (Upload/Screener/Tailor)      │    │
│  │ Upload   │  │                                 │    │
│  │ Screener │  │   Beautiful, professional UI    │    │
│  │ Tailor   │  │   with blue and white colors    │    │
│  │          │  │                                 │    │
│  │ [API ●]  │  │                                 │    │
│  └──────────┘  └─────────────────────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 🎨 Features

✅ **Drag-and-drop** file uploads
✅ **Real-time** toast notifications  
✅ **Professional** sidebar navigation
✅ **Loading animations** for all actions
✅ **Responsive design** (works on all devices)
✅ **Corporate blue** color scheme
✅ **Error handling** with helpful messages
✅ **Automatic PDF** downloads

## 🔧 Troubleshooting

### "npm install" fails
```bash
# Delete and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Port 3000 already in use
```bash
# Kill the process
lsof -ti:3000 | xargs kill -9
# Then restart
npm run dev
```

### Can't connect to backend
1. Check backend is running: `curl http://localhost:8000/health`
2. Verify port 8000 is correct
3. Check no firewall blocking localhost

### PDF download doesn't work
1. Add OpenAI API key to `.env`
2. Restart backend
3. Try again

### CORS errors
- Already configured! ✅
- If you see errors, clear browser cache
- Hard reload: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

## 📚 Documentation

Detailed guides available:
- `FRONTEND_BUILD_SUMMARY.md` - What was built
- `FRONTEND_QUICKSTART.md` - Setup details
- `COMPLETE_GUIDE.md` - Full project guide
- `frontend/README.md` - Frontend-specific docs

## 🎉 You're Ready!

Everything is configured and ready to go. Just run:

```bash
./start_both.sh
```

Then open: **http://localhost:3000**

## 💡 Quick Tips

1. **Keep terminals visible** - easier to spot errors
2. **Check browser console** (F12) - for debugging
3. **Use toast notifications** - they show success/error
4. **Test API directly** - http://localhost:8000/docs
5. **Read the logs** - both frontend and backend

## 🚀 Next Steps

After launching:
1. ✅ Test file upload
2. ✅ Test resume screening  
3. ✅ Test resume tailoring
4. 🎨 Customize branding (optional)
5. 🚢 Deploy to production (when ready)

---

## 🎯 The Moment of Truth

Run this now:
```bash
cd "/Users/narenratnam/Desktop/RAG and MCP Project"
./start_both.sh
```

Then open: http://localhost:3000

**Enjoy your new recruiting dashboard!** 💼✨

---

**Need Help?**
- Check `COMPLETE_GUIDE.md` for troubleshooting
- Review backend logs in Terminal 1
- Review frontend logs in Terminal 2
- Check browser console (F12) for frontend errors

# 🧪 Quick Test Guide - Resume Tailor Upgrade

## ⚡ Quick Start

### 1. Restart Backend (Important!)
```bash
# Stop current backend (Ctrl+C if running)
# Then restart:
python -m uvicorn app.main:app --reload
```

**Why?** Backend code changed - needs restart to load new endpoints.

### 2. Frontend Should Auto-Reload
The frontend should automatically detect changes. If not:
```bash
cd frontend
npm run dev
```

### 3. Open in Browser
Navigate to: **http://localhost:3000/tailor**

---

## ✅ Test Workflow

### Step 1: Prepare Test Data

**Job Description (copy this):**
```
Senior Python Developer

We are seeking an experienced Python developer with expertise in:
- FastAPI and Django frameworks
- RESTful API development
- AWS cloud services
- Docker and containerization
- PostgreSQL and MongoDB
- Git version control

5+ years of experience required.
```

**Resume PDF:** Use any PDF resume you have, or create a simple one.

### Step 2: Upload and Generate

1. **Paste** the job description in the left text area
2. **Upload** your resume PDF on the right (drag or browse)
3. You should see a green checkmark when file is selected
4. Click **"Generate Preview"**
5. Wait 5-10 seconds for AI processing

### Step 3: Review Preview

You should see:
- A preview section appear below
- The tailored resume text displayed
- A green "Download PDF" button

### Step 4: Download PDF

1. Review the preview text
2. Click **"Download PDF"**
3. A file should download: `tailored_resume.pdf`
4. Open it to verify formatting

---

## 🎯 Expected Results

### With OpenAI API Key

**Preview Text Should:**
- Incorporate keywords from job description
- Maintain professional tone
- Keep resume structure
- Highlight relevant skills

**Example Output:**
```
JOHN DOE
SENIOR PYTHON DEVELOPER

Experienced Python Developer with 5+ years building scalable 
applications using FastAPI and Django frameworks...

TECHNICAL SKILLS
• Python, FastAPI, Django
• RESTful API Development
• AWS Cloud Services (EC2, S3, Lambda)
• Docker & Containerization
...
```

### Without OpenAI API Key (Demo Mode)

**Preview Text Shows:**
```
TAILORED RESUME (Demo Mode - Add OPENAI_API_KEY to enable AI)

ORIGINAL RESUME:
[Your resume content]

TARGETED FOR:
[Job description]

Note: This is a demo response...
```

**Action:** Add your OpenAI API key to `.env` and restart backend.

---

## 🐛 Common Issues & Fixes

### Issue 1: "Module not found: pdf_extractor"

**Cause:** Backend not restarted after code changes

**Fix:**
```bash
# Stop backend (Ctrl+C)
python -m uvicorn app.main:app --reload
```

### Issue 2: "Failed to tailor resume"

**Possible Causes:**
- Backend not running
- Invalid PDF file
- OpenAI API key missing/invalid

**Fixes:**
1. Check backend terminal for errors
2. Try a different PDF file
3. Verify `.env` has `OPENAI_API_KEY=sk-proj-...`

### Issue 3: File Upload Not Working

**Cause:** FormData not sent correctly

**Fix:**
1. Hard refresh browser (Cmd+Shift+R / Ctrl+Shift+R)
2. Check browser console (F12) for errors
3. Verify backend shows FormData in logs

### Issue 4: Preview Shows But "Download PDF" Fails

**Cause:** PDF generation endpoint issue

**Possible Fixes:**
1. Check backend terminal for errors
2. Verify `fpdf2` is installed: `pip install fpdf2`
3. Check browser console for network errors

### Issue 5: Drag-and-Drop Not Working

**Fix:**
- Use the "Browse Files" button instead
- Ensure file is PDF format
- Try clearing browser cache

---

## 📋 Testing Checklist

Complete these tests to verify everything works:

- [ ] **File Upload via Drag-and-Drop**
  - Drag PDF over upload zone
  - Zone should highlight blue
  - File should be accepted

- [ ] **File Upload via Browse Button**
  - Click "Browse Files"
  - Select PDF
  - File should show with checkmark

- [ ] **Remove File**
  - Upload a file
  - Click "Remove File" button
  - Should clear and show upload zone again

- [ ] **Generate Preview - Success**
  - Fill both inputs
  - Click "Generate Preview"
  - Should show loading animation
  - Preview section should appear

- [ ] **Generate Preview - Validation**
  - Try with only job description (button disabled)
  - Try with only file (button disabled)
  - Button should only enable when both provided

- [ ] **Download PDF**
  - Generate preview first
  - Click "Download PDF"
  - File should download
  - Open PDF and verify content

- [ ] **Error Handling**
  - Try uploading non-PDF file
  - Should show error toast
  - Try with very long job description
  - Should handle gracefully

- [ ] **UI/UX**
  - Check loading states
  - Verify toast notifications
  - Test responsive design (resize window)
  - Check all icons display correctly

---

## 🔍 Debug Mode

### Check Backend Logs

Look for these in backend terminal:

**Success:**
```
INFO: 127.0.0.1:xxxxx - "POST /tailor_resume HTTP/1.1" 200 OK
INFO: 127.0.0.1:xxxxx - "POST /generate_pdf HTTP/1.1" 200 OK
```

**Errors:**
```
ERROR: Exception in ASGI application
...detailed error message...
```

### Check Frontend Console

Open browser DevTools (F12), check Console tab:

**Success:**
```
✓ File selected: resume.pdf
✓ Preview generated successfully
✓ PDF downloaded successfully
```

**Errors:**
```
✗ Failed to tailor resume: [error message]
```

### Test API Directly

**Test Preview Endpoint:**
```bash
curl -X POST http://localhost:8000/tailor_resume \
  -F "job_description=Test job description" \
  -F "resume_file=@/path/to/resume.pdf"
```

**Test PDF Endpoint:**
```bash
curl -X POST http://localhost:8000/generate_pdf \
  -H "Content-Type: application/json" \
  -d '{"tailored_text":"Test content"}' \
  --output test.pdf
```

---

## 💡 Tips for Best Results

1. **Use Clear Job Descriptions**
   - Include specific skills and requirements
   - Mention technologies and tools
   - Add experience level needed

2. **Upload Quality Resumes**
   - Clean, well-formatted PDFs
   - Not too long (1-3 pages ideal)
   - Text-based, not scanned images

3. **Review Before Downloading**
   - Read through the preview
   - Check for any issues
   - Ensure keywords are included

4. **OpenAI API Key**
   - Use a valid key for best results
   - Monitor usage at platform.openai.com
   - Demo mode works but doesn't tailor

---

## ✅ Success Criteria

Your upgrade is working correctly if:

1. ✅ You can upload a PDF resume (not paste text)
2. ✅ Preview shows tailored content
3. ✅ Download button appears after preview
4. ✅ PDF downloads successfully
5. ✅ UI is responsive and user-friendly
6. ✅ Error handling works (wrong file type, etc.)
7. ✅ Loading states show during processing
8. ✅ Toast notifications provide feedback

---

## 🎉 All Working?

If all tests pass, you now have a professional, user-friendly Resume Tailor with:

- 📤 **PDF Upload** (no more copy/paste!)
- 👀 **Preview** (review before committing)
- ⬇️ **Separate Download** (when you're ready)
- 🎨 **Beautiful UI** (professional design)
- ⚡ **Fast & Reliable** (proper error handling)

**Ready for production use!** 🚀

---

## 📞 Need Help?

1. Check `RESUME_TAILOR_UPGRADE.md` for detailed documentation
2. Review backend terminal for API errors
3. Check browser console for frontend errors
4. Verify `.env` configuration
5. Ensure all dependencies installed: `pip install -r requirements.txt`

**Happy Tailoring!** ✨

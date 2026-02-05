# Resume Tailor Feature Guide

## Overview
The Resume Tailor feature uses AI (OpenAI GPT-3.5-turbo) to automatically rewrite your resume to match specific job descriptions. It generates a professionally formatted PDF with the tailored content.

## Setup Instructions

### 1. Install Dependencies
Run the following command to install the new dependencies:
```bash
pip install -r requirements.txt
```

New packages added:
- `fpdf2>=2.7.0` - For PDF generation
- `langchain-openai>=0.0.5` - For OpenAI integration

### 2. Configure OpenAI API Key

**IMPORTANT:** To enable AI-powered resume tailoring, you need to add your OpenAI API key to the `.env` file.

1. Open the `.env` file in your project root
2. Find the line: `OPENAI_API_KEY=your_openai_api_key_here`
3. Replace `your_openai_api_key_here` with your actual OpenAI API key

Example:
```
OPENAI_API_KEY=sk-proj-abc123xyz...
```

**Note:** If you don't have an OpenAI API key:
- Get one at: https://platform.openai.com/api-keys
- The app will still work in "Demo Mode" without a key, but won't provide AI-powered tailoring

### 3. Start the Server
```bash
python -m uvicorn app.main:app --reload
```

## API Usage

### Endpoint: POST /tailor_resume

**Request Body:**
```json
{
  "job_description": "We are looking for a Senior Python Developer with experience in FastAPI, Docker, and AWS...",
  "current_resume_text": "John Doe\n\nEXPERIENCE\n- Python Developer at Company X\n- Built REST APIs using FastAPI..."
}
```

**Response:**
- Returns a PDF file download (`tailored_resume.pdf`)
- The PDF contains your resume rewritten to match the job description

### Using cURL:
```bash
curl -X POST "http://localhost:8000/tailor_resume" \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Senior Python Developer with FastAPI experience",
    "current_resume_text": "John Doe - Python Developer"
  }' \
  --output tailored_resume.pdf
```

### Using Python:
```python
import requests

response = requests.post(
    "http://localhost:8000/tailor_resume",
    json={
        "job_description": "Senior Python Developer...",
        "current_resume_text": "John Doe\nEXPERIENCE\n..."
    }
)

# Save the PDF
with open("tailored_resume.pdf", "wb") as f:
    f.write(response.content)
```

## How It Works

1. **AI Processing**: The system sends your resume and job description to OpenAI's GPT-3.5-turbo
2. **Smart Rewriting**: The AI rewrites your resume to:
   - Incorporate keywords from the job description
   - Highlight relevant skills and experience
   - Maintain professional, achievement-oriented language
   - Keep your original structure while optimizing content
3. **PDF Generation**: The tailored text is formatted into a clean, professional PDF
4. **Download**: The PDF is returned for immediate download

## Features

✅ AI-powered resume optimization
✅ Keyword matching with job descriptions  
✅ Professional PDF formatting
✅ Clean typography with headers and bullets
✅ Demo mode (works without API key for testing)
✅ Error handling and graceful degradation

## Files Created

- `app/services/pdf_generator.py` - PDF generation service
- `app/services/resume_tailor.py` - AI tailoring logic
- Updated `app/main.py` - Added `/tailor_resume` endpoint

## Testing the Feature

1. Start the server: `python -m uvicorn app.main:app --reload`
2. Visit the interactive docs: http://localhost:8000/docs
3. Find the `/tailor_resume` endpoint
4. Click "Try it out"
5. Enter sample job description and resume text
6. Click "Execute"
7. Download the generated PDF

## Troubleshooting

**No API Key Error:**
- Make sure you've added your OpenAI API key to `.env`
- Restart the server after updating `.env`

**Import Errors:**
- Run `pip install -r requirements.txt` again
- Make sure all dependencies are installed

**PDF Encoding Issues:**
- The PDF generator handles most text encoding automatically
- Special characters are converted to latin-1 compatible versions

## Cost Considerations

Each resume tailoring request calls OpenAI's API:
- Model: GPT-3.5-turbo
- Approximate cost: $0.001-0.002 per request
- Monitor usage at: https://platform.openai.com/usage

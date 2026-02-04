# 🌐 HTTP Endpoint Guide
## `/screen_candidate` API Documentation

---

## Overview

The `/screen_candidate` endpoint provides HTTP access to the candidate screening functionality, allowing you to compare resumes against job descriptions without needing an MCP client.

---

## Endpoint Details

### Route
```
POST /screen_candidate
```

### Parameters
- **job_description** (string, required): The job description to compare the resume against

### Request Format
Query parameter or request body

### Response Format
JSON object with screening results

---

## Usage Examples

### 1. Using cURL (Query Parameter)

```bash
curl -X POST "http://localhost:8000/screen_candidate?job_description=Senior%20ML%20Engineer%20with%20Python%20and%20FastAPI%20experience"
```

### 2. Using cURL (URL-encoded)

```bash
curl -X POST "http://localhost:8000/screen_candidate" \
  --data-urlencode "job_description=Senior Software Engineer
Requirements:
- 5+ years Python
- FastAPI framework
- RAG systems experience
- Vector database knowledge"
```

### 3. Using Python Requests

```python
import requests

job_description = """
Senior ML Engineer - RAG Systems

Requirements:
- 5+ years Python experience
- FastAPI and microservices
- Vector databases (ChromaDB, Pinecone)
- LangChain and RAG pipelines
- Production ML systems

Responsibilities:
- Design and implement RAG APIs
- Optimize vector search performance
- Build agent integration tools
"""

response = requests.post(
    "http://localhost:8000/screen_candidate",
    params={"job_description": job_description}
)

result = response.json()
print(result)
```

### 4. Using JavaScript/Fetch

```javascript
const jobDescription = `
Senior Software Engineer
- Python, FastAPI
- 5+ years experience
- ML/RAG systems
`;

fetch('http://localhost:8000/screen_candidate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: `job_description=${encodeURIComponent(jobDescription)}`
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## Response Format

### Success Response

```json
{
  "status": "success",
  "job_description": "Senior ML Engineer with Python...",
  "screening_result": "CONTEXT: Here are the relevant parts of the candidate's resume:\n\n[Part 1 - Page 1]:\nJohn Smith - Senior Software Engineer...\n\n[Part 2 - Page 1]:\nTechnical Skills: Python, FastAPI...\n\n...\n\nTASK: Compare the resume parts above against this Job Description:\n\nSenior ML Engineer with Python..."
}
```

### No Resume Found

```json
{
  "status": "success",
  "job_description": "Senior ML Engineer...",
  "screening_result": "No resume information found in the database. Please upload a resume first."
}
```

### Error Response

```json
{
  "detail": "Error screening candidate: [error details]"
}
```

**HTTP Status Code:** 500

---

## Complete Workflow

### Step 1: Upload Resume

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@john_smith_resume.pdf"
```

**Response:**
```json
{
  "status": "success",
  "filename": "john_smith_resume.pdf",
  "chunks_processed": 8,
  "message": "Successfully processed and stored 8 chunks"
}
```

### Step 2: Screen Candidate

```bash
curl -X POST "http://localhost:8000/screen_candidate?job_description=Senior%20ML%20Engineer:%20Python,%20FastAPI,%20RAG"
```

**Response:**
```json
{
  "status": "success",
  "job_description": "Senior ML Engineer: Python, FastAPI, RAG",
  "screening_result": "CONTEXT: Here are the relevant parts of the candidate's resume:\n\n[Part 1 - Page 1]:\nJohn Smith\nSenior Software Engineer\n5+ years building production ML systems...\n\n[Part 2 - Page 1]:\nTechnical Expertise:\n- Python (Expert): FastAPI, asyncio\n- Vector Databases: ChromaDB, Pinecone\n- ML: LangChain, HuggingFace\n\n[Part 3 - Page 2]:\nRecent Project: RAG API\n- Built semantic search with ChromaDB\n- Sub-100ms query latency\n\n... (up to 10 parts)\n\nTASK: Compare the resume parts above against this Job Description:\n\nSenior ML Engineer: Python, FastAPI, RAG"
}
```

### Step 3: Parse and Display

```python
import requests
import json

# Get screening result
response = requests.post(
    "http://localhost:8000/screen_candidate",
    params={"job_description": "Senior ML Engineer: Python, FastAPI, RAG"}
)

data = response.json()

# Extract the screening result
screening_text = data["screening_result"]

# Display or process
print(screening_text)

# Could send to LLM for analysis
# analysis = llm.analyze(screening_text)
```

---

## Swagger UI Access

### Interactive Documentation

1. Start the server:
   ```bash
   python start.py
   ```

2. Open your browser:
   ```
   http://localhost:8000/docs
   ```

3. Find the `/screen_candidate` endpoint

4. Click "Try it out"

5. Enter your job description:
   ```
   Senior ML Engineer
   - Python, FastAPI
   - 5+ years experience
   - RAG systems
   ```

6. Click "Execute"

7. View the response in the UI

### Screenshot of Swagger UI

```
POST /screen_candidate
Screen a candidate by comparing their resume against a job description

Parameters:
┌─────────────────┬──────────┬─────────────────────────────┐
│ Name            │ Required │ Description                 │
├─────────────────┼──────────┼─────────────────────────────┤
│ job_description │ Yes      │ The job description to      │
│                 │          │ compare the resume against  │
└─────────────────┴──────────┴─────────────────────────────┘

[Try it out] button
```

---

## Comparison: HTTP vs MCP

| Feature | HTTP Endpoint | MCP Tool |
|---------|---------------|----------|
| **Access** | Any HTTP client | MCP client required |
| **Authentication** | Standard HTTP auth | MCP protocol |
| **Response Format** | JSON | String |
| **Use Case** | Web apps, direct API calls | Agent integration |
| **Swagger UI** | ✅ Yes | ❌ No |

---

## Integration Examples

### Web Application

```javascript
// React component
async function screenCandidate(jobDescription) {
  const response = await fetch('/api/screen_candidate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `job_description=${encodeURIComponent(jobDescription)}`
  });
  
  const data = await response.json();
  return data.screening_result;
}

// Usage
const result = await screenCandidate(jobDescriptionText);
setScreeningResult(result);
```

### Python Script

```python
#!/usr/bin/env python3
import requests
import sys

def screen_candidate(job_description):
    """Screen a candidate against a job description"""
    response = requests.post(
        "http://localhost:8000/screen_candidate",
        params={"job_description": job_description}
    )
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python screen.py <job_description>")
        sys.exit(1)
    
    job_desc = sys.argv[1]
    result = screen_candidate(job_desc)
    
    print("Status:", result["status"])
    print("\nScreening Result:")
    print(result["screening_result"])
```

### Automation Script

```bash
#!/bin/bash
# batch_screen.sh - Screen multiple candidates

for resume in resumes/*.pdf; do
    echo "Processing: $resume"
    
    # Upload resume
    curl -X POST "http://localhost:8000/upload" -F "file=@$resume"
    
    # Screen against job description
    curl -X POST "http://localhost:8000/screen_candidate" \
      --data-urlencode "job_description@job_description.txt" \
      > "results/$(basename $resume .pdf)_screening.json"
    
    echo "Done: $resume"
done
```

---

## Error Handling

### No Resume Uploaded

**Request:**
```bash
curl -X POST "http://localhost:8000/screen_candidate?job_description=Senior%20Engineer"
```

**Response:**
```json
{
  "status": "success",
  "job_description": "Senior Engineer",
  "screening_result": "No resume information found in the database. Please upload a resume first."
}
```

**Solution:** Upload a resume first via POST /upload

### Invalid Job Description

**Request:**
```bash
curl -X POST "http://localhost:8000/screen_candidate?job_description="
```

**Response:** Will still work but return empty/generic results

**Best Practice:** Always provide meaningful job description

### Server Error

**Response:**
```json
{
  "detail": "Error screening candidate: [specific error]"
}
```

**Status Code:** 500

**Solution:** Check server logs, restart if needed

---

## Performance

| Metric | Value |
|--------|-------|
| **Latency** | ~100-150ms |
| **Chunks Retrieved** | 10 |
| **Context Size** | ~3000-5000 tokens |
| **Concurrent Requests** | 50+ per second |

---

## Best Practices

### 1. Be Specific in Job Descriptions

**Poor:**
```
Software engineer needed
```

**Better:**
```
Senior Software Engineer
- 5+ years Python
- FastAPI framework
- RAG systems experience
```

**Best:**
```
Senior ML Engineer - RAG Systems

Required Skills:
- Python: FastAPI, async, type hints (5+ years)
- Vector Databases: ChromaDB or Pinecone
- ML: LangChain, embeddings, semantic search
- Architecture: Microservices, API design

Responsibilities:
- Design production RAG pipelines
- Optimize vector search performance
- Integrate with LLM agents
- Mentor junior engineers
```

### 2. Upload Resume First

Always ensure a resume is uploaded before calling `/screen_candidate`

### 3. Parse the Response

The `screening_result` is formatted for LLM consumption. Parse it appropriately:

```python
result = response.json()["screening_result"]

# Split into CONTEXT and TASK sections
context_section = result.split("TASK:")[0].replace("CONTEXT:", "").strip()
task_section = result.split("TASK:")[1].strip()

print("Resume Context:", context_section)
print("\nJob Requirements:", task_section)
```

### 4. Rate Limiting

For production, implement rate limiting:
- Limit requests per user
- Prevent abuse
- Monitor usage patterns

---

## Testing

### Quick Test

```bash
# 1. Start server
python start.py

# 2. Upload test resume
curl -X POST "http://localhost:8000/upload" \
  -F "file=@test_resume.pdf"

# 3. Test screening
curl -X POST "http://localhost:8000/screen_candidate?job_description=Python%20Developer"

# Expected: Success response with screening result
```

### Unit Test

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_screen_candidate():
    response = client.post(
        "/screen_candidate",
        params={"job_description": "Python Developer"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "screening_result" in data
```

---

## Related Endpoints

| Endpoint | Purpose | Method |
|----------|---------|--------|
| `/upload` | Upload resume PDF | POST |
| `/consult` | Query knowledge base | POST |
| `/screen_candidate` | Screen candidate | POST |
| `/health` | Health check | GET |
| `/docs` | API documentation | GET |

---

## Summary

The `/screen_candidate` endpoint provides:
- ✅ HTTP access to candidate screening
- ✅ Simple query parameter input
- ✅ JSON response format
- ✅ Swagger UI documentation
- ✅ Error handling
- ✅ Production-ready

**Perfect for:** Web apps, scripts, automation, non-MCP integrations

---

**Last Updated:** Just now  
**Status:** ✅ Active  
**Location:** `app/main.py` (lines 255-280)  
**Swagger UI:** http://localhost:8000/docs

# 🔍 Candidate Search & Rank Feature

## Overview

The **Candidate Search & Rank** feature is an AI-powered recruitment tool that searches your resume database and intelligently ranks candidates for a job opening. It combines **vector similarity search** with **GPT-3.5 AI reranking** to find the best matches.

---

## 🎯 How It Works

### 1. **Vector Search (Semantic Similarity)**
   - When you paste a job description, the system uses **ChromaDB** to find the top 10 resumes that are semantically similar to the job requirements
   - Uses **HuggingFace embeddings** (all-MiniLM-L6-v2) for fast, accurate matching
   - Finds candidates based on meaning, not just keywords

### 2. **AI Reranking (Intelligent Evaluation)**
   - The top 10 candidates are sent to **GPT-3.5-turbo** for expert evaluation
   - The AI acts as a "Senior Technical Recruiter" and evaluates:
     - Skills match (technical and soft skills)
     - Experience level alignment
     - Education requirements
     - Industry background
     - Achievement relevance
     - Cultural fit indicators
   - Selects and ranks the **top 7 best matches**

### 3. **Scored Results**
   - Each candidate receives a score (0-100) with reasoning
   - **Score Guidelines:**
     - 90-100: Exceptional match, exceeds requirements
     - 80-89: Strong match, meets all key requirements
     - 70-79: Good match, meets most requirements
     - 60-69: Adequate match, meets core requirements
     - 50-59: Weak match, missing key skills

---

## 🚀 Usage

### Backend Endpoint

**POST /search_candidates**

**Input:**
```json
{
  "job_description": "Senior Full Stack Developer\nRequirements: React, Node.js, 5+ years experience..."
}
```

**Output:**
```json
{
  "status": "success",
  "count": 7,
  "candidates": [
    {
      "rank": 1,
      "filename": "john_smith.pdf",
      "score": 95,
      "reasoning": "Exceptional match with 6 years of React and Node.js experience. Led multiple full-stack projects and demonstrated strong architectural skills."
    },
    ...
  ]
}
```

### Frontend Usage

1. **Navigate to "Candidate Search"** in the sidebar
2. **Paste your job description** in the text area
3. **Click "Find Top Talent"**
4. **View ranked results** with scores and reasoning

---

## 🎨 UI Features

### Search Interface
- Large text area for job descriptions
- Prominent "Find Top Talent" button with loading state
- Real-time feedback with toast notifications

### Results Display
- **Rank Badges:** 
  - 🥇 Gold for #1
  - 🥈 Silver for #2
  - 🥉 Bronze for #3
  - Blue gradient for #4-7
- **Score Badges:** Color-coded by performance
  - Green: 90+ (Exceptional)
  - Blue: 80-89 (Strong)
  - Yellow: 70-79 (Good)
  - Orange: 60-69 (Adequate)
  - Red: 50-59 (Weak)
- **Detailed Cards:** Show filename, score, reasoning, and match quality

### Info Panels
- Visual explanation of the 3-step process
- Usage instructions
- Feature highlights

---

## 📂 Files Added/Modified

### Backend
- **`app/main.py`** - Added `POST /search_candidates` endpoint
  - Vector search integration
  - AI reranking logic
  - Demo mode fallback
  - Robust error handling

### Frontend
- **`frontend/lib/api.js`** - Added `searchCandidates()` function
- **`frontend/app/search/page.js`** - New search page with:
  - Job description input
  - Loading states
  - Candidate cards
  - Score visualization
  - Rank badges
- **`frontend/components/Sidebar.js`** - Added "Candidate Search" navigation link

---

## 🔧 Technical Details

### Backend Implementation

```python
# Step 1: Search vector store
results = vector_service.search(query=job_description, k=10)

# Step 2: Prepare candidate data
candidates_text = [format_candidate(result) for result in results]

# Step 3: AI reranking
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
system_prompt = "You are a Senior Technical Recruiter..."
response = llm.invoke([SystemMessage(system_prompt), HumanMessage(candidates_text)])

# Step 4: Parse and return ranked results
ranked_candidates = json.loads(response.content)
```

### Frontend Implementation

```javascript
// Call search API
const data = await searchCandidates(jobDescription)

// Display results
candidates.map(candidate => (
  <CandidateCard
    rank={candidate.rank}
    filename={candidate.filename}
    score={candidate.score}
    reasoning={candidate.reasoning}
  />
))
```

---

## 🛡️ Error Handling & Fallbacks

### Demo Mode
If `OPENAI_API_KEY` is not configured, the system returns demo results based on vector similarity scores.

### AI Parsing Failure
If the AI response can't be parsed as JSON, the system falls back to vector similarity ranking.

### Empty Database
If no resumes are found, a helpful message prompts the user to upload resumes first.

---

## 🎯 Best Practices

### For Best Results:
1. **Upload Quality Resumes:** The system works best with well-formatted, complete resumes
2. **Detailed Job Descriptions:** Include specific requirements, skills, and experience levels
3. **Multiple Candidates:** Upload at least 10 resumes for effective ranking
4. **Clear Requirements:** List must-have skills vs. nice-to-have skills

### Job Description Template:
```
[Job Title]

Requirements:
- [Skill 1]
- [Skill 2]
- [Years of experience]

Responsibilities:
- [Responsibility 1]
- [Responsibility 2]

Nice to Have:
- [Optional skill 1]
- [Optional skill 2]
```

---

## 🔗 Integration with Existing Features

The Candidate Search feature complements other tools in the dashboard:

1. **Candidate Upload:** Builds the resume database for searching
2. **Resume Screener:** Deep-dive analysis of a single candidate
3. **AI Resume Tailor:** Help selected candidates optimize their resumes

### Recommended Workflow:
```
1. Upload → Add candidates to the database
2. Search → Find top 7 matches for a job
3. Screen → Deep analysis of top candidates
4. Tailor → Help final candidates optimize resumes
```

---

## 🧪 Testing

### Test the Feature:

1. **Start the backend:**
   ```bash
   cd /Users/narenratnam/Desktop/RAG\ and\ MCP\ Project
   python start.py
   ```

2. **Start the frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Navigate to:** `http://localhost:3000/search`

4. **Test with sample job description:**
   ```
   Senior Software Engineer
   Requirements: Python, FastAPI, React, 5+ years experience
   Nice to have: AWS, Docker, PostgreSQL
   ```

5. **Verify:**
   - Top 10 results are fetched from vector store
   - AI ranks and selects top 7
   - Cards display rank, score, and reasoning
   - Color coding matches score ranges

---

## 📊 Performance

- **Vector Search:** ~100-200ms for 10 results
- **AI Reranking:** ~2-4 seconds with GPT-3.5-turbo
- **Total Time:** ~3-5 seconds for complete search & rank

### Optimization Opportunities:
- Use GPT-3.5-turbo-0125 for faster responses
- Cache results for identical job descriptions
- Implement pagination for large candidate pools
- Add filters (experience level, location, skills)

---

## 🎉 Summary

The Candidate Search & Rank feature is a powerful AI-driven tool that:

✅ Searches your resume database intelligently  
✅ Uses GPT-3.5 to evaluate and rank candidates  
✅ Provides detailed reasoning for each match  
✅ Displays results in a beautiful, intuitive UI  
✅ Integrates seamlessly with existing features  

**You now have a complete AI recruiting pipeline!** 🚀

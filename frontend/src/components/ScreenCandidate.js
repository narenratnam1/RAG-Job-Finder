import React, { useState } from 'react';
import apiService from '../services/api';

function ScreenCandidate() {
  const [jobDescription, setJobDescription] = useState('');
  const [screening, setScreening] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleScreen = async (e) => {
    e.preventDefault();
    
    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    setScreening(true);
    setError(null);
    setResult(null);

    try {
      const screeningResult = await apiService.screenCandidate(jobDescription);
      setResult(screeningResult);
    } catch (err) {
      setError(err.response?.data?.detail || 'Screening failed. Please try again.');
    } finally {
      setScreening(false);
    }
  };

  const handleClear = () => {
    setJobDescription('');
    setResult(null);
    setError(null);
  };

  const loadSampleJobDescription = () => {
    const sample = `Senior Software Engineer - RAG Systems

Required Skills:
- 5+ years Python experience
- FastAPI and microservices architecture
- Vector databases (ChromaDB, Pinecone)
- LangChain and RAG pipelines
- Machine Learning fundamentals

Responsibilities:
- Design and implement production RAG APIs
- Optimize vector search performance
- Build agent integration tools
- Mentor junior engineers`;
    
    setJobDescription(sample);
  };

  const parseScreeningResult = (resultText) => {
    if (!resultText) return { context: '', task: '' };
    
    const parts = resultText.split('TASK:');
    const context = parts[0].replace('CONTEXT:', '').trim();
    const task = parts[1] ? parts[1].trim() : '';
    
    return { context, task };
  };

  return (
    <div className="screen-container">
      <div className="section-header">
        <h2>Screen Candidate</h2>
        <p>Compare uploaded resume against job description using semantic matching</p>
      </div>

      <form onSubmit={handleScreen} className="screen-form">
        <div className="form-group">
          <label htmlFor="job-description">Job Description</label>
          <textarea
            id="job-description"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the job description here...&#10;&#10;Include:&#10;- Required skills&#10;- Years of experience&#10;- Responsibilities&#10;- Nice-to-have qualifications"
            className="job-description-input"
            rows="10"
            disabled={screening}
          />
          <div className="form-actions">
            <button
              type="button"
              onClick={loadSampleJobDescription}
              className="sample-button"
            >
              Load Sample
            </button>
            <button
              type="submit"
              disabled={screening || !jobDescription.trim()}
              className="screen-button"
            >
              {screening ? '⏳ Screening...' : '🎯 Screen Candidate'}
            </button>
            {jobDescription && (
              <button
                type="button"
                onClick={handleClear}
                className="clear-button"
              >
                Clear
              </button>
            )}
          </div>
        </div>
      </form>

      {error && (
        <div className="alert alert-error">
          <span className="alert-icon">❌</span>
          <span>{error}</span>
        </div>
      )}

      {result && (
        <div className="screening-result">
          <div className="result-header">
            <h3>📊 Screening Results</h3>
            <span className="result-status">Analysis Complete</span>
          </div>

          {result.screening_result.includes('No resume information') ? (
            <div className="no-resume">
              <p>⚠️ No resume found in database</p>
              <p className="hint">
                Please upload a resume PDF in the "Upload Documents" tab first.
              </p>
            </div>
          ) : (
            <>
              <div className="context-section">
                <h4>📄 Resume Context (Top 10 Relevant Sections)</h4>
                <div className="context-content">
                  <pre>{parseScreeningResult(result.screening_result).context}</pre>
                </div>
              </div>

              <div className="task-section">
                <h4>🎯 Comparison Task</h4>
                <div className="task-content">
                  <pre>{parseScreeningResult(result.screening_result).task}</pre>
                </div>
              </div>

              <div className="analysis-note">
                <p>
                  <strong>💡 Next Step:</strong> Use this context with an LLM (Claude, GPT-4, etc.) 
                  to analyze how well the candidate matches the job requirements.
                </p>
              </div>
            </>
          )}
        </div>
      )}

      <div className="info-box">
        <h3>🎓 How It Works</h3>
        <ol>
          <li><strong>Upload Resume:</strong> First, upload candidate's resume as PDF</li>
          <li><strong>Enter Job Description:</strong> Paste or type the job requirements</li>
          <li><strong>Semantic Matching:</strong> System retrieves top 10 most relevant resume sections</li>
          <li><strong>AI Analysis:</strong> Use the formatted output with your LLM for evaluation</li>
        </ol>
      </div>

      <div className="workflow-steps">
        <div className="step">
          <div className="step-number">1</div>
          <div className="step-content">
            <h4>Upload Resume</h4>
            <p>PDF document processed and vectorized</p>
          </div>
        </div>
        <div className="step-arrow">→</div>
        <div className="step">
          <div className="step-number">2</div>
          <div className="step-content">
            <h4>Enter Job Description</h4>
            <p>Requirements analyzed semantically</p>
          </div>
        </div>
        <div className="step-arrow">→</div>
        <div className="step">
          <div className="step-number">3</div>
          <div className="step-content">
            <h4>Get Match Analysis</h4>
            <p>Top 10 relevant resume sections</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ScreenCandidate;

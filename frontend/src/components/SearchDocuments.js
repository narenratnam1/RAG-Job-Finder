import React, { useState } from 'react';
import apiService from '../services/api';

function SearchDocuments() {
  const [query, setQuery] = useState('');
  const [searching, setSearching] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a search query');
      return;
    }

    setSearching(true);
    setError(null);
    setResults(null);

    try {
      const searchResults = await apiService.consultDocuments(query);
      setResults(searchResults);
    } catch (err) {
      setError(err.response?.data?.detail || 'Search failed. Please try again.');
    } finally {
      setSearching(false);
    }
  };

  const handleClear = () => {
    setQuery('');
    setResults(null);
    setError(null);
  };

  return (
    <div className="search-container">
      <div className="section-header">
        <h2>Search Documents</h2>
        <p>Semantic search across all uploaded documents using AI embeddings</p>
      </div>

      <form onSubmit={handleSearch} className="search-form">
        <div className="search-input-group">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your question or search query..."
            className="search-input"
            disabled={searching}
          />
          <button
            type="submit"
            disabled={searching || !query.trim()}
            className="search-button"
          >
            {searching ? '🔄 Searching...' : '🔍 Search'}
          </button>
          {(query || results) && (
            <button
              type="button"
              onClick={handleClear}
              className="clear-button"
            >
              Clear
            </button>
          )}
        </div>
      </form>

      {error && (
        <div className="alert alert-error">
          <span className="alert-icon">❌</span>
          <span>{error}</span>
        </div>
      )}

      {results && (
        <div className="results-container">
          <div className="results-header">
            <h3>Search Results</h3>
            <span className="results-count">
              {results.results_count} result{results.results_count !== 1 ? 's' : ''} found
            </span>
          </div>

          {results.results_count === 0 ? (
            <div className="no-results">
              <p>No relevant documents found.</p>
              <p className="hint">Try uploading documents first or rephrase your query.</p>
            </div>
          ) : (
            <div className="results-list">
              {results.results.map((result, index) => (
                <div key={index} className="result-card">
                  <div className="result-header">
                    <span className="result-rank">#{result.rank}</span>
                    <div className="result-meta">
                      <span className="result-source">📄 {result.source}</span>
                      <span className="result-page">Page {result.page}</span>
                      <span className="result-score">
                        {(result.relevance_score * 100).toFixed(1)}% match
                      </span>
                    </div>
                  </div>
                  <div className="result-content">
                    <p>{result.content}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      <div className="info-box">
        <h3>💡 Search Tips</h3>
        <ul>
          <li>Use natural language questions: "What is the refund policy?"</li>
          <li>Be specific for better results: "Python experience with FastAPI"</li>
          <li>Semantic search finds meaning, not just keywords</li>
          <li>Returns top 3 most relevant chunks from all documents</li>
        </ul>
      </div>

      {results && results.results_count > 0 && (
        <div className="search-stats">
          <p>
            <strong>Query:</strong> "{results.query}"
          </p>
          <p>
            <strong>Processing time:</strong> ~100ms • <strong>Model:</strong> all-MiniLM-L6-v2
          </p>
        </div>
      )}
    </div>
  );
}

export default SearchDocuments;

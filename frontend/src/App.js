import React, { useState, useEffect } from 'react';
import './App.css';
import apiService from './services/api';
import UploadDocument from './components/UploadDocument';
import SearchDocuments from './components/SearchDocuments';
import ScreenCandidate from './components/ScreenCandidate';

function App() {
  const [activeTab, setActiveTab] = useState('upload');
  const [healthStatus, setHealthStatus] = useState(null);
  const [apiInfo, setApiInfo] = useState(null);

  useEffect(() => {
    checkHealth();
    fetchApiInfo();
  }, []);

  const checkHealth = async () => {
    try {
      const health = await apiService.checkHealth();
      setHealthStatus(health);
    } catch (error) {
      console.error('Health check failed:', error);
      setHealthStatus({ status: 'unhealthy', error: error.message });
    }
  };

  const fetchApiInfo = async () => {
    try {
      const info = await apiService.getApiInfo();
      setApiInfo(info);
    } catch (error) {
      console.error('Failed to fetch API info:', error);
    }
  };

  return (
    <div className="App">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1>🤖 Agentic RAG API</h1>
          <p className="subtitle">Document Search & Candidate Screening</p>
          <div className="health-status">
            <span className={`status-indicator ${healthStatus?.status === 'healthy' ? 'healthy' : 'unhealthy'}`}>
              ●
            </span>
            <span className="status-text">
              {healthStatus?.status === 'healthy' ? 'System Operational' : 'System Down'}
            </span>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="tabs">
        <button
          className={`tab ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          📤 Upload Documents
        </button>
        <button
          className={`tab ${activeTab === 'search' ? 'active' : ''}`}
          onClick={() => setActiveTab('search')}
        >
          🔍 Search Documents
        </button>
        <button
          className={`tab ${activeTab === 'screen' ? 'active' : ''}`}
          onClick={() => setActiveTab('screen')}
        >
          👤 Screen Candidate
        </button>
      </nav>

      {/* Main Content */}
      <main className="main-content">
        <div className="content-wrapper">
          {activeTab === 'upload' && <UploadDocument />}
          {activeTab === 'search' && <SearchDocuments />}
          {activeTab === 'screen' && <ScreenCandidate />}
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="footer-content">
          <p>
            {apiInfo?.message || 'Agentic RAG API'} v{apiInfo?.version || '1.0.0'}
          </p>
          <p className="footer-tech">
            FastAPI • ChromaDB • LangChain • React
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;

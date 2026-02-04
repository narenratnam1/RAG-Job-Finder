import React, { useState } from 'react';
import apiService from '../services/api';

function UploadDocument() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setError(null);
      setUploadResult(null);
    } else {
      setError('Please select a PDF file');
      setSelectedFile(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setUploading(true);
    setError(null);
    setUploadResult(null);

    try {
      const result = await apiService.uploadDocument(selectedFile);
      setUploadResult(result);
      setSelectedFile(null);
      // Reset file input
      document.getElementById('file-input').value = '';
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    const file = e.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setError(null);
      setUploadResult(null);
    } else {
      setError('Please drop a PDF file');
    }
  };

  return (
    <div className="upload-container">
      <div className="section-header">
        <h2>Upload PDF Document</h2>
        <p>Upload resumes, policies, or any PDF document to add to the knowledge base</p>
      </div>

      <div
        className="upload-area"
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        <div className="upload-icon">📄</div>
        <p className="upload-text">
          Drag and drop a PDF file here, or click to select
        </p>
        <input
          id="file-input"
          type="file"
          accept=".pdf"
          onChange={handleFileSelect}
          className="file-input"
        />
        <label htmlFor="file-input" className="file-label">
          Choose File
        </label>
      </div>

      {selectedFile && (
        <div className="selected-file">
          <div className="file-info">
            <span className="file-icon">📎</span>
            <div className="file-details">
              <span className="file-name">{selectedFile.name}</span>
              <span className="file-size">
                {(selectedFile.size / 1024).toFixed(2)} KB
              </span>
            </div>
          </div>
          <button
            onClick={handleUpload}
            disabled={uploading}
            className="upload-button"
          >
            {uploading ? 'Uploading...' : 'Upload Document'}
          </button>
        </div>
      )}

      {error && (
        <div className="alert alert-error">
          <span className="alert-icon">❌</span>
          <span>{error}</span>
        </div>
      )}

      {uploadResult && (
        <div className="alert alert-success">
          <span className="alert-icon">✅</span>
          <div>
            <p><strong>Upload Successful!</strong></p>
            <p>File: {uploadResult.filename}</p>
            <p>Chunks processed: {uploadResult.chunks_processed}</p>
            <p className="message">{uploadResult.message}</p>
          </div>
        </div>
      )}

      <div className="info-box">
        <h3>📝 Upload Guidelines</h3>
        <ul>
          <li>Only PDF files are supported</li>
          <li>Documents are automatically chunked and embedded</li>
          <li>Each chunk is ~1000 characters with 100-character overlap</li>
          <li>Use meaningful filenames for better organization</li>
        </ul>
      </div>
    </div>
  );
}

export default UploadDocument;

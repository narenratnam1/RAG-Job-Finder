import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Health check
  async checkHealth() {
    const response = await api.get('/health');
    return response.data;
  },

  // Upload PDF document
  async uploadDocument(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Search/consult documents
  async consultDocuments(query) {
    const response = await api.post('/consult', null, {
      params: { query },
    });
    return response.data;
  },

  // Screen candidate
  async screenCandidate(jobDescription) {
    const response = await api.post('/screen_candidate', null, {
      params: { job_description: jobDescription },
    });
    return response.data;
  },

  // Get API info
  async getApiInfo() {
    const response = await api.get('/');
    return response.data;
  },
};

export default apiService;

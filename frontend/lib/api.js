import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Upload a PDF file to the backend
 * @param {File} file - The PDF file to upload
 * @returns {Promise<Object>} Upload result
 */
export async function uploadPDF(file) {
  const formData = new FormData()
  formData.append('file', file)

  try {
    // Don't set Content-Type header - let browser set it with boundary
    const response = await axios.post(`${API_BASE_URL}/upload`, formData)
    return response.data
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.message || 'Failed to upload PDF'
    console.error('Upload PDF error:', error.response?.data || error)
    throw new Error(errorMessage)
  }
}

/**
 * Screen a candidate against a job description using saved resume
 * @param {string} jobDescription - The job description
 * @param {string} resumeFilename - The saved resume filename
 * @returns {Promise<Object>} Screening results with score and analysis
 */
export async function screenCandidate(jobDescription, resumeFilename) {
  try {
    const formData = new FormData()
    formData.append('job_description', jobDescription)
    formData.append('resume_filename', resumeFilename)
    
    const response = await axios.post(`${API_BASE_URL}/screen_candidate`, formData)
    return response.data
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.message || 'Failed to screen candidate'
    console.error('Screen candidate error:', error.response?.data || error)
    throw new Error(errorMessage)
  }
}

/**
 * Search and rank top candidates for a job description
 * @param {string} jobDescription - The job description
 * @returns {Promise<Object>} Top 7 ranked candidates with scores
 */
export async function searchCandidates(jobDescription) {
  try {
    const formData = new FormData()
    formData.append('job_description', jobDescription)
    
    const response = await axios.post(`${API_BASE_URL}/search_candidates`, formData)
    return response.data
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.message || 'Failed to search candidates'
    console.error('Search candidates error:', error.response?.data || error)
    throw new Error(errorMessage)
  }
}

/**
 * Get list of saved resumes from library
 * @returns {Promise<Object>} Response with list of resumes
 */
export async function getResumes() {
  try {
    const response = await api.get('/resumes')
    return response.data
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.message || 'Failed to fetch resumes'
    console.error('Get resumes error:', error.response?.data || error)
    throw new Error(errorMessage)
  }
}

/**
 * Tailor resume to job description with file upload OR saved resume (returns preview text)
 * @param {string} jobDescription - The target job description
 * @param {File|null} resumeFile - The resume PDF file (if uploading new)
 * @param {string|null} resumeFilename - The saved resume filename (if using library)
 * @returns {Promise<Object>} Response with tailored_text
 */
export async function tailorResumeWithFile(jobDescription, resumeFile = null, resumeFilename = null) {
  try {
    const formData = new FormData()
    formData.append('job_description', jobDescription)
    
    if (resumeFilename) {
      // Use saved resume from library
      formData.append('resume_filename', resumeFilename)
    } else if (resumeFile) {
      // Use uploaded file
      formData.append('resume_file', resumeFile)
    } else {
      throw new Error('Either resumeFile or resumeFilename must be provided')
    }

    // Don't set Content-Type header - let browser set it with boundary
    const response = await axios.post(`${API_BASE_URL}/tailor_resume`, formData)
    return response.data
  } catch (error) {
    // Better error handling - extract detail or show full error
    const errorMessage = error.response?.data?.detail || error.message || 'Failed to tailor resume'
    console.error('Tailor resume error:', error.response?.data || error)
    throw new Error(errorMessage)
  }
}

/**
 * Generate PDF from tailored text
 * @param {string} content - The tailored resume text
 * @returns {Promise<Blob>} PDF blob
 */
export async function generatePDF(content) {
  try {
    const response = await axios.post(`${API_BASE_URL}/generate_pdf`, 
      JSON.stringify({ content: content }),
      {
        headers: {
          'Content-Type': 'application/json'
        },
        responseType: 'blob'
      }
    )
    return response.data
  } catch (error) {
    if (error.response?.data instanceof Blob) {
      // Try to parse error from blob
      try {
        const text = await error.response.data.text()
        const json = JSON.parse(text)
        const errorMessage = json.detail || 'Failed to generate PDF'
        console.error('Generate PDF error:', json)
        throw new Error(errorMessage)
      } catch (parseError) {
        console.error('Generate PDF error (could not parse):', parseError)
        throw new Error('Failed to generate PDF')
      }
    }
    const errorMessage = error.response?.data?.detail || error.message || 'Failed to generate PDF'
    console.error('Generate PDF error:', error.response?.data || error)
    throw new Error(errorMessage)
  }
}

export default api

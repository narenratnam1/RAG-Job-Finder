import axios from 'axios'

// Production: set NEXT_PUBLIC_API_URL to your deployed API (https://...).
// Local dev: if unset, use same-origin proxy /api-backend (see next.config.js → BACKEND_URL, default :8000).
const getApiBaseUrl = () => {
  const explicit = process.env.NEXT_PUBLIC_API_URL?.trim()
  if (explicit) {
    let apiUrl = explicit
    if (!apiUrl.includes('localhost') && !apiUrl.startsWith('https://')) {
      apiUrl = apiUrl.replace('http://', 'https://')
      if (!apiUrl.startsWith('https://')) {
        apiUrl = 'https://' + apiUrl
      }
    }
    return apiUrl.replace(/\/$/, '')
  }
  return '/api-backend'
}

const API_BASE_URL = getApiBaseUrl()

// Log API URL for debugging (only in browser)
if (typeof window !== 'undefined') {
  console.log('🔗 API Base URL:', API_BASE_URL)
  const isLocal =
    API_BASE_URL.includes('localhost') || API_BASE_URL.startsWith('/')
  console.log('🌍 Environment:', isLocal ? 'Development' : 'Production')
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Export API_BASE_URL so components can access it
export { API_BASE_URL }

/**
 * Upload a PDF file to the backend
 * @param {File} file - The PDF file to upload
 * @returns {Promise<Object>} Upload result
 */
export async function uploadPDF(file) {
  const formData = new FormData()
  formData.append('file', file)
  
  const uploadUrl = `${API_BASE_URL}/upload`
  console.log('📤 Uploading to:', uploadUrl)
  console.log('📄 File:', file.name, `(${(file.size / 1024).toFixed(2)} KB)`)

  try {
    // Don't set Content-Type header - let browser set it with boundary
    const response = await axios.post(uploadUrl, formData)
    console.log('✅ Upload successful:', response.data)
    return response.data
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.message || 'Failed to upload PDF'
    console.error('❌ Upload PDF error:', error.response?.data || error)
    console.error('❌ Error status:', error.response?.status)
    console.error('❌ Error URL:', uploadUrl)
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
  const screenUrl = `${API_BASE_URL}/screen_candidate`
  console.log('🔍 Screening candidate at:', screenUrl)
  
  try {
    const formData = new FormData()
    formData.append('job_description', jobDescription)
    formData.append('resume_filename', resumeFilename)
    
    const response = await axios.post(screenUrl, formData)
    console.log('✅ Screening successful')
    return response.data
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.message || 'Failed to screen candidate'
    console.error('❌ Screen candidate error:', error.response?.data || error)
    throw new Error(errorMessage)
  }
}

/**
 * Search and rank top candidates for a job description
 * @param {string} jobDescription - The job description
 * @returns {Promise<Object>} Top 7 ranked candidates with scores
 */
export async function searchCandidates(jobDescription) {
  const searchUrl = `${API_BASE_URL}/search_candidates`
  console.log('🔎 Searching candidates at:', searchUrl)
  
  try {
    const formData = new FormData()
    formData.append('job_description', jobDescription)
    
    const response = await axios.post(searchUrl, formData)
    console.log('✅ Search successful:', response.data?.count, 'candidates found')
    return response.data
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.message || 'Failed to search candidates'
    console.error('❌ Search candidates error:', error.response?.data || error)
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
    const detail = error.response?.data?.detail
    const isNetwork =
      error.code === 'ERR_NETWORK' ||
      error.message?.includes('Network Error') ||
      !error.response
    const hint = isNetwork
      ? `Cannot reach the Python API (proxied from ${API_BASE_URL}). From the project root run: npm run dev:all (starts Next + API), or in a second terminal: python start.py (with venv active). For a remote API, set NEXT_PUBLIC_API_URL in frontend/.env.local.`
      : null
    const errorMessage =
      [detail || error.message || 'Failed to fetch resumes', hint].filter(Boolean).join(' ')
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

/**
 * Agent chat (OpenAI + MCP tools on the backend). Pass full transcript; last turn must be user.
 * @param {Array<{ role: string, content: string }>} messages
 * @returns {Promise<{ role: string, content: string }>}
 */
export async function sendAgentChat(messages) {
  try {
    const response = await api.post('/api/chat', { messages })
    return response.data
  } catch (error) {
    const detail = error.response?.data?.detail
    let errorMessage = error.message || 'Chat request failed'
    if (typeof detail === 'string') {
      errorMessage = detail
    } else if (Array.isArray(detail) && detail.length) {
      errorMessage = detail.map((d) => d.msg || JSON.stringify(d)).join('; ')
    }
    console.error('Agent chat error:', error.response?.data || error)
    throw new Error(errorMessage)
  }
}

export default api

'use client'

import { useState } from 'react'
import { Search, FileSearch, CheckCircle, XCircle, AlertCircle, Award, TrendingUp } from 'lucide-react'
import toast from 'react-hot-toast'
import { screenCandidate } from '../../lib/api'
import ResumeSelect from '../../components/ResumeSelect'

export default function ScreenerPage() {
  const [jobDescription, setJobDescription] = useState('')
  const [selectedResume, setSelectedResume] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const handleScreen = async () => {
    if (!jobDescription.trim()) {
      toast.error('Please enter a job description')
      return
    }

    if (!selectedResume) {
      toast.error('Please select a resume from your library')
      return
    }

    setLoading(true)
    setResult(null)

    try {
      const data = await screenCandidate(jobDescription, selectedResume)
      setResult(data)
      toast.success('Screening complete!')
    } catch (error) {
      toast.error(error.message || 'Failed to screen candidate')
    } finally {
      setLoading(false)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-green-600 bg-green-100 border-green-300'
    if (score >= 75) return 'text-blue-600 bg-blue-100 border-blue-300'
    if (score >= 60) return 'text-yellow-600 bg-yellow-100 border-yellow-300'
    if (score >= 40) return 'text-orange-600 bg-orange-100 border-orange-300'
    return 'text-red-600 bg-red-100 border-red-300'
  }

  const getStatusIcon = (status) => {
    if (status?.includes('Excellent') || status?.includes('High')) {
      return <CheckCircle className="h-6 w-6 text-green-500" />
    }
    if (status?.includes('Moderate')) {
      return <AlertCircle className="h-6 w-6 text-yellow-500" />
    }
    return <XCircle className="h-6 w-6 text-red-500" />
  }

  const getStatusColor = (status) => {
    if (status?.includes('Excellent')) return 'text-green-700 bg-green-50 border-green-200'
    if (status?.includes('High')) return 'text-blue-700 bg-blue-50 border-blue-200'
    if (status?.includes('Moderate')) return 'text-yellow-700 bg-yellow-50 border-yellow-200'
    if (status?.includes('Low')) return 'text-orange-700 bg-orange-50 border-orange-200'
    return 'text-red-700 bg-red-50 border-red-200'
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Resume Screener</h1>
        <p className="text-gray-600">AI-powered analysis comparing candidate resumes against job descriptions</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Input Section */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="mb-6">
            <label className="flex items-center mb-3 text-sm font-semibold text-gray-700">
              <Search className="h-5 w-5 text-primary-600 mr-2" />
              Job Description
            </label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the job description here...&#10;&#10;Example:&#10;We are seeking a Senior Python Developer with 5+ years of experience in FastAPI, Django, and cloud technologies..."
              className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
            />
          </div>

          <div className="mb-6">
            <ResumeSelect
              value={selectedResume}
              onChange={setSelectedResume}
              disabled={loading}
            />
          </div>

          <button
            onClick={handleScreen}
            disabled={loading || !jobDescription.trim() || !selectedResume}
            className="w-full inline-flex items-center justify-center px-6 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Analyzing...
              </>
            ) : (
              <>
                <FileSearch className="h-5 w-5 mr-2" />
                Screen Candidate
              </>
            )}
          </button>
        </div>

        {/* Results Section */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
            <Award className="h-6 w-6 text-primary-600 mr-2" />
            Screening Results
          </h2>
          
          {loading ? (
            <div className="flex items-center justify-center h-96">
              <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
                <p className="text-gray-600">Analyzing candidate with AI...</p>
              </div>
            </div>
          ) : result ? (
            <div className="space-y-6">
              {/* Score Badge */}
              <div className="flex items-center justify-center">
                <div className={`relative ${getScoreColor(result.score)} border-4 rounded-full w-40 h-40 flex flex-col items-center justify-center`}>
                  <div className="text-5xl font-bold">{result.score}</div>
                  <div className="text-sm font-medium">out of 100</div>
                  <TrendingUp className="absolute -top-2 -right-2 h-8 w-8" />
                </div>
              </div>

              {/* Match Status */}
              <div className={`flex items-center justify-center gap-3 p-4 border-2 rounded-lg ${getStatusColor(result.match_status)}`}>
                {getStatusIcon(result.match_status)}
                <span className="text-lg font-semibold">{result.match_status}</span>
              </div>

              {/* Missing Skills */}
              {result.missing_skills && result.missing_skills.length > 0 && (
                <div className="bg-orange-50 border-2 border-orange-200 rounded-lg p-4">
                  <h3 className="font-semibold text-orange-900 mb-3 flex items-center">
                    <AlertCircle className="h-5 w-5 mr-2" />
                    Missing or Weak Skills
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {result.missing_skills.map((skill, index) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-orange-100 text-orange-800 text-sm font-medium rounded-full border border-orange-300"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Reasoning */}
              <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-4">
                <h3 className="font-semibold text-blue-900 mb-2 flex items-center">
                  <FileSearch className="h-5 w-5 mr-2" />
                  Analysis
                </h3>
                <p className="text-blue-800 leading-relaxed">
                  {result.reasoning}
                </p>
              </div>

              {/* Resume Info */}
              <div className="text-center text-sm text-gray-500 pt-4 border-t">
                Analyzed: <span className="font-medium text-gray-700">{result.resume_filename}</span>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-96 text-gray-400">
              <div className="text-center">
                <FileSearch className="h-16 w-16 mx-auto mb-4 opacity-50" />
                <p className="text-lg font-medium mb-2">No Results Yet</p>
                <p className="text-sm">Select a resume and job description,<br />then click "Screen Candidate"</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="font-semibold text-blue-900 mb-2">🎯 AI-Powered Analysis</h4>
          <p className="text-sm text-blue-800">Advanced algorithms compare skills, experience, and qualifications</p>
        </div>
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <h4 className="font-semibold text-green-900 mb-2">📊 Detailed Scoring</h4>
          <p className="text-sm text-green-800">Get a comprehensive score from 0-100 with match status</p>
        </div>
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
          <h4 className="font-semibold text-purple-900 mb-2">🔍 Skills Gap Analysis</h4>
          <p className="text-sm text-purple-800">Identify missing skills and areas for improvement</p>
        </div>
      </div>

      <div className="mt-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <h3 className="font-semibold text-yellow-900 mb-2">How to use:</h3>
        <ol className="text-sm text-yellow-800 space-y-1 list-decimal list-inside">
          <li>Upload candidate resumes using the "Candidate Upload" page</li>
          <li>Select a resume from your library using the dropdown above</li>
          <li>Paste the job description you want to screen against</li>
          <li>Click "Screen Candidate" and review the AI analysis</li>
        </ol>
      </div>
    </div>
  )
}

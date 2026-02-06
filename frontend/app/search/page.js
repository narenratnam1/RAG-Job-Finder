'use client'

import { useState } from 'react'
import { Search, Users, Award, TrendingUp, FileText, Sparkles, Eye, Download, X } from 'lucide-react'
import toast from 'react-hot-toast'
import { searchCandidates } from '../../lib/api'

export default function SearchPage() {
  const [jobDescription, setJobDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [candidates, setCandidates] = useState([])
  const [message, setMessage] = useState('')
  const [previewCandidate, setPreviewCandidate] = useState(null)

  const handleSearch = async () => {
    if (!jobDescription.trim()) {
      toast.error('Please enter a job description')
      return
    }

    setLoading(true)
    setCandidates([])
    setMessage('')

    try {
      const data = await searchCandidates(jobDescription)
      setCandidates(data.candidates || [])
      setMessage(data.message || '')
      
      if (data.count === 0) {
        toast('No candidates found. Upload resumes first!', { icon: '📁' })
      } else {
        toast.success(`Found ${data.count} top candidate${data.count !== 1 ? 's' : ''}!`)
      }
    } catch (error) {
      toast.error(error.message || 'Failed to search candidates')
    } finally {
      setLoading(false)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 90) return 'from-green-500 to-green-600'
    if (score >= 80) return 'from-blue-500 to-blue-600'
    if (score >= 70) return 'from-yellow-500 to-yellow-600'
    if (score >= 60) return 'from-orange-500 to-orange-600'
    return 'from-red-500 to-red-600'
  }

  const getScoreBadgeColor = (score) => {
    if (score >= 90) return 'bg-green-100 text-green-700 border-green-300'
    if (score >= 80) return 'bg-blue-100 text-blue-700 border-blue-300'
    if (score >= 70) return 'bg-yellow-100 text-yellow-700 border-yellow-300'
    if (score >= 60) return 'bg-orange-100 text-orange-700 border-orange-300'
    return 'bg-red-100 text-red-700 border-red-300'
  }

  const getRankBadgeColor = (rank) => {
    if (rank === 1) return 'bg-gradient-to-br from-yellow-400 to-yellow-600 text-white'
    if (rank === 2) return 'bg-gradient-to-br from-gray-300 to-gray-500 text-white'
    if (rank === 3) return 'bg-gradient-to-br from-orange-400 to-orange-600 text-white'
    return 'bg-gradient-to-br from-primary-500 to-primary-700 text-white'
  }

  const getDisplayName = (candidate) => {
    // If name is "Unknown Candidate", use cleaned filename instead
    if (!candidate.name || candidate.name === 'Unknown Candidate') {
      return candidate.filename
        .replace('.pdf', '')
        .replace(/_/g, ' ')
        .replace(/-/g, ' ')
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ')
    }
    return candidate.name
  }

  const handleDownload = (candidate) => {
    // Use download_url from backend if available, otherwise construct it
    const downloadUrl = candidate.download_url 
      ? `http://localhost:8000${candidate.download_url}`
      : `http://localhost:8000/resumes/${encodeURIComponent(candidate.filename)}`
    
    window.open(downloadUrl, '_blank')
    toast.success(`Downloading ${candidate.filename}`)
  }

  const handlePreview = (candidate) => {
    setPreviewCandidate(candidate)
  }

  const closePreview = () => {
    setPreviewCandidate(null)
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Candidate Search & Rank</h1>
        <p className="text-gray-600">Find and rank the best candidates for your job opening using AI-powered search</p>
      </div>

      {/* Search Input Section */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <label className="flex items-center mb-3 text-sm font-semibold text-gray-700">
          <Search className="h-5 w-5 text-primary-600 mr-2" />
          Job Description
        </label>
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste the job description here to find the best matching candidates...&#10;&#10;Example:&#10;Senior Full Stack Developer&#10;Requirements: React, Node.js, Python, 5+ years experience&#10;Nice to have: AWS, Docker, GraphQL"
          className="w-full h-48 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none mb-4"
        />
        
        <button
          onClick={handleSearch}
          disabled={loading || !jobDescription.trim()}
          className="w-full inline-flex items-center justify-center px-6 py-4 bg-gradient-to-r from-primary-600 to-primary-700 text-white font-semibold rounded-lg hover:from-primary-700 hover:to-primary-800 transition-all shadow-lg disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              Searching & Ranking...
            </>
          ) : (
            <>
              <Sparkles className="h-5 w-5 mr-2" />
              Find Top Talent
              <Users className="h-5 w-5 ml-2" />
            </>
          )}
        </button>
      </div>

      {/* Results Section */}
      {loading ? (
        <div className="bg-white rounded-lg shadow-md p-12">
          <div className="flex items-center justify-center">
            <div className="text-center">
              <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto mb-4"></div>
              <p className="text-lg text-gray-700 font-medium">Searching resume database...</p>
              <p className="text-sm text-gray-500 mt-2">AI is analyzing and ranking candidates</p>
            </div>
          </div>
        </div>
      ) : candidates.length > 0 ? (
        <div>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900 flex items-center">
              <Award className="h-7 w-7 text-primary-600 mr-2" />
              Top {candidates.length} Candidate{candidates.length !== 1 ? 's' : ''}
            </h2>
            <div className="text-sm text-gray-500">
              {message && <span className="italic">{message}</span>}
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4">
            {candidates.map((candidate) => (
              <div
                key={candidate.rank}
                className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow border-l-4 border-primary-500"
              >
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-start gap-4 flex-1">
                      {/* Rank Badge */}
                      <div className={`flex items-center justify-center w-14 h-14 rounded-full ${getRankBadgeColor(candidate.rank)} shadow-lg font-bold text-2xl`}>
                        #{candidate.rank}
                      </div>
                      
                      {/* Candidate Info */}
                      <div className="flex-1">
                        <div className="mb-2">
                          {/* Candidate Name - Large and Bold */}
                          <h3 className="text-2xl font-bold text-gray-900 mb-1">
                            {getDisplayName(candidate)}
                          </h3>
                          {/* Filename - Smaller Subtitle */}
                          <div className="flex items-center text-sm text-gray-500">
                            <FileText className="h-4 w-4 mr-1" />
                            {candidate.filename}
                          </div>
                        </div>
                        
                        {/* Reasoning */}
                        <p className="text-gray-700 leading-relaxed mt-3">
                          {candidate.reasoning}
                        </p>
                        
                        {/* Action Buttons */}
                        <div className="flex items-center gap-3 mt-4">
                          <button
                            onClick={() => handlePreview(candidate)}
                            className="inline-flex items-center px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium rounded-lg transition-colors"
                          >
                            <Eye className="h-4 w-4 mr-2" />
                            Preview
                          </button>
                          <button
                            onClick={() => handleDownload(candidate)}
                            className="inline-flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg transition-colors"
                          >
                            <Download className="h-4 w-4 mr-2" />
                            Download
                          </button>
                        </div>
                      </div>
                    </div>

                    {/* Score Badge */}
                    <div className={`ml-4 flex flex-col items-center justify-center px-6 py-3 rounded-lg border-2 ${getScoreBadgeColor(candidate.score)} min-w-24`}>
                      <div className="text-3xl font-bold">{candidate.score}</div>
                      <div className="text-xs font-medium uppercase">Score</div>
                    </div>
                  </div>

                  {/* Quick Stats Bar */}
                  <div className="flex items-center gap-4 mt-4 pt-4 border-t border-gray-200">
                    <div className="flex items-center text-sm text-gray-600">
                      <TrendingUp className="h-4 w-4 mr-1" />
                      Rank {candidate.rank} of {candidates.length}
                    </div>
                    <div className={`px-3 py-1 rounded-full text-xs font-medium ${getScoreBadgeColor(candidate.score)}`}>
                      {candidate.score >= 90 ? 'Exceptional Match' :
                       candidate.score >= 80 ? 'Strong Match' :
                       candidate.score >= 70 ? 'Good Match' :
                       candidate.score >= 60 ? 'Adequate Match' : 'Weak Match'}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : message ? (
        <div className="bg-white rounded-lg shadow-md p-12">
          <div className="text-center">
            <Users className="h-16 w-16 mx-auto mb-4 text-gray-400 opacity-50" />
            <p className="text-lg text-gray-700 font-medium mb-2">{message}</p>
            <p className="text-sm text-gray-500">Upload resumes using the "Candidate Upload" page</p>
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-md p-12">
          <div className="text-center text-gray-400">
            <Search className="h-16 w-16 mx-auto mb-4 opacity-50" />
            <p className="text-lg font-medium mb-2">No Search Yet</p>
            <p className="text-sm">Enter a job description above and click "Find Top Talent"</p>
          </div>
        </div>
      )}

      {/* Info Section */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="font-semibold text-blue-900 mb-2">🔍 Smart Search</h4>
          <p className="text-sm text-blue-800">Vector database finds semantically similar candidates</p>
        </div>
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
          <h4 className="font-semibold text-purple-900 mb-2">🤖 AI Reranking</h4>
          <p className="text-sm text-purple-800">GPT-3.5 evaluates and ranks candidates by fit</p>
        </div>
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <h4 className="font-semibold text-green-900 mb-2">🎯 Top 7 Results</h4>
          <p className="text-sm text-green-800">Get the best matches ranked from best to worst</p>
        </div>
      </div>

      <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="font-semibold text-blue-900 mb-2">How it works:</h3>
        <ol className="text-sm text-blue-800 space-y-1 list-decimal list-inside">
          <li>Vector search finds 10 semantically similar resumes from the database</li>
          <li>AI analyzes all 10 candidates against your job requirements</li>
          <li>GPT-3.5 selects and ranks the top 7 best matches</li>
          <li>Results show scores, reasoning, and ranking for easy comparison</li>
        </ol>
      </div>

      {/* Preview Modal */}
      {previewCandidate && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" onClick={closePreview}>
          <div className="bg-white rounded-lg shadow-2xl max-w-7xl w-full max-h-[90vh] overflow-hidden" onClick={(e) => e.stopPropagation()}>
            {/* Modal Header */}
            <div className="bg-gradient-to-r from-primary-600 to-primary-700 text-white p-6 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className={`flex items-center justify-center w-12 h-12 rounded-full ${getRankBadgeColor(previewCandidate.rank)} shadow-lg font-bold text-xl`}>
                  #{previewCandidate.rank}
                </div>
                <div>
                  <h2 className="text-2xl font-bold">{getDisplayName(previewCandidate)}</h2>
                  <p className="text-primary-100 text-sm flex items-center mt-1">
                    <FileText className="h-4 w-4 mr-1" />
                    {previewCandidate.filename}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className={`px-4 py-2 rounded-lg ${getScoreBadgeColor(previewCandidate.score)} font-bold text-lg`}>
                  Score: {previewCandidate.score}
                </div>
                <button
                  onClick={closePreview}
                  className="p-2 hover:bg-primary-800 rounded-lg transition-colors"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>
            </div>

            {/* Modal Body - Two Column Layout */}
            <div className="grid grid-cols-2 gap-4 p-6 overflow-y-auto max-h-[calc(90vh-180px)]">
              {/* Left Column: AI Analysis */}
              <div className="space-y-6">
                {/* Match Status Badge */}
                <div className="mb-4">
                  <div className={`inline-flex px-4 py-2 rounded-full text-sm font-medium ${getScoreBadgeColor(previewCandidate.score)}`}>
                    {previewCandidate.score >= 90 ? '⭐ Exceptional Match' :
                     previewCandidate.score >= 80 ? '🎯 Strong Match' :
                     previewCandidate.score >= 70 ? '👍 Good Match' :
                     previewCandidate.score >= 60 ? '✓ Adequate Match' : '⚠️ Weak Match'}
                  </div>
                </div>

                {/* Quick Stats */}
                <div className="grid grid-cols-3 gap-3 mb-4">
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 text-center">
                    <div className="text-xl font-bold text-blue-700">#{previewCandidate.rank}</div>
                    <div className="text-xs text-blue-600 font-medium mt-1">Rank</div>
                  </div>
                  <div className={`border-2 rounded-lg p-3 text-center ${getScoreBadgeColor(previewCandidate.score)}`}>
                    <div className="text-xl font-bold">{previewCandidate.score}</div>
                    <div className="text-xs font-medium mt-1">Score</div>
                  </div>
                  <div className="bg-purple-50 border border-purple-200 rounded-lg p-3 text-center">
                    <div className="text-xl font-bold text-purple-700">
                      {previewCandidate.score >= 90 ? 'A+' :
                       previewCandidate.score >= 80 ? 'A' :
                       previewCandidate.score >= 70 ? 'B' :
                       previewCandidate.score >= 60 ? 'C' : 'D'}
                    </div>
                    <div className="text-xs text-purple-600 font-medium mt-1">Grade</div>
                  </div>
                </div>

                {/* Reasoning Section */}
                <div className="mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                    <Award className="h-5 w-5 text-primary-600 mr-2" />
                    AI Analysis & Reasoning
                  </h3>
                  <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 max-h-64 overflow-y-auto">
                    <p className="text-gray-700 leading-relaxed whitespace-pre-wrap text-sm">
                      {previewCandidate.reasoning}
                    </p>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => handleDownload(previewCandidate)}
                    className="flex-1 inline-flex items-center justify-center px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-colors"
                  >
                    <Download className="h-5 w-5 mr-2" />
                    Download
                  </button>
                  <button
                    onClick={closePreview}
                    className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold rounded-lg transition-colors"
                  >
                    Close
                  </button>
                </div>
              </div>

              {/* Right Column: PDF Preview */}
              <div className="flex flex-col h-full">
                <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                  <FileText className="h-5 w-5 text-primary-600 mr-2" />
                  Resume Preview
                </h3>
                <div className="flex-1 border-2 border-gray-300 rounded-lg overflow-hidden bg-gray-100">
                  {previewCandidate.download_url ? (
                    <iframe
                      src={`http://localhost:8000${previewCandidate.download_url}`}
                      className="w-full h-full min-h-[600px]"
                      title="Resume PDF Preview"
                    />
                  ) : (
                    <div className="flex items-center justify-center h-full text-gray-500">
                      <div className="text-center">
                        <FileText className="h-16 w-16 mx-auto mb-4 opacity-50" />
                        <p>PDF preview not available</p>
                        <button
                          onClick={() => handleDownload(previewCandidate)}
                          className="mt-4 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg"
                        >
                          Download to View
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

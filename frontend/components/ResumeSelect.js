'use client'

import { useState, useEffect } from 'react'
import { RefreshCw, FileText } from 'lucide-react'
import toast from 'react-hot-toast'
import { getResumes } from '../lib/api'

export default function ResumeSelect({ value, onChange, disabled = false }) {
  const [resumes, setResumes] = useState([])
  const [loading, setLoading] = useState(false)

  const fetchResumes = async () => {
    setLoading(true)
    try {
      const data = await getResumes()
      setResumes(data.resumes || [])
      if (data.count === 0) {
        toast('No saved resumes found. Upload one first!', { icon: '📁' })
      }
    } catch (error) {
      console.error('Failed to fetch resumes:', error)
      toast.error('Failed to load resume library')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchResumes()
  }, [])

  return (
    <div className="space-y-2">
      <label className="flex items-center text-sm font-semibold text-gray-700">
        <FileText className="h-5 w-5 text-primary-600 mr-2" />
        Select Saved Resume
      </label>
      
      <div className="flex gap-2">
        <select
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          disabled={disabled || loading}
          className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
        >
          <option value="">-- Select a resume --</option>
          {resumes.map((resume) => (
            <option key={resume} value={resume}>
              {resume}
            </option>
          ))}
        </select>
        
        <button
          onClick={fetchResumes}
          disabled={loading}
          className="px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:bg-gray-100 disabled:cursor-not-allowed"
          title="Refresh resume list"
        >
          <RefreshCw className={`h-5 w-5 text-gray-600 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>
      
      {resumes.length === 0 && !loading && (
        <p className="text-sm text-gray-500">
          No saved resumes. Upload one using "Candidate Upload" page.
        </p>
      )}
      
      {resumes.length > 0 && (
        <p className="text-sm text-gray-500">
          {resumes.length} resume{resumes.length !== 1 ? 's' : ''} in your library
        </p>
      )}
    </div>
  )
}

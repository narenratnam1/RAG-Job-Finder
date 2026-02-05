'use client'

import { useState, useCallback } from 'react'
import { Wand2, Download, FileText, Upload, Eye, CheckCircle, X } from 'lucide-react'
import toast from 'react-hot-toast'
import { tailorResumeWithFile, generatePDF } from '../../lib/api'
import ResumeSelect from '../../components/ResumeSelect'

export default function TailorPage() {
  const [jobDescription, setJobDescription] = useState('')
  const [useLibrary, setUseLibrary] = useState(true)
  const [selectedResume, setSelectedResume] = useState('')
  const [resumeFile, setResumeFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [tailoredText, setTailoredText] = useState('')
  const [isDragging, setIsDragging] = useState(false)
  const [downloadingPDF, setDownloadingPDF] = useState(false)

  const handleDragOver = useCallback((e) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    setIsDragging(false)

    const file = e.dataTransfer.files[0]
    if (file && file.type === 'application/pdf') {
      setResumeFile(file)
      toast.success(`Selected: ${file.name}`)
    } else {
      toast.error('Please upload a PDF file')
    }
  }, [])

  const handleFileInput = (e) => {
    const file = e.target.files[0]
    if (file) {
      setResumeFile(file)
      toast.success(`Selected: ${file.name}`)
    }
  }

  const handleGeneratePreview = async () => {
    if (!jobDescription.trim()) {
      toast.error('Please provide a job description')
      return
    }

    if (useLibrary && !selectedResume) {
      toast.error('Please select a resume from your library')
      return
    }

    if (!useLibrary && !resumeFile) {
      toast.error('Please upload a resume file')
      return
    }

    setLoading(true)
    setTailoredText('')

    try {
      const result = await tailorResumeWithFile(
        jobDescription,
        useLibrary ? null : resumeFile,
        useLibrary ? selectedResume : null
      )
      setTailoredText(result.tailored_text)
      toast.success('Preview generated successfully!')
    } catch (error) {
      toast.error(error.message || 'Failed to generate preview')
    } finally {
      setLoading(false)
    }
  }

  const handleDownloadPDF = async () => {
    if (!tailoredText) {
      toast.error('No preview to download')
      return
    }

    setDownloadingPDF(true)

    try {
      const blob = await generatePDF(tailoredText)
      
      // Create download link
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'tailored_resume.pdf'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)

      toast.success('PDF downloaded successfully!')
    } catch (error) {
      toast.error(error.message || 'Failed to download PDF')
    } finally {
      setDownloadingPDF(false)
    }
  }

  const clearResumeFile = () => {
    setResumeFile(null)
    setTailoredText('')
  }

  const toggleResumeSource = () => {
    setUseLibrary(!useLibrary)
    setSelectedResume('')
    setResumeFile(null)
    setTailoredText('')
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Resume Tailor</h1>
        <p className="text-gray-600">Upload your resume and job description to generate a tailored version with preview</p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Job Description Input */}
          <div>
            <label className="flex items-center mb-3 text-sm font-semibold text-gray-700">
              <FileText className="h-5 w-5 text-primary-600 mr-2" />
              Job Description
            </label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the target job description here...&#10;&#10;Example:&#10;Senior Full Stack Developer&#10;Required Skills: React, Node.js, Python, AWS..."
              className="w-full h-80 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
            />
          </div>

          {/* Resume Selection/Upload */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <label className="flex items-center text-sm font-semibold text-gray-700">
                <Upload className="h-5 w-5 text-primary-600 mr-2" />
                Your Resume
              </label>
              <button
                onClick={toggleResumeSource}
                className="text-sm text-primary-600 hover:text-primary-700 font-medium"
              >
                {useLibrary ? '+ Upload new file' : '← Use saved resume'}
              </button>
            </div>

            {useLibrary ? (
              /* Use Saved Resume from Library */
              <div className="h-80 flex flex-col justify-center">
                <ResumeSelect
                  value={selectedResume}
                  onChange={setSelectedResume}
                  disabled={loading}
                />
                
                {selectedResume && (
                  <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                    <div className="flex items-center">
                      <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
                      <div>
                        <p className="text-sm font-medium text-green-900">Resume Selected</p>
                        <p className="text-xs text-green-700">{selectedResume}</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              /* Upload New Resume File */
              <div>
                {resumeFile ? (
                  <div className="h-80 border-2 border-green-300 bg-green-50 rounded-lg p-6 flex flex-col items-center justify-center">
                    <CheckCircle className="h-16 w-16 text-green-500 mb-4" />
                    <p className="text-lg font-semibold text-gray-900 mb-2">{resumeFile.name}</p>
                    <p className="text-sm text-gray-600 mb-4">
                      {(resumeFile.size / 1024).toFixed(2)} KB
                    </p>
                    <button
                      onClick={clearResumeFile}
                      className="inline-flex items-center px-4 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors"
                    >
                      <X className="h-4 w-4 mr-2" />
                      Remove File
                    </button>
                  </div>
                ) : (
                  <div
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    className={`h-80 border-2 border-dashed rounded-lg p-6 flex flex-col items-center justify-center transition-colors ${
                      isDragging
                        ? 'border-primary-500 bg-primary-50'
                        : 'border-gray-300 hover:border-primary-400'
                    }`}
                  >
                    <Upload className="h-16 w-16 text-gray-400 mb-4" />
                    <p className="text-lg font-semibold text-gray-900 mb-2">
                      Drag and drop your resume PDF
                    </p>
                    <p className="text-sm text-gray-600 mb-4">or</p>
                    <label className="cursor-pointer">
                      <span className="inline-flex items-center px-6 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 transition-colors">
                        <FileText className="h-5 w-5 mr-2" />
                        Browse Files
                      </span>
                      <input
                        type="file"
                        accept=".pdf"
                        onChange={handleFileInput}
                        className="hidden"
                      />
                    </label>
                    <p className="text-xs text-gray-500 mt-4">PDF files only, max 10MB</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Generate Preview Button */}
        <button
          onClick={handleGeneratePreview}
          disabled={loading || !jobDescription.trim() || (useLibrary ? !selectedResume : !resumeFile)}
          className="w-full inline-flex items-center justify-center px-6 py-4 bg-gradient-to-r from-primary-600 to-primary-700 text-white font-semibold rounded-lg hover:from-primary-700 hover:to-primary-800 transition-all shadow-lg disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              Generating Preview...
            </>
          ) : (
            <>
              <Eye className="h-5 w-5 mr-2" />
              Generate Preview
              <Wand2 className="h-5 w-5 ml-2" />
            </>
          )}
        </button>
      </div>

      {/* Preview Section */}
      {tailoredText && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">Preview: Tailored Resume</h2>
            <button
              onClick={handleDownloadPDF}
              disabled={downloadingPDF}
              className="inline-flex items-center px-6 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              {downloadingPDF ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Generating PDF...
                </>
              ) : (
                <>
                  <Download className="h-5 w-5 mr-2" />
                  Download PDF
                </>
              )}
            </button>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-6 max-h-96 overflow-y-auto">
            <pre className="whitespace-pre-wrap text-sm text-gray-800 font-sans leading-relaxed">
              {tailoredText}
            </pre>
          </div>
          
          <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-800">
              ✓ Preview generated! Review the tailored content above, then click "Download PDF" to save it.
            </p>
          </div>
        </div>
      )}

      {/* Info Section */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="font-semibold text-blue-900 mb-2">📚 Resume Library</h4>
          <p className="text-sm text-blue-800">Reuse saved resumes or upload new ones</p>
        </div>
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <h4 className="font-semibold text-green-900 mb-2">👀 Preview First</h4>
          <p className="text-sm text-green-800">Review the AI-tailored content before downloading</p>
        </div>
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
          <h4 className="font-semibold text-purple-900 mb-2">⬇️ Download PDF</h4>
          <p className="text-sm text-purple-800">Get a professionally formatted PDF when ready</p>
        </div>
      </div>
    </div>
  )
}

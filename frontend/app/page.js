'use client'

import { useState, useCallback } from 'react'
import { Upload, FileText, CheckCircle } from 'lucide-react'
import toast from 'react-hot-toast'
import { uploadPDF } from '../lib/api'

export default function HomePage() {
  const [isDragging, setIsDragging] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadedFile, setUploadedFile] = useState(null)

  const handleDragOver = useCallback((e) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback(async (e) => {
    e.preventDefault()
    setIsDragging(false)

    const file = e.dataTransfer.files[0]
    if (file && file.type === 'application/pdf') {
      await handleUpload(file)
    } else {
      toast.error('Please upload a PDF file')
    }
  }, [])

  const handleFileInput = async (e) => {
    const file = e.target.files[0]
    if (file) {
      await handleUpload(file)
    }
  }

  const handleUpload = async (file) => {
    setUploading(true)
    try {
      const result = await uploadPDF(file)
      setUploadedFile({
        name: file.name,
        chunks: result.chunks_processed
      })
      toast.success(`Successfully uploaded ${file.name}!`)
    } catch (error) {
      toast.error(error.message || 'Failed to upload file')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Candidate Upload</h1>
        <p className="text-gray-600">Upload candidate resumes in PDF format for processing and analysis</p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-8">
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
            isDragging
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400'
          }`}
        >
          <div className="flex flex-col items-center justify-center">
            {uploading ? (
              <>
                <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mb-4"></div>
                <p className="text-gray-600">Uploading and processing...</p>
              </>
            ) : uploadedFile ? (
              <>
                <CheckCircle className="h-16 w-16 text-green-500 mb-4" />
                <p className="text-lg font-semibold text-gray-900 mb-2">{uploadedFile.name}</p>
                <p className="text-sm text-gray-600">Processed {uploadedFile.chunks} chunks successfully</p>
                <button
                  onClick={() => setUploadedFile(null)}
                  className="mt-4 text-primary-600 hover:text-primary-700 font-medium"
                >
                  Upload Another File
                </button>
              </>
            ) : (
              <>
                <Upload className="h-16 w-16 text-gray-400 mb-4" />
                <p className="text-lg font-semibold text-gray-900 mb-2">
                  Drag and drop your PDF here
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
              </>
            )}
          </div>
        </div>

        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-semibold text-blue-900 mb-2">How it works:</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Upload candidate resume PDFs to the system</li>
            <li>• Documents are automatically processed and indexed</li>
            <li>• Use the Resume Screener to evaluate candidates against job descriptions</li>
            <li>• Use the AI Resume Tailor to customize resumes for specific roles</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

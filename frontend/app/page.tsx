'use client'

import { useState } from 'react'
import { Target, FileText, Upload, AlertCircle, Lightbulb, CheckCircle, XCircle } from 'lucide-react'
import axios from 'axios'

interface AnalysisResult {
  match_percentage: number
  similarity_score: number
  resume_skills: string[]
  jd_skills: string[]
  matching_skills: string[]
  missing_skills: string[]
  resume_length: number
  jd_length: number
  analysis: {
    overall_match: string
    skill_coverage: string
    recommendations: string[]
  }
}

export default function Home() {
  const [resumeFile, setResumeFile] = useState<File | null>(null)
  const [resumeText, setResumeText] = useState('')
  const [jdFile, setJdFile] = useState<File | null>(null)
  const [jdText, setJdText] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState('')

  const handleFileUpload = (file: File | null, type: 'resume' | 'jd') => {
    if (type === 'resume') {
      setResumeFile(file)
      setResumeText('')
    } else {
      setJdFile(file)
      setJdText('')
    }
  }

  const handleTextInput = (text: string, type: 'resume' | 'jd') => {
    if (type === 'resume') {
      setResumeText(text)
      setResumeFile(null)
    } else {
      setJdText(text)
      setJdFile(null)
    }
  }

  const analyzeResumeJD = async () => {
    if ((!resumeFile && !resumeText) || (!jdFile && !jdText)) {
      setError('Please provide both resume and job description content')
      return
    }

    setIsAnalyzing(true)
    setError('')

    try {
      const formData = new FormData()
      
      if (resumeFile) {
        formData.append('resume_file', resumeFile)
      } else if (resumeText) {
        formData.append('resume_text', resumeText)
      }
      
      if (jdFile) {
        formData.append('jd_file', jdFile)
      } else if (jdText) {
        formData.append('jd_text', jdText)
      }

      const response = await axios.post('/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setResult(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred during analysis')
    } finally {
      setIsAnalyzing(false)
    }
  }

  const getMatchColor = (percentage: number) => {
    if (percentage >= 80) return 'text-green-600'
    if (percentage >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getMatchBgColor = (percentage: number) => {
    if (percentage >= 80) return 'bg-green-100'
    if (percentage >= 60) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  const resetForm = () => {
    setResumeFile(null)
    setResumeText('')
    setJdFile(null)
    setJdText('')
    setResult(null)
    setError('')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center">
            <div className="p-3 bg-blue-100 rounded-full mr-4">
              <Target className="w-8 h-8 text-blue-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Resume & JD Matcher</h1>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                AI-powered tool that matches your resume with job descriptions.
              </p>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="card mb-8 border-red-200 bg-red-50">
            <div className="flex items-center">
              <AlertCircle className="w-5 h-5 text-red-600 mr-2" />
              <span className="text-red-800">{error}</span>
            </div>
          </div>
        )}

        {!result ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Resume Input */}
            <div className="card">
              <div className="flex items-center mb-4">
                <FileText className="w-6 h-6 text-blue-600 mr-3" />
                <h2 className="text-xl font-semibold text-gray-900">Resume</h2>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Upload Resume File
                  </label>
                  <input
                    type="file"
                    accept=".pdf,.docx,.txt"
                    onChange={(e) => handleFileUpload(e.target.files?.[0] || null, 'resume')}
                    className="input-field"
                  />
                  <p className="text-sm text-gray-500 mt-1">
                    Supported formats: PDF, DOCX, TXT
                  </p>
                </div>
                
                <div className="text-center text-gray-500">OR</div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Paste Resume Text
                  </label>
                  <textarea
                    value={resumeText}
                    onChange={(e) => handleTextInput(e.target.value, 'resume')}
                    placeholder="Paste your resume content here..."
                    rows={8}
                    className="input-field"
                  />
                </div>
              </div>
            </div>

            {/* Job Description Input */}
            <div className="card">
              <div className="flex items-center mb-4">
                <Target className="w-6 h-6 text-blue-600 mr-3" />
                <h2 className="text-xl font-semibold text-gray-900">Job Description</h2>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Upload Job Description File
                  </label>
                  <input
                    type="file"
                    accept=".pdf,.docx,.txt"
                    onChange={(e) => handleFileUpload(e.target.files?.[0] || null, 'jd')}
                    className="input-field"
                  />
                  <p className="text-sm text-gray-500 mt-1">
                    Supported formats: PDF, DOCX, TXT
                  </p>
                </div>
                
                <div className="text-center text-gray-500">OR</div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Paste Job Description
                  </label>
                  <textarea
                    value={jdText}
                    onChange={(e) => handleTextInput(e.target.value, 'jd')}
                    placeholder="Paste the job description here..."
                    rows={8}
                    className="input-field"
                  />
                </div>
              </div>
            </div>
          </div>
        ) : (
          /* Results Display */
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-gray-900">Analysis Results</h2>
              <button onClick={resetForm} className="btn-secondary">
                Analyze Another
              </button>
            </div>

            {/* Match Score */}
            <div className="card text-center">
              <div className={`inline-flex items-center justify-center w-24 h-24 rounded-full ${getMatchBgColor(result.match_percentage)} mb-4`}>
                <span className={`text-3xl font-bold ${getMatchColor(result.match_percentage)}`}>
                  {result.match_percentage}%
                </span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Overall Match: {result.analysis.overall_match}
              </h3>
              <p className="text-gray-600">
                {result.analysis.skill_coverage} skills matched
              </p>
            </div>

            {/* Skills Analysis */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
                  Matching Skills ({result.matching_skills.length})
                </h3>
                <div className="flex flex-wrap">
                  {result.matching_skills.map((skill, index) => (
                    <span key={index} className="skill-tag skill-match">
                      {skill}
                    </span>
                  ))}
                  {result.matching_skills.length === 0 && (
                    <p className="text-gray-500">No matching skills found</p>
                  )}
                </div>
              </div>

              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <XCircle className="w-5 h-5 text-yellow-600 mr-2" />
                  Missing Skills ({result.missing_skills.length})
                </h3>
                <div className="flex flex-wrap">
                  {result.missing_skills.map((skill, index) => (
                    <span key={index} className="skill-tag skill-missing">
                      {skill}
                    </span>
                  ))}
                  {result.missing_skills.length === 0 && (
                    <p className="text-gray-500">All required skills are present!</p>
                  )}
                </div>
              </div>
            </div>

            {/* Recommendations */}
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Lightbulb className="w-5 h-5 text-blue-600 mr-2" />
                Recommendations
              </h3>
              <ul className="space-y-2">
                {result.analysis.recommendations.map((rec, index) => (
                  <li key={index} className="flex items-start">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span className="text-gray-700">{rec}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Detailed Stats */}
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Detailed Statistics</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-blue-600">{result.match_percentage}%</div>
                  <div className="text-sm text-gray-600">Match Score</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-gray-600">{result.resume_skills.length}</div>
                  <div className="text-sm text-gray-600">Resume Skills</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-gray-600">{result.jd_skills.length}</div>
                  <div className="text-sm text-gray-600">JD Skills</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-gray-600">{result.matching_skills.length}</div>
                  <div className="text-sm text-gray-600">Matched Skills</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Action Button */}
        {!result && (
          <div className="text-center mt-8">
            <button
              onClick={analyzeResumeJD}
              disabled={isAnalyzing}
              className="btn-primary text-lg px-8 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isAnalyzing ? (
                <div className="flex items-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Analyzing...
                </div>
              ) : (
                <div className="flex items-center">
                  <Upload className="w-5 h-5 mr-2" />
                  Analyze Match
                </button>
              )}
            </button>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="text-center mt-16 text-gray-500">
        <p>Powered by AI & NLP</p>
      </div>
    </div>
  )
}

import React, { useState, useEffect } from 'react'

const API_BASE_URL = 'http://localhost:5000/api'

const JobDetailsPage = ({ jobId, onNavigate, currentUser }) => {
  const [job, setJob] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [applying, setApplying] = useState(false)
  const [applicationSuccess, setApplicationSuccess] = useState(false)

  useEffect(() => {
    fetchJobDetails()
  }, [jobId])

  const fetchJobDetails = async () => {
    try {
      setLoading(true)
      setError('')
      
      const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`, {
        credentials: 'include'
      })
      
      if (response.ok) {
        const data = await response.json()
        const jobData = data.job
        
        // Transform backend data to frontend format
        setJob({
          id: jobData.id || jobData._id,
          title: jobData.title,
          company: jobData.company,
          location: jobData.location,
          salary: jobData.salary_min && jobData.salary_max 
            ? `${jobData.salary_currency === 'PKR' ? 'PKR' : '$'} ${(jobData.salary_min/100000).toFixed(1)}-${(jobData.salary_max/100000).toFixed(1)} LPA`
            : 'Salary not disclosed',
          type: jobData.type,
          category: jobData.category,
          tags: jobData.skills_required || [],
          description: jobData.description,
          requirements: jobData.requirements || [],
          responsibilities: jobData.responsibilities || [],
          benefits: [
            'Competitive salary package',
            'Professional development opportunities',
            'Health benefits',
            'Flexible working arrangements'
          ],
          postedDate: jobData.created_at ? new Date(jobData.created_at).toISOString().split('T')[0] : 'Recently',
          companyDescription: `${jobData.company} is a leading company in the ${jobData.category} sector.`,
          posted_by: jobData.posted_by
        })
      } else {
        setError('Failed to load job details')
      }
    } catch (err) {
      console.error('Error fetching job:', err)
      setError('Error connecting to server')
    } finally {
      setLoading(false)
    }
  }

  const handleApply = async () => {
    if (!currentUser) {
      onNavigate('login')
      return
    }
    
    // FIXED: Use 'job_seeker' with underscore instead of 'jobseeker'
    if (currentUser.role !== 'job_seeker') {
      alert('Only job seekers can apply for jobs')
      return
    }

    setApplying(true)
    setError('')

    try {
      const response = await fetch(`${API_BASE_URL}/applications`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          job_id: jobId,
          cover_letter: `I am interested in the ${job.title} position at ${job.company}. I believe my skills and experience make me a strong candidate for this role.`
        }),
        credentials: 'include'
      })

      const data = await response.json()

      if (response.ok) {
        setApplicationSuccess(true)
        setTimeout(() => setApplicationSuccess(false), 3000)
      } else {
        setError(data.error || 'Failed to submit application')
      }
    } catch (err) {
      console.error('Error applying:', err)
      setError('Error submitting application')
    } finally {
      setApplying(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin border-4 border-gray-300 border-t-teal-600 rounded-full w-12 h-12"></div>
          <p className="mt-4 text-gray-600">Loading job details...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 text-xl mb-4">⚠️</div>
          <p className="text-gray-600">{error}</p>
          <button 
            onClick={fetchJobDetails}
            className="mt-4 text-teal-600 hover:underline"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  if (!job) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Job not found</h2>
          <button onClick={() => onNavigate('jobs')} className="bg-teal-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-teal-700">
            Back to Jobs
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-gray-800 to-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <button 
            onClick={() => onNavigate('jobs')}
            className="mb-4 text-white hover:text-gray-200 flex items-center gap-2"
          >
            ← Back to Jobs
          </button>
          <h1 className="text-4xl font-bold mb-2">{job.title}</h1>
          <p className="text-xl text-gray-100">{job.company}</p>
          <div className="flex flex-wrap gap-4 mt-4 text-gray-100">
            <span>📍 {job.location}</span>
            <span>💰 {job.salary}</span>
            <span>⏰ {job.type}</span>
            <span>📅 Posted {new Date(job.postedDate).toLocaleDateString()}</span>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Job Description */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Job Description</h2>
              <p className="text-gray-700 leading-relaxed">{job.description}</p>
            </div>

            {/* Requirements */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Requirements</h2>
              <ul className="space-y-2">
                {job.requirements.map((req, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-teal-600 mr-2">•</span>
                    <span className="text-gray-700">{req}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Benefits */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Benefits</h2>
              <ul className="space-y-2">
                {job.benefits.map((benefit, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-green-600 mr-2">✓</span>
                    <span className="text-gray-700">{benefit}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Skills */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Required Skills</h2>
              <div className="flex flex-wrap gap-2">
                {job.tags.map((tag, index) => (
                  <span key={index} className="bg-teal-50 text-teal-700 px-3 py-1 rounded-full text-sm font-semibold">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Company Info */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-3">About {job.company}</h3>
              <p className="text-gray-700 text-sm leading-relaxed">{job.companyDescription}</p>
            </div>

            {/* Job Details */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-3">Job Details</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Category:</span>
                  <span className="font-medium">{job.category}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Type:</span>
                  <span className="font-medium">{job.type}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Location:</span>
                  <span className="font-medium">{job.location}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Salary:</span>
                  <span className="font-medium">{job.salary}</span>
                </div>
              </div>
            </div>

            {/* Apply Button */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              {applicationSuccess && (
                <div className="mb-4 bg-green-50 border border-green-200 text-green-800 px-4 py-2 rounded text-sm">
                  ✅ Application submitted successfully!
                </div>
              )}
              {error && (
                <div className="mb-4 bg-red-50 border border-red-200 text-red-800 px-4 py-2 rounded text-sm">
                  {error}
                </div>
              )}
              <button
                onClick={handleApply}
                disabled={applying || applicationSuccess}
                className={`w-full text-lg py-3 rounded-lg font-semibold ${
                  applicationSuccess 
                    ? 'bg-green-600 text-white' 
                    : 'bg-teal-600 text-white hover:bg-teal-700 disabled:opacity-50'
                }`}
              >
                {applying 
                  ? 'Submitting...' 
                  : applicationSuccess 
                    ? 'Applied!' 
                    : currentUser 
                      ? 'Apply Now' 
                      : 'Sign in to Apply'}
              </button>
              <p className="text-xs text-gray-500 text-center mt-2">
                {currentUser ? 'Click to submit your application' : 'Sign in to apply for this job'}
              </p>
            </div>

            {/* Share */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-3">Share this job</h3>
              <div className="flex gap-2">
                <button className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm hover:bg-gray-50">
                  Share
                </button>
                <button className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm hover:bg-gray-50">
                  Save
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default JobDetailsPage